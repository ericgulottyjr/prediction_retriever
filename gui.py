import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from s3conn import download_files
from datetime import datetime
import parse_TU, parse_VP

# Global variable to store stop IDs
entered_stop_ids = []

def start_download():
    result_label.config(text="Downloading...")
    
    # Retrieve the dates and other data
    start_date_str = start_date_cal.get_date()
    end_date_str = end_date_cal.get_date()
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    end_date = datetime.strptime(end_date_str, '%Y/%m/%d')
    
    # Call download function with user selections
    selected_types = []
    if trip_updates_var.get():
        selected_types.append('realtime_TripUpdates_enhanced')
    if vehicle_positions_var.get():
        selected_types.append('realtime_VehiclePositions_enhanced')

    # Ensure at least one type is selected before proceeding
    if not selected_types:
        result_label.config(text="Please select at least one file type to download.")
    else:
        # Call parse function if stop IDs are entered and the parse option is selected
        if parse_var.get() and entered_stop_ids:
            result_label.config(text="Downloading and Parsing...")
        else:
            result_label.config(text="Downloading...")

        for file_type in selected_types:
            download_files(
                start_date.strftime('%Y/%m/%d'),
                end_date.strftime('%Y/%m/%d'),
                minute_increment_entry.get(),
                seconds_var.get(),
                file_type  # Pass the selected file type to s3conn.py
            )

        if parse_var.get() and entered_stop_ids:
            if 'realtime_TripUpdates_enhanced' in selected_types:
                parse_TU.parse_trip_updates(entered_stop_ids)
            if 'realtime_VehiclePositions_enhanced' in selected_types:
                parse_VP.parse_vehicle_positions(entered_stop_ids)
            result_label.config(text="Download/parse complete.")
        else:
            result_label.config(text="Download complete.")


def save_stop_ids():
    global entered_stop_ids
    entered_stop_ids.extend(stop_ids_entry.get().split())
    stop_ids_window.destroy()

def open_stop_ids_window():
    global stop_ids_entry, stop_ids_window
    stop_ids_window = tk.Toplevel(root)
    stop_ids_window.title("Enter Stop IDs")

    tk.Label(stop_ids_window, text="Enter space separated stop IDs:").pack()

    stop_ids_entry = tk.Entry(stop_ids_window)
    stop_ids_entry.pack()

    tk.Button(stop_ids_window, text="OK", command=save_stop_ids).pack()

def toggle_entry():
    if parse_var.get():
        open_stop_ids_window()

root = tk.Tk()
root.title("Predictions Retriever")

# Styling
style = ttk.Style(root)
style.theme_use('clam')

# Start Date Picker
start_date_label = tk.Label(root, text="Choose Start Date:")
start_date_label.pack()
current_date = datetime.now().date()
start_date_cal = Calendar(root, selectmode='day', date_pattern='yyyy/mm/dd', year=current_date.year, month=current_date.month, day=current_date.day)
start_date_cal.pack()

# End Date Picker
end_date_label = tk.Label(root, text="Choose End Date:")
end_date_label.pack()
end_date_cal = Calendar(root, selectmode='day', date_pattern='yyyy/mm/dd', year=current_date.year, month=current_date.month, day=current_date.day)
end_date_cal.pack()

# Checkbox variables to track user selections
trip_updates_var = tk.BooleanVar()
vehicle_positions_var = tk.BooleanVar()

# Checkbox widgets for 'realtime TripUpdates' and 'realtime VehiclePositions'
trip_updates_checkbox = tk.Checkbutton(root, text="Download realtime TripUpdates", variable=trip_updates_var)
vehicle_positions_checkbox = tk.Checkbutton(root, text="Download realtime VehiclePositions", variable=vehicle_positions_var)
trip_updates_checkbox.pack()
vehicle_positions_checkbox.pack()

# Minute Increment Input
minute_increment_label = tk.Label(root, text="Minute Increment:")
minute_increment_label.pack()
minute_increment_entry = tk.Entry(root, width=5)
minute_increment_entry.pack()

# Second Increment Input
seconds_label = tk.Label(root, text="Second Increment:")
seconds_label.pack()
seconds_options = [str(i) for i in range(0, 31, 10)]
seconds_var = tk.StringVar(value=seconds_options[0])
seconds_menu = tk.OptionMenu(root, seconds_var, *seconds_options)
seconds_menu.pack()

# Parse Option
parse_var = tk.BooleanVar()
parse_checkbox = tk.Checkbutton(root, text="Parse?", variable=parse_var, command=toggle_entry)
parse_checkbox.pack()

# Start Download Button
download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()

# Result Label
result_label = tk.Label(root, text="")
result_label.pack()

root.geometry("")
root.mainloop()