import tkinter as tk
import customtkinter
from customtkinter import *

# Create the main Tkinter window
root = tk.Tk()
root.title("Scrollable Frame Example")

# Create a frame to contain the scrollable frame
detailMailListFolderFrame = tk.Frame(root)
detailMailListFolderFrame.pack(fill=tk.BOTH, expand=True)

# Create the CtkScrollableFrame
file_frame = CTkScrollableFrame(
    master=detailMailListFolderFrame,
    fg_color="#3F3F46",
    height=40,
    orientation="horizontal"
)

# Add widgets to the scrollable frame
for i in range(20):
    label = tk.Label(file_frame, text=f"Label {i}")
    label.pack(side=tk.LEFT, padx=5)

# Pack the scrollable frame
file_frame.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter main loop
root.mainloop()