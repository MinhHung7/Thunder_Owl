import tkinter as tk
from PIL import Image, ImageTk

def toggle_additional_buttons():
    if button4.winfo_ismapped():
        button4.pack_forget()
        button5.pack_forget()
    else:
        button4.pack()
        button5.pack()

# Create the main window
root = tk.Tk()
root.title("Button Example")

# Load images for icons (replace these paths with your own image paths)
icon_path = "D:\FILE SOCKET PYTHON\Icons\mail.png"
button4_icon = ImageTk.PhotoImage(Image.open(icon_path))

# Create buttons 1, 2, and 3
button1 = tk.Button(root, text="Button 1")
button1.pack()

button2 = tk.Button(root, text="Button 2", command=toggle_additional_buttons)
button2.pack()

button3 = tk.Button(root, text="Button 3")
button3.pack()

# Create buttons 4 and 5 with icons but initially hide them
button4 = tk.Button(root, text="Button 4", image=button4_icon, compound=tk.LEFT)
button4.pack_forget()

button5 = tk.Button(root, text="Button 5", image=button4_icon, compound=tk.LEFT)
button5.pack_forget()

# Start the Tkinter event loop
root.mainloop()
