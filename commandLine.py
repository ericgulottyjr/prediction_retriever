from datetime import datetime
from s3conn import download_files
import parse

def main():
    # Parse the initial input
    initial_input = input("Enter start_date (YYYY/MM/DD), end_date (YYYY/MM/DD), minute increment (up to 60), second increment: ")
    # Handle spaces after commas
    params = [param.strip() for param in initial_input.split(',')]
    
    if len(params) != 4:
        print("Invalid input format. Please use the format: YYYY/MM/DD,YYYY/MM/DD,XX,XX")
        return

    try:
        # Convert dates to datetime objects
        start_date = datetime.strptime(params[0], '%Y/%m/%d')
        end_date = datetime.strptime(params[1], '%Y/%m/%d')
        # Get minute and second increments
        min_increment = params[2]
        sec_increment = params[3]
    except ValueError as e:
        print(f"Invalid date format or increments: {e}")
        return

    # Perform the download
    download_files(
        start_date.strftime('%Y/%m/%d'),
        end_date.strftime('%Y/%m/%d'),
        min_increment,
        sec_increment
    )

    # Ask if the user wants to parse
    parse_input = input("Do you want to parse the downloaded files? (y/n): ").lower()
    if parse_input == 'y':
        stop_ids_input = input("Enter a list of comma-separated stop_ids: ")
        stop_ids = [id.strip() for id in stop_ids_input.split(',')]
        parse.parse_stops(stop_ids)
    elif parse_input != 'n':
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()