import boto3
import os
from datetime import datetime, timedelta

# Initialize the S3 client
s3_client = boto3.client('s3')

# Specify your bucket name
bucket_name = 'mbta-gtfs-s3'

# Get user input for start and end dates
start_date_str = input("Enter start date (YYYY/MM/DD): ")
end_date_str = input("Enter end date (YYYY/MM/DD): ")

start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
end_date = datetime.strptime(end_date_str, '%Y/%m/%d')

# Define a function to list objects under a specific prefix using Boto3's Paginator
def list_objects_with_prefix(prefix):
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    objects = []
    for page in pages:
        objects.extend(page.get('Contents', []))
    return objects

# Iterate through each minute within the specified date range
current_date = start_date
while current_date <= end_date:
    prefix = current_date.strftime('%Y/%m/%d/')
    objects = list_objects_with_prefix(prefix)

    for hour in range(24):
        for minute in range(0, 60, 1):  # Change the step to control the frequency (e.g., every minute)
            hh_mm = f"{hour:02d}:{minute:02d}"
            
            for obj in objects:
                file_key = obj['Key']
                
                if 'realtime_TripUpdates_enhanced' in file_key and hh_mm == file_key.split('_')[0][-9:-4]:
                    print(f"Found: {file_key}")
                    
                    # Create the target directory based on the prefix
                    target_dir = os.path.join('temp', prefix)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Download the file
                    file_name = os.path.basename(file_key)
                    local_file_path = os.path.join(target_dir, file_name)
                    s3_client.download_file(bucket_name, file_key, local_file_path)
                    
                    print(f"Downloaded: {file_key} -> {local_file_path}")
                    break  # Stop searching for files in this minute
            
    current_date += timedelta(days=1)