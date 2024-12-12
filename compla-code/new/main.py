# main.py
import json
import os
from plot_library import plot_lidar_data
from lidar_processor import process_files

def main():
    print("Welcome to LIDAR Signal Analyzer!")
    print("Please provide the folder path containing CSV files.")

    json_file_path = 'compla-code/ALiN_202404032035.json'
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
