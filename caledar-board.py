from tkcalendar import Calendar
import tkinter as tk
from tkinter import Frame, Button, Label

def select_date():
    my_date = mycal.get_date()
    selected_date.config(text=my_date)

# Create the main window
root = tk.Tk()
root.title("Calendar Board")
root.geometry("600x600")

# Create a frame for the calendar
frame = Frame(root)
frame.grid(row=0, column=0, sticky="w")

# Increase the font size of the calendar
mycal = Calendar(frame, setmode="day", date_pattern='d/m/yy', font="Arial 10")
mycal.pack(padx=15, pady=15)

selected_date = Label(frame, text="")
selected_date.pack(padx=2, pady=2)

open_cal = Button(frame, text="Select Date", command=select_date)
open_cal.pack(padx=15, pady=15)

# Run the main loop
root.mainloop()
