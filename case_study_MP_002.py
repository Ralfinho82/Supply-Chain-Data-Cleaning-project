import pandas as pd
import numpy as np

# Display all columns
pd.set_option("display.max_columns", None)

# Paths to the CSV-files
data_sample_path = "data_sample_AufgDataScience_Case.csv"
event_locations_path = "event_locations_DataScience_Case.csv"

# Read the files into Pandas Dataframes
data_sample = pd.read_csv(data_sample_path, sep=";")
event_locations = pd.read_csv(event_locations_path, sep=";")

# Show first five rows to check contents of Dataframes
print(data_sample.head())
print(event_locations.head())

# Count and drop duplicate entries
data_sample_duplicates = data_sample.duplicated().sum()
print("Count of double rows: ", data_sample_duplicates)

row_count_original_df = len(data_sample)
print("The original dataframe has", row_count_original_df, "rows.")

data_sample_no_duplicates = data_sample.drop_duplicates(keep=False)
row_count_no_duplicates_df = len(data_sample_no_duplicates)
print("The dataframe without duplicates has", row_count_no_duplicates_df, "rows.")


# Analyse missing values
data_sample_count = data_sample_no_duplicates.isnull().sum()
percent_missing = round(((data_sample_count.sum() / np.prod(data_sample_no_duplicates.shape)) * 100), 2)
# Counting and printing the amount of missing values
print("Count of missing values", "\n", data_sample_count)
# Printing the percentage of missing values
print("Percent of missing data:", percent_missing)


# Deal with cryptic codes in columns "Description" and "PortofDischarge"
# Merge Dataframes on column "EventLocation" and drop column "EventLocation"
merged_data = pd.merge(data_sample_no_duplicates, event_locations, on="EventLocation", how="left")
merged_data = merged_data.drop(columns=["EventLocation"])
# Rename column "Bezeichnung" to "Description"
merged_data.rename(columns={"Bezeichnung": "Description"}, inplace=True)

# Replace values in column "PortofDischarge" with the corresponding location names
merged_data["PortofDischarge"] = merged_data["PortofDischarge"].replace({
    "urn:jaif:id:loc:26LUSCHS": "Hafen Charleston",
    "urn:jaif:id:loc:26LUSSAV": "Bahnterminal Savannah",
    "urn:jaif:id:loc:26LMXATM": "Hafen Altamira"
})
# Assigning datatype "str" to "PortofDischarge"
merged_data["PortofDischarge"] = merged_data["PortofDischarge"].astype(str)
# Replace empty values and Whitespace in column PortofDischarge with NaN
merged_data["PortofDischarge"].replace("", np.nan, inplace=True)
merged_data["PortofDischarge"].replace(" ", np.nan, inplace=True)  

# Show first five rows to check content of the Dataframe
print(merged_data.head())


# Deal with unreadable values in column date columns
# Check if "#" is part of the three date columns and remove rows with this sign
# Regular expression that checks for value "#"
regular_expression_pattern = "#"

# Check in each of the three columns and remove the rows with "#" characters
for column in ["PoCreationDate", "EventTime", "EventMessageTime"]:
    if column in merged_data.columns:
        contains_invalid_chars = merged_data[column].astype(str).str.contains(regular_expression_pattern)
        if contains_invalid_chars.any():
            print(f"Invalid characters found in column {column}. Remove affected lines.")
            merged_data = merged_data[~contains_invalid_chars]
        else:
            print(f"No invalid characters in column {column}")
    else:
        print(f"Column {column} does not exist in the DataFrame.")

print(f"Number of lines after removal:{len(merged_data)}")


# Deal with empty values of column ShipmentQuantity - Exploration reveals, all empty values can be linked to Material value "A2560107300"
# Calculate the mean of "ShipmentQuantity" for "A2560107300", excluding NaN values in the calculation
mean_shipment_quantity = merged_data.loc[merged_data["Material"] == "A2560107300", "ShipmentQuantity"].mean()

