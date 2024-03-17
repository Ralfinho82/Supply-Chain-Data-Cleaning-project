# Supply Chain Data Cleaning and Analysis

This repository contains an IPython notebook documenting the process of cleaning and analyzing supply chain data using Python libraries such as Pandas and NumPy. The dataset consists of two CSV files: `data_sample_AufgDataScience_Case.csv` and `event_locations_DataScience_Case.csv`.

## Project Overview

The notebook contains the following sections:

### 1. Import Libraries and Set Display Options
- Imports necessary libraries and sets display options for Pandas.

### 2. Define Paths and Read Data
- Defines paths to the CSV files and reads them into Pandas DataFrames.

### 3. Initial Examination of the Data
- Displays the first five rows of each DataFrame to check the contents.

### 4. Count and Drop Duplicate Entries
- Counts and drops duplicate entries from the `data_sample` DataFrame.

### 5. Analyze Missing Values
- Analyzes missing values in the `data_sample` DataFrame.

### 6. Merge DataFrames and Clean Up Columns
- Merges DataFrames on the "EventLocation" column and cleans up column names.

### 7. Deal with Cryptic Codes in Columns
- Replaces cryptic codes in the "PortofDischarge" column with corresponding location names.

### 8. Display the Updated DataFrame
- Displays the updated DataFrame after merging and cleanup.

### 9. Cleanup Date Columns
- Deals with corrupted data in date columns by removing rows with unreadable values.

### 10. Deal with Missing Values in "ShipmentQuantity"
- Handles missing values in the "ShipmentQuantity" column by replacing NaN values with the mean.

### 11. Additional Data Cleanup and Type Assignment
- Converts columns to appropriate data types.

### 12. Deal with Cryptic Codes in Column "EventLocation"
- Replaces a specific cryptic code in the "EventLocation" column.

### 13. Calculate Values for Column "Time2Arrival"
- Calculates values for the "Time2Arrival" column.

### 14. Replace German Expressions with English Expressions
- Replaces German expressions with English expressions in specific columns.

### 15. Final Data Quality Analysis and Exporting the DataFrame to CSV
- Performs a final data quality analysis and exports the cleaned DataFrame to a CSV file.

## Conclusion

This notebook provides a comprehensive guide to cleaning and analyzing supply chain data, ensuring data quality and preparing it for further analysis.

For more details, refer to the [Jupyter Notebook](notebook.ipynb) in this repository.

