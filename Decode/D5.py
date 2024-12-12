import struct
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


def decode_trc_to_csv(trc_file_path, output_csv_path):
    """
    Decodes a LeCroy `.trc` file and outputs a CSV similar to WaveStudio's export.
    """
    try:
        with open(trc_file_path, "rb") as f:
            content = f.read()

        # Extract metadata from WAVEDESC header
        header = content[:256]
        desc_len = struct.unpack('I', header[36:40])[0]
        comm_type = struct.unpack('H', header[32:34])[0]
        vertical_gain = struct.unpack('f', header[156:160])[0]
        vertical_offset = struct.unpack('f', header[160:164])[0]
        horizontal_interval = struct.unpack('f', header[176:180])[0]
        horizontal_offset = struct.unpack('d', header[180:188])[0]

        # Extract waveform data
        waveform_start = desc_len
        if comm_type == 0:
            data = np.frombuffer(content[waveform_start:], dtype=np.int8)
        else:
            data = np.frombuffer(content[waveform_start:], dtype=np.int16)

        # Calculate time and amplitude
        num_points = len(data)
        time_values = np.linspace(
            horizontal_offset,
            horizontal_interval * (num_points - 1) + horizontal_offset,
            num_points
        )
        waveform = data * vertical_gain + vertical_offset

        # Create DataFrame and save to CSV
        df = pd.DataFrame({"Time (s)": time_values, "Amplitude": waveform})
        df.to_csv(output_csv_path, index=False)
        return "Decoding successful!"
    except Exception as e:
        return f"Error: {str(e)}"


def select_trc_file():
    """Open file dialog to select a `.trc` file."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Teledyne LeCroy Files", "*.trc")]
    )
    if file_path:
        trc_file_path.set(file_path)


def select_output_csv():
    """Open file dialog to select where to save the output CSV."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        output_csv_path.set(file_path)


def decode_file():
    """Decode the `.trc` file and save the CSV."""
    trc_path = trc_file_path.get()
    csv_path = output_csv_path.get()

    if not trc_path or not csv_path:
        messagebox.showerror("Error", "Please select input and output files!")
        return

    result = decode_trc_to_csv(trc_path, csv_path)
    if "successful" in result:
        messagebox.showinfo("Success", result)
    else:
        messagebox.showerror("Error", result)


# Create GUI window
root = tk.Tk()
root.title("TRC to CSV Decoder")

# Variables to store file paths
trc_file_path = tk.StringVar()
output_csv_path = tk.StringVar()

# Input file selection
tk.Label(root, text="Select .trc File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=trc_file_path, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_trc_file).grid(row=0, column=2, padx=10, pady=5)

# Output file selection
tk.Label(root, text="Save CSV As:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=output_csv_path, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_csv).grid(row=1, column=2, padx=10, pady=5)

# Decode button
tk.Button(root, text="Decode", command=decode_file, bg="green", fg="white").grid(row=2, column=0, columnspan=3, pady=20)

# Run the application
root.mainloop()
