import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from tkinter import Tk, filedialog
from tqdm import tqdm
import json

#  def plot_lidar_data(data, oc_cal, oc_dis):
#     plt.figure(figsize=(10, 6))
    
#     # ข้อมูลเดิม
#     # plt.scatter(data['Digitizer Signal (v * m²)'], data['Distance (m)'], color='red', label="Distance vs Digitizer Signal", alpha=0.7)
#     plt.plot(data['Digitizer Signal (v * m²)'], data['Distance (m)'], color='red', linewidth=2, label="new-data")
#     plt.plot(oc_cal, oc_dis, color='green', linewidth=2, label="old-data")
    
#     plt.title("LIDAR Signal Analyzer - Combined Data", fontsize=14)
#     plt.xlabel("Digitizer Signal (v * m²) : c * Time / 2", fontsize=12)
#     plt.ylabel("Distance (m) : Ampl * Distance (m) **2", fontsize=12)
#     plt.grid(True)
#     plt.xlim(left=0)
#     plt.ylim(bottom=0)
#     plt.legend()
#     plt.show()

def plot_lidar_data(data, oc_cal, oc_dis):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # ข้อมูลที่พล็อต
    line1, = ax.plot(data['Digitizer Signal (v * m²)'], data['Distance (m)'], color='red', linewidth=2, label="new-data")
    line2, = ax.plot(oc_cal, oc_dis, color='green', linewidth=2, label="old-data")

    # ตั้งค่ากราฟ
    ax.set_title("LIDAR Signal Analyzer - 03/04/2024 20.00", fontsize=14)
    ax.set_xlabel("Digitizer Signal (v * m²) : Ampl * (Distance (m) ** 2) ", fontsize=12)
    ax.set_ylabel("Distance (m) : (Time * c) / 2", fontsize=12)
    ax.grid(True)
    ax.legend()

    # เพิ่ม CheckButtons สำหรับควบคุมการแสดงผล
    check_ax = plt.axes([0.8, 0.5, 0.1, 0.2])  # กำหนดตำแหน่งของ CheckButtons
    check = CheckButtons(check_ax, ['new-data', 'old-data'], [True, True])

    # ฟังก์ชันสำหรับเปิด/ปิดข้อมูล
    def toggle_lines(label):
        # เปิด/ปิดการแสดงข้อมูล
        if label == 'new-data':
            line1.set_visible(not line1.get_visible())
        elif label == 'old-data':
            line2.set_visible(not line2.get_visible())
        
        # เก็บข้อมูลที่แสดงอยู่
        x_data = []
        y_data = []
        
        # ตรวจสอบข้อมูลที่ยังมองเห็น
        if line1.get_visible():
            x_data.extend(data['Digitizer Signal (v * m²)']) # [::-1]
            y_data.extend(data['Distance (m)'])
        if line2.get_visible():
            x_data.extend(oc_cal)
            y_data.extend(oc_dis)
        
        # ปรับขนาดแกน x และ y อัตโนมัติ
        if x_data and y_data:  # ป้องกันกรณีไม่มีข้อมูลที่แสดง
            # ax.set_xlim(0, max(x_data))  # left=0 เสมอ
            ax.set_xlim(min(x_data), max(x_data))
            ax.set_ylim(min(y_data), max(y_data))
        else:  # หากไม่มีข้อมูลที่แสดง ให้รีเซ็ตขอบเขต
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        
        plt.draw()

    check.on_clicked(toggle_lines)

    # แสดงกราฟ
    plt.show()

def filter_outliers(data):
    return data

def process_files(file_paths):
    file_data = []  # เก็บข้อมูลของแต่ละไฟล์
    for file_path in tqdm(file_paths, desc="Processing files", unit="file"):
        try:
            data = pd.read_csv(file_path, skiprows=4)
            if not {'Time', 'Ampl'}.issubset(data.columns):
                print(f"File {file_path} does not contain 'Time' and 'Ampl' columns. Skipping...")
                continue
            
            data = data[['Time', 'Ampl']].dropna()
            file_data.append(data)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # ตรวจสอบว่าแต่ละไฟล์มีจำนวนแถวเท่ากัน
    row_counts = [len(data) for data in file_data]
    if len(set(row_counts)) != 1:
        raise ValueError("All files must have the same number of rows.")

    # ใช้ Mean ในการหาค่าเฉลี่ยของแต่ละแถวจากทุกไฟล์
    combined_data = pd.concat(file_data).groupby(level=0).mean()

    # คำนวณค่าตามสูตร
    c = 3e8 # m/s
    combined_data['Ampl'] = -combined_data['Ampl']
    # combined_data['Time'] = combined_data['Time'] * 1e6 # แปลงเป็น นาโนวินาทีต่อจุด
    # combined_data['Ampl'] = combined_data['Ampl'] * 1000  # คูณ 1,000 เพื่อเปลี่ยนเป็น mV


    combined_data['Distance (m)'] = (combined_data['Time'] * c) /2 

    combined_data['Digitizer Signal (v * m²)'] = combined_data['Ampl'] * (combined_data['Distance (m)'] **2) 

    # กรองข้อมูลผิดปกติ
    combined_data = filter_outliers(combined_data)

    return combined_data

def save_to_csv(combined_data, oc_cal, oc_dis):
    # สร้าง DataFrame สำหรับ combined_data
    combined_df = combined_data[['Distance (m)', 'Digitizer Signal (v * m²)']].reset_index(drop=True)
    
    # สร้าง DataFrame สำหรับ OC_cal และ OC_dis
    json_data_df = pd.DataFrame({
        'OC_cal': oc_cal,
        'OC_dis': oc_dis
    })

    # รวมข้อมูลทั้งหมด โดยไม่บังคับให้ขนาดเท่ากัน
    combined_output = pd.concat([combined_df['Distance (m)'], json_data_df['OC_dis'], combined_df['Digitizer Signal (v * m²)'], json_data_df['OC_cal']], axis=1)
    combined_output.columns = ['Distance (m)', 'OC_dis', 'Digitizer Signal (v * m²)', 'OC_cal']


    root = Tk()
    root.withdraw()
    output_file = filedialog.asksaveasfilename(
        title="Save Processed CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if output_file:
        try:
            combined_output.to_csv(output_file, index=False)
            print(f"Processed data saved to {output_file}")
        except Exception as e:
            print(f"Error saving processed data to CSV: {e}")
    else:
        print("Save operation cancelled.")

def main():
    print("Welcome to LIDAR Signal Analyzer!")
    print("Please select CSV files.")

    json_file_path = 'ALiN_202404032035.json'
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)
    
    oc_cal = json_data[0]['OC_cal']
    oc_dis = json_data[0]['dis']
    
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select CSV Files",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_paths:
        try:
            data = process_files(file_paths)
            
            if not data.empty:
                plot_lidar_data(data, oc_cal, oc_dis)
                save_to_csv(data, oc_cal, oc_dis)  # บันทึกข้อมูลลงไฟล์ CSV
            else:
                print("No valid data to plot.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No files selected!")

if __name__ == "__main__":
    main()
