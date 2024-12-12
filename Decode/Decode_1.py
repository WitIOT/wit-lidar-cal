import struct
import numpy as np
import pandas as pd
from tkinter import Tk, filedialog, messagebox
import os

def parse_trc(file_path):
    """
    Function to parse LeCroy .trc file and extract waveform data.
    """
    with open(file_path, 'rb') as file:
        content = file.read()

    # Locate WAVEDESC header
    wave_desc_start = content.find(b'WAVEDESC')

    if wave_desc_start == -1:
        raise ValueError("WAVEDESC header not found in the .trc file.")

    # Extract header information
    wave_desc_length = struct.unpack('i', content[wave_desc_start + 36:wave_desc_start + 40])[0]
    user_text_length = struct.unpack('i', content[wave_desc_start + 40:wave_desc_start + 44])[0]
    trig_time_array_length = struct.unpack('i', content[wave_desc_start + 48:wave_desc_start + 52])[0]
    wave_array_1_length = struct.unpack('i', content[wave_desc_start + 60:wave_desc_start + 64])[0]

    # Horizontal scaling
    horiz_interval = struct.unpack('f', content[wave_desc_start + 176:wave_desc_start + 180])[0]
    horiz_offset = struct.unpack('d', content[wave_desc_start + 180:wave_desc_start + 188])[0]

    # Vertical scaling
    vertical_gain = struct.unpack('f', content[wave_desc_start + 156:wave_desc_start + 160])[0]
    vertical_offset = struct.unpack('f', content[wave_desc_start + 160:wave_desc_start + 164])[0]

    # Locate waveform data
    wave_data_start = wave_desc_start + wave_desc_length + user_text_length + trig_time_array_length
    raw_waveform_data = content[wave_data_start:wave_data_start + wave_array_1_length]

    # Convert waveform data to voltage values
    waveform = np.array(struct.unpack(f'{wave_array_1_length}b', raw_waveform_data))
    voltage = (waveform * vertical_gain) - vertical_offset

    # Generate time data
    time = np.arange(0, len(voltage)) * horiz_interval + horiz_offset

    # Create DataFrame for export
    df = pd.DataFrame({'Time': time, 'Ampl': voltage})

    return df

def main():
    while True:
        # Create a Tkinter directory selection dialog
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        folder_path = filedialog.askdirectory(
            title="Select a folder containing .trc files"
        )

        if not folder_path:
            messagebox.showwarning("No Folder Selected", "You must select a folder to proceed.")
            break

        # Create export folder with the same name as the selected folder
        parent_dir = os.getcwd()
        export_folder_name = os.path.basename(folder_path) + "_export"
        export_dir = os.path.join(parent_dir, export_folder_name)
        os.makedirs(export_dir, exist_ok=True)

        processed_files = 0  # Counter for successful files

        # Process all .trc files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".trc"):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # Parse the .trc file
                    waveform_df = parse_trc(file_path)

                    # Save to CSV with the same filename
                    base_name = file_name.replace(".trc", ".csv")
                    output_csv_path = os.path.join(export_dir, base_name)
                    waveform_df.to_csv(output_csv_path, index=False)

                    # Notify the user for each file
                    print(f"File '{file_path}' processed successfully. Saved as: {output_csv_path}")
                    processed_files += 1

                except Exception as e:
                    print(f"Error processing file '{file_path}': {e}")

        # Notify the user when all files are processed
        messagebox.showinfo(
            "Decoding Completed",
            f"All .trc files in the folder have been processed.\n"
            f"Total files processed: {processed_files}\n"
            f"Files saved in: {export_dir}"
        )

        # Ask if the user wants to process another folder
        if not messagebox.askyesno("Continue?", "Do you want to process another folder?"):
            messagebox.showinfo("Goodbye", "Thank you for using the program!")
            break

if __name__ == "__main__":
    main()
