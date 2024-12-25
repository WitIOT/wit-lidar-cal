import pandas as pd
from tkinter import Tk, filedialog
import pandas as pd
import matplotlib.pyplot as plt


# ฟังก์ชันสำหรับดึงข้อมูลจากไฟล์ CSV
def load_copol_data(csv_file):
    try:
        # อ่านข้อมูลจากไฟล์ CSV
        data = pd.read_csv(csv_file)

        # ตรวจสอบว่ามีคอลัมน์ copol_raw และ copol_nrb หรือไม่
        if 'copol_raw' not in data.columns or 'copol_nrb' not in data.columns or 'range_nrb' not in data.columns  or 'time' not in data.columns:
            raise ValueError("ไฟล์ CSV ไม่มีคอลัมน์ที่ต้องการ: copol_raw หรือ copol_nrb")

        # ดึงข้อมูลมาเก็บในตัวแปร
        copol_raw = data['copol_raw'].tolist()  # แปลงเป็น List
        copol_nrb = data['copol_nrb'].tolist()  # แปลงเป็น List
        range_nrb = data['range_nrb'].tolist()  # แปลงเป็น List
        Time = data['time'].tolist()  # แปลงเป็น List

        return copol_raw, copol_nrb, range_nrb , Time
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        return None, None

# ฟังก์ชันสำหรับเลือกไฟล์ด้วย UI
def browse_file():
    root = Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลักของ Tkinter
    file_path = filedialog.askopenfilename(title="เลือกไฟล์ CSV", filetypes=[("CSV Files", "*.csv")])
    return file_path

# ฟังก์ชันสำหรับคำนวณ Distance
def calculate_distance(time):
    Distance = [ 2/  x * 3e8  for x in time]
    return Distance

def calculate_Digitizer_signal(Distance1):
    Ds = [(x ** 2) * copol_nrb[i] for i, x in enumerate(Distance1)]
    return Ds

# เลือกไฟล์ CSV ผ่าน UI
csv_file = browse_file()
if csv_file:
    copol_raw, copol_nrb , range_nrb , Time = load_copol_data(csv_file)

    # แสดงผลข้อมูลที่ดึงมา
    if copol_raw is not None and copol_nrb is not None and range_nrb is not None and Time is not None:
        # print("copol_raw:", copol_raw[:5])  # แสดงตัวอย่างข้อมูล 5 ตัวแรก
        # print("copol_nrb:", copol_nrb[:5])  # แสดงตัวอย่างข้อมูล 5 ตัวแรก

        copol_nrb = [x for x in copol_nrb if pd.notna(x)]
        range_nrb = [x for x in range_nrb if pd.notna(x)]
        Time = [x for x in Time if pd.notna(x)]

        Distance1 = calculate_distance(Time)
        Digitizer_signal1 = calculate_Digitizer_signal(range_nrb)
        print("Distance:", Distance1)  # แสดงตัวอย่างข้อมูล 5 ตัวแรก
        print("Digitizer signal:", Digitizer_signal1)  # แสดงตัวอย่างข้อมูล 5 ตัวแรก
        print("Range:", range_nrb)

        plt.figure(figsize=(10, 6))
        plt.plot(Digitizer_signal1, range_nrb, color='blue', linewidth=2 ,  label='Digitizer Signal vs Distance')
        # plt.plot(Distance1, Digitizer_signal1, color='red', linewidth=2 , label='Distance vs Digitizer Signal')
        # plt.stackplot(Distance1, Digitizer_signal1, colors=['red'], alpha=0.5)
        # ตั้งค่าชื่อกราฟและแกน
        plt.title("Distance vs Digitizer Signal")
        plt.xlabel("Digitizer Signal (Digitizer_signal1)")
        plt.ylabel("Distance (Distance1)")
        plt.grid(True)
        plt.legend()
        plt.show()
        
else:
    print("ไม่มีการเลือกไฟล์")
