import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

def plot_lidar_data(data,oc_cal, oc_dis):
        # กรองข้อมูล Actual Data ให้เหลือเฉพาะค่าที่ Distance >= 1000
    filtered_data = data[data['Distance (m)'] >= 1000].copy()

    # เลื่อนข้อมูลให้จุดต่ำสุดของ Distance กลายเป็น 0
    if not filtered_data.empty:
        min_distance = filtered_data['Distance (m)'].min()
        filtered_data['Distance (m)'] = filtered_data['Distance (m)'] - min_distance

    
    plt.figure(figsize=(10, 6))
    # plt.scatter(data['Digitizer Signal (v * m²)'], data['Distance (m)'], color='red', label="Distance vs Digitizer Signal", alpha=0.7)
    plt.plot(filtered_data['Digitizer Signal (v * m²)'], filtered_data['Distance (m)'], color='blue', linewidth=2, label="Actual Data")
    plt.plot(oc_cal, oc_dis, color='green', linewidth=2, label="Corrected Data")

    plt.title("LIDAR Signal Analyzer - Combined Data", fontsize=14)
    plt.xlabel("Digitizer Signal (v * m²)", fontsize=12)
    plt.ylabel("Distance (m)", fontsize=12)
    plt.grid(True)
    plt.legend()
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
                plot_lidar_data(data, oc_cal, oc_dis)
            else:
                print("No valid data to plot.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("The specified folder path does not exist.")

if __name__ == "__main__":
    main()
