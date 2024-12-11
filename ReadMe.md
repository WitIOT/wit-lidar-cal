# LIDAR Signal Analyzer

The `LIDAR Signal Analyzer` script is designed to process multiple CSV files containing time signal (`Time`) and signal amplitude (`Ampl`) measurements from LIDAR. It calculates the distance (`Distance`) and digitizer signal (`Digitizer Signal`), then plots the processed data for comparison with corrected data (from a JSON file).

## Features

- Reads multiple CSV files from a specified folder.
- Validates that all files contain the same number of rows.
- Calculates `Distance` and `Digitizer Signal` from `Time` and `Ampl`.
- Displays `Actual Data` and `Corrected Data` on a comparison graph.
- Filters `Actual Data` to only include `Distance >= 1000` and offsets it to start from 0 on the Y-axis.

## Input Data

1. **CSV Files**: CSV files must contain `Time` and `Ampl` columns. Files are read from the specified folder.  
   Example structure:
   ```
   Time,Ampl
   1.23e-5,0.002
   1.24e-5,0.003
   ...
   ```

   > Note: The script skips the first 4 rows (`skiprows=4`) when reading each CSV file.

2. **JSON File**: Contains corrected data (`OC_cal` and `dis`) for comparison.  
   Example structure:
   ```json
   [
     {
       "OC_cal": [value1, value2, ...],
       "dis": [distance1, distance2, ...]
     }
   ]
   ```

## Prerequisites

- Install Python 3.x.
- Install the required libraries:
  ```bash
  pip install pandas matplotlib tqdm
  ```

## Usage

1. Place the script and the JSON file in the `compla-code` folder (example structure below).
2. Create a folder containing multiple CSV files in the directory above `compl`, e.g.:
   ```
   project/
   ├─ csv-03-04-2024-tmp4-20-00/
   │  ├─ data1.csv
   │  ├─ data2.csv
   │  └─ ...
   ├─ compla-code/
   │  ├─ script.py
   │  ├─ ALiN_202404032035.json
   │  └─ ...
   ```
3. In the script (e.g., `gen-chart2-1.py`), set the `folder_path` variable to the target CSV folder, e.g., `folder_path = "../csv-03-04-2024-tmp4-20-00"`.
4. Run the script:
   ```bash
   python gen-chart2-1.py
   ```
5. The script will process the data and display a comparison graph showing `Actual Data` and `Corrected Data`.

## Example Output

- The graph will show `Actual Data` (blue) and `Corrected Data` (green).
- The `Actual Data` is filtered to only display distances greater than or equal to 1000 meters and is shifted to start from 0 on the Y-axis.

## Customization

- To modify filtering or data adjustment logic, edit the `plot_lidar_data` or `process_files` functions.
- To change the JSON file name or structure, update the `main()` function where `json_file_path` is defined.

---