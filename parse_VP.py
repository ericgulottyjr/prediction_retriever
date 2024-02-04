import os
import json
import gzip
from datetime import datetime, timedelta
from collections import defaultdict

def parse_vehicle_positions(stop_ids, base_directory='temp', output_directory='temp/agg_json'):
    aggregated_data = defaultdict(list)

    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            if file_name.endswith('.gz'):
                file_path = os.path.join(root, file_name)
                with gzip.open(file_path, 'rb') as gz_file:
                    json_content = gz_file.read()
                    json_data = json.loads(json_content)

                    if 'entity' in json_data:
                        entities = json_data['entity']
                        for entity in entities:
                            if 'vehicle' in entity:
                                vehicle_data = entity['vehicle']
                                stop_id = vehicle_data.get('stop_id', None)
                                if stop_id is not None:
                                    # Ensure stop_id is numeric
                                    try:
                                        stop_id = str(stop_id)
                                    except ValueError:
                                        continue

                                    # Get timestamp and convert to datetime
                                    timestamp = vehicle_data.get('timestamp', None)
                                    if timestamp is not None:
                                        try:
                                            timestamp = datetime.fromtimestamp(int(timestamp))
                                        except ValueError:
                                            timestamp = None

                                    if stop_id in stop_ids:
                                        # Include all fields from the original event
                                        entry = {
                                            'stop_id': stop_id,
                                            'timestamp': timestamp,
                                            'vehicle_data': vehicle_data
                                        }
                                        # Group entries by day
                                        day_key = timestamp.strftime('%Y%m%d')
                                        aggregated_data[day_key].append(entry)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Save the aggregated data to JSON files, one for each day
    for day_key, entries in aggregated_data.items():
        output_file_path = os.path.join(output_directory, f"{day_key}.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(entries, json_file, default=str, indent=4)

    print(f"Aggregated data saved to {output_directory}")

if __name__ == "__main__":
    # Example stop_ids list, replace with your actual list of stop_ids
    stop_ids = ['70106', '70107', '70237', '70238', '70160', '70161', '70503', '70504', '70511', '70512', '70174', '70175']
    parse_vehicle_positions(stop_ids)