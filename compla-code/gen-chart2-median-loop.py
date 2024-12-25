import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

def plot_lidar_data(data, oc_cal, oc_dis, folder_path):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot old software (oc_cal, oc_dis)
    ax.plot(oc_cal, oc_dis, color='green', linewidth=1, label="old software")

    # Plot new software (filtered_data)
    ax.plot(data['Digitizer Signal (v * m²)'],
            data['Distance (m)'],
            color='red',
            linewidth=1,
            label="new software")

    ax.set_xlabel("Digitizer Signal (v * m²)", fontsize=12)
    ax.set_ylabel("Distance (m)", fontsize=12)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    folder_name = os.path.basename(folder_path)
    parts = folder_name.split('-')
    day = parts[1]
    month = parts[2]
    year = parts[3]
    hour = parts[5]
    minute = parts[6]

    date_str = f"{day}/{month}/{year} {hour}:{minute}"
    chart_title = f"LIDAR Signal Analyzer {date_str}"
    fig.suptitle(chart_title, fontsize=14, fontweight='bold')

    ax.legend(loc='upper right', bbox_to_anchor=(1, 1))

    plt.show()

def filter_outliers(data):
    return data

def process_files(folder_path):
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    all_time = []
    all_ampl = []

    for file_path in tqdm(csv_files, desc="Processing files", unit="file"):
        try:
            data = pd.read_csv(file_path, skiprows=4)
            if not {'Time', 'Ampl'}.issubset(data.columns):
                print(f"File {file_path} does not contain 'Time' and 'Ampl' columns. Skipping...")
                continue

            data = data[['Time', 'Ampl']].dropna()
            all_time.append(data['Time'].values)
            all_ampl.append(data['Ampl'].values)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if not all_time or not all_ampl:
        raise ValueError("No valid data found in the specified files.")

    # Calculate median
    combined_time = pd.DataFrame(all_time).median(axis=0).values
    combined_ampl = pd.DataFrame(all_ampl).median(axis=0).values

    combined_data = pd.DataFrame({'Time': combined_time, 'Ampl': combined_ampl})

    c = 3e8
    combined_data = combined_data[combined_data['Time'] > 10e-6]
    combined_data['Time'] = combined_data['Time'] - 10e-6
    combined_data['Ampl'] = -combined_data['Ampl']
    combined_data['Distance (m)'] = (combined_data['Time'] * c) / 2
    combined_data['Digitizer Signal (v * m²)'] = combined_data['Ampl'] * (combined_data['Distance (m)'] ** 2)

    combined_data = filter_outliers(combined_data)

    return combined_data

def main():
    print("Welcome to LIDAR Signal Analyzer!")
    print("Please provide the folder path containing CSV files.")

    json_file_path = 'ALiN_202404032035.json'
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    oc_cal = json_data[0]['OC_cal']
    oc_dis = json_data[0]['dis']

    folder_path = "../csv-03-04-2024-tmp4-20-00"

    if os.path.isdir(folder_path):
        try:
            data = process_files(folder_path)
            if not data.empty:
                plot_lidar_data(data, oc_cal, oc_dis, folder_path)
            else:
                print("No valid data to plot.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("The specified folder path does not exist.")

if __name__ == "__main__":
    main()