# Round the mean to the nearest integer if it is a valid number
mean_shipment_quantity = round(mean_shipment_quantity)

# Replace NaN values in "ShipmentQuantity" for "A2560107300" with the mean
merged_data.loc[(merged_data["Material"] == "A2560107300") & (merged_data["ShipmentQuantity"].isna()), "ShipmentQuantity"] = mean_shipment_quantity
print("Replaced NaN values in 'ShipmentQuantity' for 'A2560107300' with:", mean_shipment_quantity)


# Deal with value "urn:jaif:id:loc:25LUN498999044W013" whis is most likely a typo in column EventLocation. Replace with "Werk Tuscaloosa"
merged_data["Description"] = merged_data["Description"].replace("urn:jaif:id:loc:25LUN498999044W013", "Werk Tuscaloosa")
# Check the changes
print(merged_data["Description"])


# Set schema of the Dataframe columns for further quality processing
merged_data["PoCreationDate"] = pd.to_datetime(merged_data["PoCreationDate"], format="%d.%m.%Y %H:%M", errors='coerce')
merged_data["EventTime"] = pd.to_datetime(merged_data["EventTime"], format="%d.%m.%Y %H:%M", errors='coerce')
merged_data["EventMessageTime"] = pd.to_datetime(merged_data["EventMessageTime"], format="%d.%m.%Y %H:%M", errors='coerce')
merged_data["ContainerNumber"] = merged_data["ContainerNumber"].astype(str)
merged_data["VesselName"] = merged_data["VesselName"].astype(str)
merged_data["ShipmentNumber"] = merged_data["ShipmentNumber"].astype(int)
merged_data["ShipmentQuantity"] = merged_data["ShipmentQuantity"].astype(int)
merged_data["Material"] = merged_data["Material"].astype(str)
merged_data["Controller"] = merged_data["Controller"].astype(str)
merged_data["EventName"] = merged_data["EventName"].astype(str)
merged_data["Description"] = merged_data["Description"].astype(str)


# Deal with empty values for Time2Arrival - calculate the number
# Sort the Dataframe based on "ShipmentNumber" and "EventTime" to ensure the events are in chronological order
merged_data.sort_values(by=["ShipmentNumber", "EventTime"], inplace=True)

# Calculate "Time2Arrival" as the number of days from the first event for each "ShipmentNumber" to the "Goods Receipt Dock" event
def calculate_time_to_arrival(df):
    # Calculate the time difference in days from the first event for each "ShipmentNumber"
    first_event_times = df.groupby("ShipmentNumber")["EventTime"].transform("min")
    df["Time2Arrival"] = (df["EventTime"] - first_event_times).dt.days
    return df

# Apply the function to the DataFrame
merged_data = calculate_time_to_arrival(merged_data)

# Ensure "Time2Arrival" is of type int
merged_data["Time2Arrival"] = merged_data["Time2Arrival"].astype(int)


# Replace German with English in "PortofDischarge" and "Description" columns
merged_data["PortofDischarge"] = merged_data["PortofDischarge"].str.replace("Hafen", "Port")
merged_data["Description"] = merged_data["Description"].str.replace("Hafen", "Port")
merged_data["PortofDischarge"] = merged_data["PortofDischarge"].str.replace("Werk", "Plant")
merged_data["Description"] = merged_data["Description"].str.replace("Werk", "Plant")


# Analyse final data quality with final dataframe
data_sample_count = merged_data.isnull().sum()
percent_missing = round(((data_sample_count.sum() / np.prod(merged_data.shape)) * 100), 2)
# Counting and printing the amount of missing values
print("Count of missing values", "\n", data_sample_count)
# Printing the percentage of missing values
print("Percent of missing data:", percent_missing)


# Export the final Data Frame into a CSV-file for further processing
merged_data.to_csv("exported_data_clean.csv", index=False, sep=";")
