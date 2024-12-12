import struct
import numpy as np
import pandas as pd
from tkinter import Tk, filedialog

def extract_waveform_data(file_path, output_csv_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    # Metadata จาก WaveStudio
    horizontal_start = 1.599806e-6
    horizontal_interval = 4e-07  # แก้ให้ตรงกับ WaveStudio
    num_samples = 125002

    # ดึง Metadata (Vertical Gain และ Offset)
    header_start = data.find(b"WAVEDESC")
    if header_start == -1:
        raise ValueError("WAVEDESC not found in the file")
    
    vertical_gain_metadata = struct.unpack("<f", data[header_start + 156:header_start + 160])[0]
    vertical_offset_metadata = struct.unpack("<f", data[header_start + 160:header_start + 164])[0]

    print(f"Vertical Gain (Metadata): {vertical_gain_metadata}")
    print(f"Vertical Offset (Metadata): {vertical_offset_metadata}")

    # Raw waveform data extraction
    wave_descriptor_length = struct.unpack("<i", data[header_start + 36:header_start + 40])[0]
    user_text_length = struct.unpack("<i", data[header_start + 40:header_start + 44])[0]
    wave_array_start = header_start + wave_descriptor_length + user_text_length

    raw_waveform_data = data[wave_array_start:wave_array_start + num_samples * 2]

    # Convert raw waveform data to signed 16-bit integers
    waveform_amplitudes = struct.unpack(f"<{num_samples}h", raw_waveform_data)

    # Debug: แสดงข้อมูลดิบบางส่วน
    print("Raw waveform data (first 10 samples):", waveform_amplitudes[:10])

    # Recalculate Vertical Gain and Offset
    raw_min = min(waveform_amplitudes)
    raw_max = max(waveform_amplitudes)
    wave_min = -0.006  # ช่วงค่าต่ำสุดจาก WaveStudio
    wave_max = 0.004   # ช่วงค่าสูงสุดจาก WaveStudio
    vertical_gain = (wave_max - wave_min) / (raw_max - raw_min)
    vertical_offset = wave_min - (raw_min * vertical_gain)

    print(f"Recalculated Vertical Gain: {vertical_gain}")
    print(f"Recalculated Vertical Offset: {vertical_offset}")

    # Convert amplitudes and times to float64
    amplitudes = np.array([(value * vertical_gain) + vertical_offset for value in waveform_amplitudes], dtype=np.float64)
    times = np.array([i * horizontal_interval + horizontal_start for i in range(num_samples)], dtype=np.float64)

    # Debug: แสดงค่า Amplitude บางส่วน
    print("Converted Amplitudes (first 10 samples):", amplitudes[:10])

    # Create a DataFrame
    waveform_df = pd.DataFrame({"Time": times, "Amplitude": amplitudes})

    # Save to CSV
    waveform_df.to_csv(output_csv_path, index=False, float_format='%.16e')
    print(f"Waveform data saved to {output_csv_path}")

def browse_and_extract():
    # Open file dialog to select the TRC file
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        title="Select TRC File",
        filetypes=[("TRC Files", "*.trc"), ("All Files", "*.*")]
    )
    if not file_path:
        print("No file selected.")
        return

    # Set output file path
    output_csv_path = filedialog.asksaveasfilename(
        title="Save CSV File As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not output_csv_path:
        print("No output file selected.")
        return

    try:
        extract_waveform_data(file_path, output_csv_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    browse_and_extract()
