# lidar_processor.py
import os
import pandas as pd
from tqdm import tqdm

def filter_outliers(data):
    # Add your logic for filtering outliers here
    return data

def process_files(folder_path):
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    file_data = []
    for file_path in tqdm(csv_files, desc="Processing files", unit="file"):
        try:
            data = pd.read_csv(file_path, skiprows=4)
            if not {'Time', 'Ampl'}.issubset(data.columns):
                print(f"File {file_path} does not contain 'Time' and 'Ampl' columns. Skipping...")
                continue

            data = data[['Time', 'Ampl']].dropna()
            file_data.append(data)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    row_counts = [len(data) for data in file_data]
    if len(set(row_counts)) != 1:
        raise ValueError("All files must have the same number of rows.")

    combined_data = pd.concat(file_data).groupby(level=0).median()
    c = 3e8
    combined_data['Ampl'] = -combined_data['Ampl']
    combined_data['Distance (m)'] = (combined_data['Time'] * c) / 2
    combined_data['Digitizer Signal (v * m²)'] = combined_data['Ampl'] * (combined_data['Distance (m)'] ** 2)

    combined_data = filter_outliers(combined_data)
    return combined_data
