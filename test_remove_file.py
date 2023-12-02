import tkinter as tk
from tkinter import *

def insert_image():
    global img
    global mail_entry
    # Create a PhotoImage object
    img = PhotoImage(file="D:/Picture1.png")  # Change the path and file format if needed

    # Get the dimensions of the image
    img_width = img.width()
    img_height = img.height()

    # Define the maximum width for the image
    max_width = 600  # Change this value to your desired maximum width

    # Calculate the scale factor based on the maximum width
    scale_factor = max_width / img_width

    # Calculate the new dimensions while preserving the aspect ratio
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)

    # Resize the image using the zoom method
    img = img.subsample(int(img_width / new_width), int(img_height / new_height))

    # Insert the image into the Text widget
    mail_entry.image_create(END, image=img)

# Create the main window
window = tk.Tk()
window.title("Insert Image Example")

# Create a Text widget
mail_entry = tk.Text(window, wrap="word", width=100, height=50)
mail_entry.pack(pady=10)

# Create a button to insert an image
insert_button = tk.Button(window, text="Insert Image", command=insert_image)
insert_button.pack(pady=5)



# Start the Tkinter event loop
window.mainloop()
