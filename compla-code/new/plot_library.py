# lidar_library.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from lidar_processor import process_files

def plot_lidar_data(data, oc_cal, oc_dis, folder_path):
    filtered_data = data[data['Distance (m)'] >= 1000].copy()

    if not filtered_data.empty:
        min_distance = filtered_data['Distance (m)'].min()
        filtered_data['Distance (m)'] -= min_distance

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(oc_cal, oc_dis, color='green', linewidth=2, label="old software")
    ax1.set_xlabel("Digitizer Signal (v * m²)", fontsize=12, color='green')
    ax1.set_ylabel("Distance (m)", fontsize=12)
    ax1.tick_params(axis='x', labelcolor='green')

    ax2 = ax1.twiny()
    ax2.plot(filtered_data['Digitizer Signal (v * m²)'], filtered_data['Distance (m)'], label="new software")
    ax2.tick_params(axis='x', labelcolor='blue')

    folder_name = os.path.basename(folder_path)
    parts = folder_name.split('-')
    day, month, year, hour, minute = parts[1], parts[2], parts[3], parts[5], parts[6]
    date_str = f"{day}/{month}/{year} {hour}:{minute}"

    chart_title = f"LIDAR Signal Analyzer {date_str}"
    fig.suptitle(chart_title, fontsize=14, fontweight='bold')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2

    ax1.legend(lines, labels, loc='upper right', bbox_to_anchor=(1, 1))

    plt.show()

def filter_outliers(data):
    return data
