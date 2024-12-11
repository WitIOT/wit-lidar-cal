import json
import matplotlib.pyplot as plt

# โหลดข้อมูลจากไฟล์ JSON
file_path = 'ALiN_202404032035.json'  # เปลี่ยนเป็นชื่อไฟล์ของคุณ
with open(file_path, 'r') as file:
    data = json.load(file)

# ดึงข้อมูลที่ต้องการจาก JSON
oc_cal = data[0]["OC_cal"]
oc_dis = data[0]["dis"]

# สร้างแผนภูมิ
plt.figure(figsize=(10, 6))
# plt.xlim(left=0)
# plt.plot(oc_cal, oc_dis, 'b.', label="OC vs Distance")
plt.plot(oc_cal, oc_dis, color='blue', linewidth=2, label="ALin Line Connecting Points")
plt.ylim(bottom=0)
plt.xlim(left=0)


# ปรับแต่งแผนภูมิ
plt.title("OC vs Distance Chart")
plt.xlabel("OC (calibrated)")
plt.ylabel("Distance (m)")
plt.legend()
plt.grid(True)

# แสดงผล
plt.show()
