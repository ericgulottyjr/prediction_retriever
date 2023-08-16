import os
import pandas as pd
import json
import gzip
from datetime import datetime

# Specify the base directory
base_directory = 'temp'

# Ask the user for a list of stop IDs
stops = input("Enter a list of space separated stop IDs: ")
stop_list = list(stops.split(" "))

# Initialize the dataframes dictionary to store DataFrames for each date
dataframes = {}

# Iterate through the year, month, and day directories under the temp directory
for year in os.listdir(base_directory):
    year_directory = os.path.join(base_directory, year)
    if os.path.isdir(year_directory):
        for month in os.listdir(year_directory):
            month_directory = os.path.join(year_directory, month)
            if os.path.isdir(month_directory):
                for day in os.listdir(month_directory):
                    day_directory = os.path.join(month_directory, day)
                    if os.path.isdir(day_directory):
                        # Iterate through .gz files in each date directory, extract JSON content, and parse it
                        for root, dirs, files in os.walk(day_directory):
                            for file_name in files:
                                if file_name.endswith('.gz'):
                                    file_path = os.path.join(day_directory, file_name)
                                    with gzip.open(file_path, 'rb') as gz_file:
                                        json_content = gz_file.read()
                                        json_data = json.loads(json_content)
                                        
                                        # Check if the key "entity" exists in the JSON data
                                        if 'entity' in json_data:
                                            entities = json_data['entity']
                                            for entity in entities:
                                                if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
                                                    stop_time_updates = entity['trip_update']['stop_time_update']
                                                    for stop_update in stop_time_updates:
                                                        if 'departure' in stop_update and 'stop_id' in stop_update:
                                                            stop_id = stop_update['stop_id']
                                                            if stop_id in stop_list:
                                                                departure_time = stop_update['departure']['time']
                                                                current_time = file_name.split('_')[0].split('T')[1].replace('Z','').replace('/', ':')
                                                                datetime_str = f"{year}-{month}-{day} {current_time}"
                                                                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

                                                                # Initialize DataFrames and append rows based on the extracted data
                                                                dataframe_name = f"{year}{month}{day}"
                                                                if dataframe_name not in dataframes:
                                                                    dataframes[dataframe_name] = pd.DataFrame(columns=['id', 'stop_id', 'current_time', 'departure_time'])
                                                                dataframes[dataframe_name] = pd.concat([
                                                                    dataframes[dataframe_name],
                                                                    pd.DataFrame({'id': [entity['id']],
                                                                                  'stop_id': [stop_id],
                                                                                  'current_time': [datetime_obj],
                                                                                  'departure_time': [departure_time]})],
                                                                    ignore_index=True
                                                                )

# Save each DataFrame as a CSV file
agg_csvs_directory = os.path.join(base_directory, 'agg_csvs')
os.makedirs(agg_csvs_directory, exist_ok=True)
for dataframe_name, df in dataframes.items():
    csv_file_path = os.path.join(agg_csvs_directory, f"{dataframe_name}.csv")
    df.to_csv(csv_file_path, index=False)
    print(f"Saved DataFrame {dataframe_name} to {csv_file_path}")

# Print the content of each DataFrame for verification
for dataframe_name, df in dataframes.items():
    print(f"DataFrame for {dataframe_name}:")
    print(df)
    print()