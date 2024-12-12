import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

def plot_lidar_data(data, oc_cal, oc_dis,folder_path):
    # กรองข้อมูล Actual Data ให้เหลือเฉพาะค่าที่ Distance >= 1000
    filtered_data = data[data['Distance (m)'] >= 1000].copy()

    # เลื่อนข้อมูลให้จุดต่ำสุดของ Distance กลายเป็น 0
    if not filtered_data.empty:
        min_distance = filtered_data['Distance (m)'].min()
        filtered_data['Distance (m)'] = filtered_data['Distance (m)'] - min_distance

    # สร้างกราฟหลัก
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Corrected Data (แกนล่าง)
    ax1.plot(oc_cal, oc_dis, color='green', linewidth=2, label="old software")
    ax1.set_xlabel("Digitizer Signal (v * m²)", fontsize=12, color='green')
    ax1.set_ylabel("Distance (m)", fontsize=12)
    ax1.tick_params(axis='x', labelcolor='green')

    # เพิ่มแกน X ด้านบนสำหรับ Actual Data
    ax2 = ax1.twiny()
    ax2.plot(filtered_data['Digitizer Signal (v * m²)'], filtered_data['Distance (m)'],label="new software")
    # ax2.set_xlabel("Digitizer Signal (v * m²)", fontsize=12, color='blue')
    ax2.tick_params(axis='x', labelcolor='blue')

    # แปลงชื่อ folder ให้เป็นรูปแบบวันที่ เวลา
    folder_name = os.path.basename(folder_path)
    parts = folder_name.split('-')
    # parts = ['csv', '03', '04', '2024', 'tmp4', '20', '00']
    day = parts[1]
    month = parts[2]
    year = parts[3]
    hour = parts[5]
    minute = parts[6]

    # สร้างสตริงวันเวลา
    date_str = f"{day}/{month}/{year} {hour}:{minute}"

    # ตั้ง title: บรรทัดแรกเป็น "LIDAR Signal Analyzer" บรรทัดที่สองเป็นวันเวลา
    chart_title = f"LIDAR Signal Analyzer {date_str}"
    fig.suptitle(chart_title, fontsize=14, fontweight='bold')
    # ดึง handle และ label จากทั้งสองแกนมาเพื่อทำ legend ร่วม
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    # รวม handle และ label ของทั้งสองแกน
    lines = lines1 + lines2
    labels = labels1 + labels2

    # สร้าง legend เดียวที่รวมทั้ง Actual และ Corrected Data
    # loc='upper right' คือให้ legend อยู่มุมขวาบนของแกน
    # bbox_to_anchor=(1, 1) ช่วยปรับให้ legend อยู่ภายในกรอบของ plot
    ax1.legend(lines, labels, loc='upper right', bbox_to_anchor=(1, 1))

    # plt.grid(True)
    plt.show()

def filter_outliers(data):
    # ปรับการกรองข้อมูลตามความเหมาะสม
    return data

def process_files(folder_path):
    # ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์ที่กำหนด
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    file_data = []
    for file_path in tqdm(csv_files, desc="Processing files", unit="file"):
        try:
            data = pd.read_csv(file_path, skiprows=4)
            if not {'Time', 'Ampl'}.issubset(data.columns):
                print(f"File {file_path} does not contain 'Time' and 'Ampl' columns. Skipping...")
                continue
            
            data = data[['Time', 'Ampl']].dropna()
            file_data.append(data)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    row_counts = [len(data) for data in file_data]
    if len(set(row_counts)) != 1:
        raise ValueError("All files must have the same number of rows.")

    # รวมข้อมูลโดยใช้ pd.concat และหาค่าเฉลี่ยตามดัชนี
    combined_data = pd.concat(file_data).groupby(level=0).median()

    # คำนวณค่าที่ต้องการ
    c = 3e8
    combined_data['Ampl'] = -combined_data['Ampl']
    combined_data['Distance (m)'] = (combined_data['Time'] * c) / 2
    combined_data['Digitizer Signal (v * m²)'] = combined_data['Ampl'] * (combined_data['Distance (m)'] ** 2)

    # กรองข้อมูลผิดปกติ
    combined_data = filter_outliers(combined_data)

    return combined_data

def main():
    print("Welcome to LIDAR Signal Analyzer!")
    print("Please provide the folder path containing CSV files.")

    json_file_path = 'ALiN_202404032035.json'
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)
    
    oc_cal = json_data[0]['OC_cal']
    oc_dis = json_data[0]['dis']

    # ระบุเส้นทางโฟลเดอร์ที่มีไฟล์ CSV ไว้ตรงนี้
    folder_path = "../csv-03-04-2024-tmp4-20-00"

    if os.path.isdir(folder_path):
        try:
            data = process_files(folder_path)
            if not data.empty:
                plot_lidar_data(data, oc_cal, oc_dis,folder_path)
            else:
                print("No valid data to plot.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("The specified folder path does not exist.")

if __name__ == "__main__":
    main()
