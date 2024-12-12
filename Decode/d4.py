def check_trc_version(file_path):
    """
    Check the version of the LeCroy .trc file.
    """
    try:
        with open(file_path, 'rb') as file:
            # อ่านข้อมูลส่วนหัวของไฟล์
            data = file.read(32)
            # หาตำแหน่ง WAVEDESC เพื่อหา TEMPLATE_NAME
            start_offset = data.find(b'WAVEDESC')
            if start_offset == -1:
                raise ValueError("WAVEDESC not found in the file.")
            
            # เลื่อนตำแหน่งไปยัง TEMPLATE_NAME
            file.seek(start_offset + 16)
            template_name = file.read(16).rstrip(b'\x00').decode('latin_1')
            return template_name
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# ใช้งานฟังก์ชัน
file_path = "C1--20-850v--00002.trc"
version = check_trc_version(file_path)
if version:
    print(f"TRC File Version: {version}")
else:
    print("Could not determine TRC file version.")
