import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from s3conn import download_files
from datetime import datetime

def start_download():
    result_label.config(text="Downloading...")
    download_files(
        start_date_cal.get_date().strftime('%Y/%m/%d'),
        end_date_cal.get_date().strftime('%Y/%m/%d'),
        minute_increment_entry.get(),
        seconds_var.get()
    )
    result_label.config(text="Download completed.")

root = tk.Tk()
root.title("Predictions Retriever")

style = ttk.Style(root)
style.theme_use('clam')

date_range_label = tk.Label(root, text="Select Date Range:")
date_range_label.pack()

# Initialize the calendar to the current date
current_date = datetime.now().date()
start_date_cal = Calendar(root, selectmode='day', date_pattern='yyyy/mm/dd', 
                          year=current_date.year, month=current_date.month, day=current_date.day,
                          borderwidth=0.5, background='b'
                          )
start_date_cal.pack()

end_date_cal = Calendar(root, selectmode='day', date_pattern='yyyy/mm/dd', 
                        year=current_date.year, month=current_date.month, day=current_date.day,
                        borderwidth=0.5, background='b'
                        )
end_date_cal.pack()

minute_increment_label = tk.Label(root, text="Minute Increment:")
minute_increment_label.pack()

minute_increment_entry = tk.Entry(root, width=5)
minute_increment_entry.pack()

seconds_label = tk.Label(root, text="Second Increment:")
seconds_label.pack()

seconds_options = [str(i) for i in range(0, 61, 10)]
seconds_var = tk.StringVar(value=seconds_options[0])
seconds_menu = tk.OptionMenu(root, seconds_var, *seconds_options)
seconds_menu.pack()

download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()