import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

def get_selected_date():
    selected_date = cal.selection_get()
    label.config(text=f"Selected Date: {selected_date}")

# Create main window
root = tk.Tk()
root.title("Calendar GUI")

# Create a DateEntry widget
cal = Calendar(root, selectmode="day", year=2023, month=12, day=22)
cal.pack(padx=10, pady=10)

# Create a button to get the selected date
get_date_button = tk.Button(root, text="Get Selected Date", command=get_selected_date)
get_date_button.pack(pady=10)

# Create a label to display the selected date
label = tk.Label(root, text="Selected Date: ")
label.pack(pady=10)

# Run the main loop
root.mainloop()
