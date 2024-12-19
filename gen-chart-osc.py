import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- พารามิเตอร์ที่ใช้ในการคำนวณ ---
c = 3e8        # ความเร็วแสง (m/s)
V_full_scale = 1.0   # ช่วงแรงดันสูงสุด ADC (สมมุติ)
N_bits = 12    # ความละเอียด ADC เช่น 12 bits

# อ่านข้อมูลจากไฟล์ โดยข้าม 4 บรรทัดแรก เพื่อให้บรรทัดที่ 5 เป็น header
input_file = 'csv-03-04-2024-tmp4-20-00/C1--20-850v--00000.csv'
df = pd.read_csv(input_file, skiprows=4, header=0)

# ตอนนี้ df ควรจะมีคอลัมน์ "Time" และ "Ampl"
time = df['Time'].values      # เวลา (วินาที)
# voltage = df['Ampl'].values   # แรงดัน (โวลต์)
voltage = -df['Ampl'].values
distance = (c * time) / 2
# แปลงแรงดันเป็น Digital Number (DN)
DN = (voltage / V_full_scale) * (2**N_bits - 1) 
# คำนวณ Range-corrected signal: S_R = DN * R^2
S_R = DN * (distance**2) 

# บันทึกผลลงไฟล์
output_file = 'output_calculated.csv'
df_output = pd.DataFrame({
    'time_s': time,
    'distance_m': distance,
    'voltage_V': voltage,
    'DN': DN,
    'S_R': S_R
})
df_output.to_csv(output_file, index=False)
print(f"Calculation complete! Results saved in {output_file}")

# แสดงผลในรูป chart
plt.figure(figsize=(10,6))

# กราฟที่ 1: แกน x เป็น Voltage, แกน y เป็น Distance
plt.subplot(2, 1, 1) # แสดงกราฟใน 2 แถว 1 คอลัมน์
plt.plot(voltage, distance, label='Voltage (V)') # กราฟเส้นสีฟ้า   
plt.title('LIDAR Data Analysis')
plt.xlabel('Voltage (V)')
plt.ylabel('Distance (m)') 
plt.grid(True) # แสดงเส้นกริด
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
