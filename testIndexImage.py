import tkinter as tk
from PIL import Image, ImageTk

def insert_image(text_widget, image_path, tag, image_positions):
    # Open the image using Pillow (PIL)
    img = Image.open(image_path)

    # Convert the image to Tkinter PhotoImage
    img_tk = ImageTk.PhotoImage(img)

    # Insert an invisible (zero width and height) label with the image
    label = tk.Label(text_widget, image=img_tk)
    label.image = img_tk  # Keep a reference to prevent garbage collection

    # Get the current index of the Text widget
    current_index = text_widget.index(tk.END)

    # Insert the image
    text_widget.window_create(current_index, window=label)

    # Tag the image
    text_widget.tag_add(tag, current_index, f"{current_index}+1c")

    # Update the list of image positions
    image_positions.append(current_index)

# Function to find all indices of images
def get_image_positions(image_positions):
    return image_positions

# Create the main Tkinter window
root = tk.Tk()
root.title("Text with Images")

# Create a Text widget
text_widget = tk.Text(root, wrap=tk.WORD, width=240, height=100)
text_widget.pack()

# Maintain a list to store the positions of inserted images
image_positions = []

# Insert some text
text_widget.insert(tk.END, "This is some text. ")

# Insert images at various positions
insert_image(text_widget, "D:/butterfly.gif", "image_tag", image_positions)
text_widget.insert(tk.END, "More text. ")
insert_image(text_widget, "D:/butterfly.gif", "image_tag", image_positions)

# Get positions of inserted images
image_positions = get_image_positions(image_positions)
print("Indices of images:", image_positions)

# Start the Tkinter event loop
root.mainloop()
