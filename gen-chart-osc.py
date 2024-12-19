import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# --- พารามิเตอร์ที่ใช้ในการคำนวณ ---
c = 3e8        # ความเร็วแสง (m/s)
V_full_scale = 1.0   # ช่วงแรงดันสูงสุด ADC (สมมุติ)
N_bits = 12    # ความละเอียด ADC เช่น 12 bits

# โฟลเดอร์ที่เก็บไฟล์ CSV และ pattern
input_folder = 'csv-03-04-2024-tmp4-20-00'
pattern = '*.csv'  # หรือปรับรูปแบบให้ตรงกับไฟล์ของคุณ

file_list = glob.glob(os.path.join(input_folder, pattern))
file_list = sorted(file_list)  # เรียงไฟล์ตามลำดับ

ampl_list = []
time_values = None

# อ่านไฟล์ทั้งหมดและเก็บข้อมูล Ampl
for i, f in enumerate(file_list):
    df = pd.read_csv(f, skiprows=4, header=0)
    if time_values is None:
        # เก็บ time จากไฟล์แรกเป็น reference
        time_values = df['Time'].values
    else:
        # ตรวจสอบว่าทุกไฟล์มีขนาดเท่ากัน และเวลาเหมือนกัน
        # ถ้าเวลาไม่เหมือนกัน อาจต้องทำ interpolation เพิ่ม
        if not np.array_equal(time_values, df['Time'].values):
            raise ValueError("Time values in files do not match. Consider interpolation.")
    
    ampl_list.append(df['Ampl'].values)

# แปลงเป็น array 2D: แกน 0 = ไฟล์, แกน 1 = จุดข้อมูล
ampl_array = np.array(ampl_list)  # shape = (N_files, N_points)

# คำนวณ median ของ Ampl ตามแกนไฟล์ (axis=0)
ampl_median = np.median(ampl_array, axis=0)  # shape = (N_points,)

# หลังจากได้ median แล้ว เราจะนำมาใช้งานแทน voltage
# ตามโจทย์เดิม คุณใช้ voltage = -df['Ampl'].values
# ที่นี่ก็ใช้แบบเดียวกัน: voltage = -ampl_median
voltage = -ampl_median

# คำนวณ distance
distance = (c * time_values) / 2

# คำนวณ DN
DN = (voltage / V_full_scale) * (2**N_bits - 1)

# คำนวณ S_R = DN * R^2
S_R = DN * (distance**2)

# บันทึกผลลงไฟล์
output_file = 'output_calculated_median.csv'
df_output = pd.DataFrame({
    'time_s': time_values,
    'distance_m': distance,
    'voltage_V': voltage,
    'DN': DN,
    'S_R': S_R
})
df_output.to_csv(output_file, index=False)
print(f"Median calculation complete! Results saved in {output_file}")

# แสดงผลในรูป chart
plt.figure(figsize=(10,6))

# กราฟที่ 1: แกน x เป็น Voltage, แกน y เป็น Distance
plt.subplot(2, 1, 1) # แสดงกราฟใน 2 แถว 1 คอลัมน์
plt.plot(voltage, distance, label='Voltage (median) (V)')
plt.title('LIDAR Data Analysis (Median from all files) 20240403 20:00')
plt.xlabel('Voltage (V)')
plt.ylabel('Distance (m)') 
plt.grid(True) 
plt.legend()

# กราฟที่ 2: แกน x เป็น S_R, แกน y เป็น Distance
plt.subplot(2, 1, 2)
plt.plot(S_R, distance, label='Range-corrected Signal (S_R)', color='red')
plt.xlabel('S_R (arb. units)')
plt.ylabel('Distance (m)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
