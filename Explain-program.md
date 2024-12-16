# Detailed Explanation: Filter and Compute LIDAR Data

This process involves multiple steps to prepare, clean, and compute meaningful LIDAR data from the raw input. Here’s the detailed breakdown:

## Step 1: Combine Data from Multiple Files
- **Purpose**: Aggregate data from multiple CSV files into a single dataset for analysis.
- **How**:
  - Read all the CSV files from the specified folder using `pandas.read_csv()` while skipping the first 4 rows (which likely contain metadata).
  - Extract only the `Time` and `Ampl` columns, as they are essential for LIDAR computations.
  - Drop any rows with missing values to ensure data integrity.
  - Append the cleaned data from all files into a list.

## Step 2: Check Row Consistency
- **Purpose**: Ensure all CSV files have the same number of rows for compatibility.
- **How**:
  - Count the number of rows in each file.
  - If any file has a different number of rows, raise an error to alert the user and stop further processing.

## Step 3: Combine Data by Index
- **Purpose**: Create a unified dataset by merging rows across files.
- **How**:
  - Use `pandas.concat()` to merge the data.
  - Use `groupby(level=0).median()` to compute the median value for each row across all files. This step reduces noise and increases reliability.

## Step 4: Filter Amplification Values
- **Purpose**: Prepare the amplification values for further calculations.
- **How**:
  - Multiply the `Ampl` column by `-1` to invert the signal values, as required by the computation logic.

## Step 5: Compute Distance (m)
- **Purpose**: Calculate the physical distance of the LIDAR reflection based on the time-of-flight of the signal.
- **How**:
  - Use the formula: 
    ```
    Distance (m) = (Time (s) * c) / 2
    ```
    where `c` is the speed of light (`3 × 10^8 m/s`).
  - Divide by 2 to account for the round trip of the signal (to the target and back).

## Step 6: Compute Digitizer Signal (v × m²)
- **Purpose**: Calculate the LIDAR signal's digitizer value, scaled by the square of the distance.
- **How**:
  - Use the formula:
    ```
    Digitizer Signal (v × m²) = Ampl × (Distance (m)^2)
    ```

## Step 7: Filter Outliers
- **Purpose**: Remove noisy or invalid data points to improve the reliability of the results.
- **How**:
  - Apply a custom outlier removal function (`filter_outliers()`).
  - This step can include techniques such as thresholding, Z-score filtering, or interquartile range (IQR) checks.

## Step 8: Return the Cleaned Data
- **Output**: Return the processed and cleaned dataset, which includes:
  - `Time` (original timestamps)
  - `Ampl` (corrected amplification values)
  - `Distance (m)` (calculated distances)
  - `Digitizer Signal (v × m²)` (computed signal values)

This dataset is now ready for plotting and visualization in subsequent steps of the program.
