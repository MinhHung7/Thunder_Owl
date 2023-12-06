import tkinter as tk
from PIL import Image, ImageTk

def on_text_click(event):
    cursor_index = text_widget.index(tk.CURRENT)
    print("Cursor Index:", cursor_index)

def insert_image(text_widget, image_path, index):
    # Open the image using Pillow (PIL)
    img = Image.open(image_path)

    # Convert the image to Tkinter PhotoImage
    img_tk = ImageTk.PhotoImage(img)

    # Insert an invisible (zero width and height) label with the image
    label = tk.Label(text_widget, image=img_tk)
    label.image = img_tk  # Keep a reference to prevent garbage collection
    text_widget.window_create(index, window=label)

# Create the main Tkinter window
root = tk.Tk()
root.title("Insert Image into Text")

# Create a Text widget
text_widget = tk.Text(root, wrap=tk.WORD, width=240, height=100)
text_widget.pack()

# Insert some text
text_widget.insert(tk.END, "This is some text.\n")

# Insert an image at the beginning of the text
insert_image(text_widget, "D:/butterfly.gif", "1.2")
insert_image(text_widget, "D:/butterfly.gif", "1.6")

text_widget.bind("<Button-1>", on_text_click)

# Start the Tkinter event loop
root.mainloop()
