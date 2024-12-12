import xarray as xr
import pandas as pd
import os
from tqdm import tqdm

# กำหนดโฟลเดอร์ที่มีไฟล์ .nc
input_folder = 'example-data/20241128'  # ระบุโฟลเดอร์ที่ต้องการแปลง
export_folder = os.path.join('Export', os.path.basename(os.path.normpath(input_folder)))

# ตรวจสอบและสร้างโฟลเดอร์ export หากยังไม่มี
os.makedirs(export_folder, exist_ok=True)

# ค้นหาไฟล์ทั้งหมดในโฟลเดอร์ input ที่มีนามสกุล .nc
nc_files = [f for f in os.listdir(input_folder) if f.endswith('.nc')]

if not nc_files:
    print("No .nc files found in the input folder.")
else:
    for nc_file in tqdm(nc_files, desc="Processing files"):
        input_file = os.path.join(input_folder, nc_file)
        output_file = os.path.join(export_folder, os.path.splitext(nc_file)[0] + '.csv')

        try:
            # เปิดไฟล์ .nc
            ds = xr.open_dataset(input_file)

            # ตรวจสอบข้อมูลใน Dataset
            if len(ds.data_vars) == 0:
                print(f"No variables found in the dataset: {nc_file}")
                continue

            # แปลงเฉพาะตัวแปรที่ไม่ซับซ้อน
            df_list = []
            for var_name in ds.data_vars:
                try:
                    # ดึงข้อมูลตัวแปร
                    var_data = ds[var_name].to_dataframe().reset_index()
                    df_list.append(var_data)
                except Exception as e:
                    print(f"Failed to process variable {var_name} in {nc_file}: {e}")

            # รวมทุกตัวแปรลงใน DataFrame เดียว
            if df_list:
                full_df = pd.concat(df_list, axis=1)
                full_df.to_csv(output_file, index=False)
                print(f"Data from {nc_file} saved to {output_file}")
            else:
                print(f"No data could be saved for {nc_file}.")

            # ปิด Dataset
            ds.close()

        except Exception as e:
            print(f"Failed to process file {nc_file}: {e}")