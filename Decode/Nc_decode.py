import xarray as xr
import pandas as pd
import os

input_file = 'example-data/MPL_5038_202404032020.nc'

# กำหนดโฟลเดอร์สำหรับ export
export_folder = 'Export/'

# ตรวจสอบและสร้างโฟลเดอร์ export หากยังไม่มี
os.makedirs(export_folder, exist_ok=True)

# สร้างชื่อไฟล์เอาต์พุตโดยเพิ่มโฟลเดอร์ export และเปลี่ยนนามสกุลเป็น .csv
output_file = os.path.join(export_folder, os.path.splitext(os.path.basename(input_file))[0] + '.csv')
# output_file = 'Decode/output_data_all.csv'

# เปิดไฟล์ .nc
ds = xr.open_dataset(input_file)

# ตรวจสอบข้อมูลใน Dataset
if len(ds.data_vars) == 0:
    print("No variables found in the dataset.")
else:
    # แปลงเฉพาะตัวแปรที่ไม่ซับซ้อน
    df_list = []
    for var_name in ds.data_vars:
        try:
            # ดึงข้อมูลตัวแปร
            var_data = ds[var_name].to_dataframe().reset_index()
            df_list.append(var_data)
        except Exception as e:
            print(f"Failed to process variable {var_name}: {e}")

    # รวมทุกตัวแปรลงใน DataFrame เดียว
    if df_list:
        full_df = pd.concat(df_list, axis=1)
        full_df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("No data could be saved.")

# ปิด Dataset
ds.close()
