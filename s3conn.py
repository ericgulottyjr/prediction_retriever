import boto3
import os
from datetime import datetime, timedelta

# Initialize the S3 client
s3_client = boto3.client('s3')

# Specify 
bucket_name = 'mbta-gtfs-s3'

# Define a function to list objects under a specific prefix using Boto3's Paginator
def list_objects_with_prefix(prefix):
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    objects = []
    for page in pages:
        objects.extend(page.get('Contents', []))
    return objects

def download_files(start_date_str, end_date_str, minute_increment_str, second_increment_str, file_type):
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    end_date = datetime.strptime(end_date_str, '%Y/%m/%d')
    
    # Convert minute and second increments to integers
    try:
        minute_increment = int(minute_increment_str)
    except ValueError:
        minute_increment = 1
    
    try:
        second_increment = int(second_increment_str)
    except ValueError:
        second_increment = 0
    
    current_date = start_date
    while current_date <= end_date:
        prefix = current_date.strftime('%Y/%m/%d/')
        objects = list_objects_with_prefix(prefix)

        for hour in range(24):
            for minute in range(0, 60, minute_increment):
                if second_increment == 0:
                    # Compare only up to the minute level
                    hh_mm_ss = f"{hour:02d}:{minute:02d}"
                    
                    for obj in objects:
                        file_key = obj['Key']
                        
                        if (file_type in file_key) and (hh_mm_ss == file_key.split('_')[0][-9:-4]):
                            print(f"Found: {file_key}")
                            
                            target_dir = os.path.join('temp', prefix)
                            os.makedirs(target_dir, exist_ok=True)
                            
                            file_name = os.path.basename(file_key)
                            local_file_path = os.path.join(target_dir, file_name)
                            s3_client.download_file(bucket_name, file_key, local_file_path)
                            
                            print(f"Downloaded: {file_key} -> {local_file_path}")
                            break
                else:
                    # Compare up to the second level
                    for second in range(0, 60, second_increment):
                        hh_mm_ss = f"{hour:02d}:{minute:02d}:{second:02d}"

                        for obj in objects:
                            file_key = obj['Key']
                            
                            if (file_type in file_key) and (hh_mm_ss == file_key.split('_')[0][-9:-2]+'0'):
                                print(f"Found: {file_key}")

                                target_dir = os.path.join('temp', prefix)
                                os.makedirs(target_dir, exist_ok=True)
                                
                                file_name = os.path.basename(file_key)
                                local_file_path = os.path.join(target_dir, file_name)
                                s3_client.download_file(bucket_name, file_key, local_file_path)
                                
                                print(f"Downloaded: {file_key} -> {local_file_path}")
                                break
                            
        current_date += timedelta(days=1)