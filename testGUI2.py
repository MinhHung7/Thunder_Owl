import tkinter as tk
from PIL import Image, ImageTk

def load_and_resize_image(file_path, width, height):
    original_image = Image.open(file_path)
    resized_image = original_image.resize((width, height))
    photo_image = ImageTk.PhotoImage(resized_image)
    return photo_image

def on_button_click(button_name):
    print(f"{button_name} clicked!")

def create_button_with_image_senDown(parent, file_path, width, height, button_name, command=None):
    image = load_and_resize_image(file_path, width, height)
    button = tk.Button(
        parent,
        text=button_name,
        image=image,
        compound=tk.LEFT,
        borderwidth=0,
        relief=tk.FLAT,
        command=command,
        activebackground="lightblue",
    )
    button.image = image
    return button

def toggle_additional_buttons(button_name):
    if button_name == "Sender":
        if btn_inbox_sender.winfo_ismapped():
            btn_inbox_sender.grid_forget()
            btn_send.grid_forget()
            btn_trash_sender.grid_forget()
        else:
            btn_inbox_sender.grid(row=1, column=0, pady=5)
            btn_send.grid(row=2, column=0, pady=5)
            btn_trash_sender.grid(row=3, column=0, pady=5)
    elif button_name == "Receiver":
        if btn_inbox_receiver.winfo_ismapped():
            btn_inbox_receiver.grid_forget()
            btn_trash_receiver.grid_forget()
        else:
            btn_inbox_receiver.grid(row=5, column=0, pady=5)
            btn_trash_receiver.grid(row=6, column=0, pady=5)
    elif button_name == "LocalStorage":
        if btn_outbox.winfo_ismapped():
            btn_outbox.grid_forget()
            btn_trash_local.grid_forget()
        else:
            btn_outbox.grid(row=8, column=0, pady=5)
            btn_trash_local.grid(row=9, column=0, pady=5)

# Create the main window
root = tk.Tk()
root.title("Button Example")

# Create buttons 1, 2, and 3
btn_sender = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/mail.png', 20, 20, 'hungm0434@gmail.com', lambda: toggle_additional_buttons("Sender"))
btn_sender.grid(row=0, column=0, pady=5)

btn_receiver = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/mail.png', 20, 20, 'iamhung12@gmail.com', lambda: toggle_additional_buttons("Receiver"))
btn_receiver.grid(row=4, column=0, pady=5)

btn_localStorage = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/folder.png', 20, 20, 'Local Folders', lambda: toggle_additional_buttons("LocalStorage"))
btn_localStorage.grid(row=7, column=0, pady=5)

# Create buttons 4 and 5 with icons but initially hide them
btn_inbox_sender = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/inbox.png', 20, 20, 'Inbox')
btn_inbox_sender.pack_forget()

btn_send = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/send.png', 20, 20, 'Send')
btn_send.pack_forget()

btn_trash_sender = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Trash')
btn_trash_sender.pack_forget()

btn_inbox_receiver = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/inbox.png', 20, 20, 'Inbox')
btn_inbox_receiver.pack_forget()

btn_trash_receiver = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Trash')
btn_trash_receiver.pack_forget()

btn_outbox = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/outbox.png', 20, 20, 'Outbox')
btn_outbox.pack_forget()

btn_trash_local = create_button_with_image_senDown(root, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Local Storages')
btn_trash_local.pack_forget()

# Start the Tkinter event loop
root.mainloop()
