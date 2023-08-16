import tkinter as tk
from s3conn import download_files

def start_download():
    result_label.config(text="Downloading...")
    download_files(
        start_date_entry.get(),
        end_date_entry.get(),
        minute_increment_entry.get(),
        seconds_var.get()
    )
    result_label.config(text="Download completed.")

root = tk.Tk()
root.title("Predictions Retriever")

date_range_label = tk.Label(root, text="Date Range (YYYY/MM/DD - YYYY/MM/DD):")
date_range_label.pack()

start_date_entry = tk.Entry(root)
start_date_entry.pack()

end_date_entry = tk.Entry(root)
end_date_entry.pack()

minute_increment_label = tk.Label(root, text="Minute Increment:")
minute_increment_label.pack()

minute_increment_entry = tk.Entry(root)
minute_increment_entry.pack()

seconds_label = tk.Label(root, text="Second Increment:")
seconds_label.pack()

seconds_options = [str(i) for i in range(1, 61)]
seconds_var = tk.StringVar(value=seconds_options[0])
seconds_menu = tk.OptionMenu(root, seconds_var, *seconds_options)
seconds_menu.pack()

download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()