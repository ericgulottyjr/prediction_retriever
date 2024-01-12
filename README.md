# prediction_retriever
Allows for the batch download of GTFS-realtime files from the `mbta-gtfs-s3` bucket.

## Setup
Must have the `boto3` library installed locally with active AWS keys.

## Usage
- GUI allows user to set specific date range and minute, second increments between timestamps when downloading files.
- `stop_id` input pop-up allows user to input specific `stop_id` values for the script to process.
- The script returns a processed `.csv` file with 4 columns:
  - `prediction_id` (`id`)
  - `stop_id`
  - `current_time`: timestamp given by the downloaded `.gz` file 
  - `departure_time`: next departure time for the `stop_id`
