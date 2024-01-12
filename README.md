# prediction_retriever
Allows for the batch download of GTFS-realtime files from the `mbta-gtfs-s3` bucket.

## Setup
Must have the `boto3` Python library installed locally with active AWS keys.

Download repo, `cd` to folder and use `python3 script_name.py` command to open either `gui.py` or `commandLine.py`.

## Usage
- GUI allows user to set specific date range and minute, second increments between timestamps when downloading files.
- `commandLine` provides an alternative for users who don't want to interact with the GUI.
- `stop_id` input pop-up allows user to input specific `stop_id` values for the script to process.
- The script returns a processed `.csv` file with 6 columns:
  - `prediction_id` (`id`)
  - `stop_id`
  - `file_timestamp`: timestamp given by the downloaded `.gz` file 
  - `departure_time`: next departure time for the `stop_id`
  - `current_time`: timezone-adjusted file timestamp
  - `departure_time_adj`: timezone-adjusted departure time
