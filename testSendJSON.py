import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage, simpledialog
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkcalendar import Calendar
import os
from tkinter.colorchooser import askcolor
from reportlab.pdfgen import canvas
from tkinterhtml import TkinterHtml
import socket
import json
from tkhtmlview import HTMLLabel
import base64

IP = socket.gethostbyname(socket.gethostname())
PORT = 2225
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

class FileMail:
    def __init__(self, file_name, data_file):
        self.file_name = file_name
        self.data_file = data_file

file_mail_list = []  # List to store FileMail objects

btn_inbox_sender=None
btn_send=None
btn_trash_sender=None

btn_inbox_receiver = None
btn_trash_receiver = None

btn_trash_local=None
btn_outbox=None

to_entry = None
from_entry = None
subject_entry = None
cc_entry = None
bcc_entry = None
mail_entry = None

image_references = []

def on_entry_click(event, entry_widget):
    entry_widget.config(highlightbackground="#86b7fe", highlightcolor="#86b7fe", highlightthickness=2)

def on_entry_leave(event, entry_widget):
    entry_widget.config(highlightthickness=0)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def load_and_resize_image(file_path, width, height):
    original_image = Image.open(file_path)
    resized_image = original_image.resize((width, height))
    photo_image = ImageTk.PhotoImage(resized_image)
    return photo_image

def remove_file_mail(index):
    if 0 <= index < len(file_mail_list):
        removed_file_mail = file_mail_list.pop(index)
        print(f"Removed file: {removed_file_mail.file_name}")

def remove_file_window():
    remove_window = tk.Toplevel(window)
    remove_window.title("Remove File")
    center_window(remove_window, 500, 400)

    # Create a label to display file list
    label = tk.Label(remove_window, text="File Mail List:")
    label.pack(pady=10)

    # Create a listbox to show files
    listbox = tk.Listbox(remove_window, selectmode=tk.SINGLE)
    for i, file_mail in enumerate(file_mail_list):
        listbox.insert(tk.END, f"{i}: {file_mail.file_name}")
    listbox.pack(pady=10)

    # Create an entry for the user to input the index
    index_entry = tk.Entry(remove_window, width=10)
    index_entry.pack(pady=10)

    # Create a button to perform removal
    remove_button = tk.Button(
        remove_window,
        text="Remove",
        command=lambda: remove_file_mail(int(index_entry.get()) if index_entry.get().isdigit() else -1)
    )
    remove_button.pack(pady=10)

def cut_action():
    global mail_entry
    mail_entry.event_generate("<<Cut>>")

def copy_action():
    global mail_entry
    mail_entry.event_generate("<<Copy>>")

def paste_action():
    global mail_entry
    mail_entry.event_generate("<<Paste>>")

def select_all_action():
    global mail_entry
    mail_entry.tag_add("sel", "1.0", tk.END)


def find_action():
    global mail_entry
    target = simpledialog.askstring("Find", "Enter text to find:")
    if target:
        start = "1.0"
        while start:
            start = mail_entry.search(target, start, tk.END, nocase=True)
            if start:
                end = f"{start}+{len(target)}c"
                mail_entry.tag_add("sel", start, end)
                mail_entry.mark_set("insert", end)
                start = end

def find_replace_action():
    global mail_entry
    target = simpledialog.askstring("Find and Replace", "Enter text to find:")
    if target:
        replace_text = simpledialog.askstring("Find and Replace", f"Replace '{target}' with:")
        if replace_text:
            start = "1.0"
            while start:
                start = mail_entry.search(target, start, tk.END, nocase=True)
                if start:
                    end = f"{start}+{len(target)}c"
                    mail_entry.delete(start, end)
                    mail_entry.insert(start, replace_text)
                    start = mail_entry.index(end)


def open_edit_window():
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed
    cut_button = tk.Button(edit_window, text="Cut", command=cut_action, width=button_width)
    cut_button.pack(pady=5)

    copy_button = tk.Button(edit_window, text="Copy", command=copy_action, width=button_width)
    copy_button.pack(pady=5)

    paste_button = tk.Button(edit_window, text="Paste", command=paste_action, width=button_width)
    paste_button.pack(pady=5)

    select_all_button = tk.Button(edit_window, text="Select All", command=select_all_action, width=button_width)
    select_all_button.pack(pady=5)

    find_button = tk.Button(edit_window, text="Find", command=find_action, width=button_width)
    find_button.pack(pady=5)

    find_replace_button = tk.Button(edit_window, text="Find and Replace", command=find_replace_action, width=button_width)
    find_replace_button.pack(pady=5)

    # Center the edit_window within the main window
    center_window(edit_window, 300, 250)  # Adjust the size as needed

def zoomIn_action():
    global mail_entry
    
    _ , current_size = mail_entry.cget("font").split()
    current_size = int(current_size)
    current_size += 1
    mail_entry.config(font=("Calibri", int(current_size)))

def zoomOut_action():
    global mail_entry
    
    _ , current_size = mail_entry.cget("font").split()
    current_size = int(current_size)
    current_size -= 1
    mail_entry.config(font=("Calibri", int(current_size)))

def reset_action():
    global mail_entry
    mail_entry.config(font=("Calibri", 11))

def open_view_window():
    view_window = tk.Toplevel(window)
    view_window.title("View Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed

    zoomIn_button = tk.Button(view_window, text="Zoom In", command=zoomIn_action, width=button_width)
    zoomIn_button.pack(pady=5)

    zoomOut_button = tk.Button(view_window, text="Zoom Out", command=zoomOut_action, width=button_width)
    zoomOut_button.pack(pady=5)

    reset_button = tk.Button(view_window, text="Reset", command=reset_action, width=button_width)
    reset_button.pack(pady=5)

    # Center the edit_window within the main window
    center_window(view_window, 200, 120)  # Adjust the size as needed


def getIndexImage(event):
    global cursor_index
    cursor_index = mail_entry.index(tk.CURRENT)
    with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
        data = json.load(file)
        data["Image"]["position"].append(cursor_index)
    with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
            json.dump(data, file, indent = 2)

def insert_image():

    global mail_entry
    global image_references

    # Ask the user to choose an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

    if file_path:

        # Create a PhotoImage object
        img = tk.PhotoImage(file=file_path)

        # Get the dimensions of the image
        img_width = img.width()
        img_height = img.height()

        # Define the maximum width for the image
        max_width = 300  # Change this value to your desired maximum width

        # Calculate the scale factor based on the maximum width
        scale_factor = max_width / img_width

        # Calculate the new dimensions while preserving the aspect ratio
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        # Resize the image using the zoom method
        img = img.subsample(int(img_width / new_width), int(img_height / new_height))

        # Insert the image into the Text widget
        mail_entry.image_create(tk.END, image=img)
        
        image_references.append(img)

        mail_entry.bind("<Button-3>", getIndexImage)

        with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
            data = json.load(file)
            with open(file_path, "rb") as f:
                image_data = f.read()
                data["Image"]["data"].append(base64.b64encode(image_data).decode('utf-8'))
            data["Image"]["width"].append(new_width)
            data["Image"]["height"].append(new_height)
        with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
                json.dump(data, file, indent = 2)
        

def change_font(font_name):
    global mail_entry
    print(font_name)
    if mail_entry.tag_ranges(tk.SEL):
        start, end = mail_entry.tag_ranges(tk.SEL)
        mail_entry.tag_add("highlighted", start, end)
        mail_entry.tag_configure("highlighted", font=font_name)

        with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
            data = json.load(file)
            data["Font"]["start"].append(str(start))
            data["Font"]["end"].append(str(end))
            data["Font"]["NameFont"].append(font_name)
        with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
                json.dump(data, file, indent = 2)

def font_action():
    global mail_entry
    font_window = tk.Toplevel(window)
    font_window.title("Font Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed

    font_buttons = ["Arial", "Terminal", "Roman", "Roboto", "Stencil", "Verdana", "Tahoma", "Calibri", "Gigi", "Broadway"
                    , "Wingdings", "Meiryo", "@SimSun", "Georgia", "Impact", "Courier"]
    
    for font_name in font_buttons:
        font_button = tk.Button(font_window, text=font_name, width = button_width, command=lambda font=font_name: change_font(font))
        font_button.pack(pady=5)

    # Center the font_window within the main window
    center_window(font_window, 250, 640)  # Adjust the size as needed

def change_style(style):
    if style == "Bold":
        apply_tag("bold")
    elif style == "Italic":
        apply_tag("italic")
    elif style == "Underline":
        apply_tag("underline")
    elif style == "Strikethrough":
        apply_tag("strikethrough")
    elif style == "Superscript":
        apply_tag("superscript")
    elif style == "Subscript":
        apply_tag("subscript")
    elif style == "Emphasis":
        apply_tag("emphasis")
    elif style == "Code":
        apply_tag("code")

def apply_tag(tag):
    current_tags = mail_entry.tag_names("sel.first")
    if tag in current_tags:
        mail_entry.tag_remove(tag, "sel.first", "sel.last")
    else:
        mail_entry.tag_add(tag, "sel.first", "sel.last")
        mail_entry.tag_configure(tag, **tag_styles[tag])

        tag_ranges = mail_entry.tag_ranges(tag)
        if tag_ranges:
            start_index, end_index = tag_ranges[0], tag_ranges[1]
            with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
                data = json.load(file)
                data["Style"][tag]["start"].append(str(start_index))
                data["Style"][tag]["end"].append(str(end_index))
            with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
                    json.dump(data, file, indent = 2)
            
tag_styles = {
    "bold": {"font": ("Helvetica", 12, "bold")},
    "italic": {"font": ("Helvetica", 12, "italic")},
    "underline": {"underline": True},
    "strikethrough": {"overstrike": True},
    "superscript": {"offset": 10, "font": ("Helvetica", 10)},
    "subscript": {"offset": -5, "font": ("Helvetica", 10)},
    "emphasis": {"foreground": "blue"},
    "code": {"font": ("Courier New", 12)},
}

def text_style_action():
    global mail_entry
    style_window = tk.Toplevel(window)
    style_window.title("Style Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed

    style_buttons = ["Bold", "Italic", "Underline", "Strikethrough", "Superscript", "Subscript", "Emphasis", "Code"]
    
    for style_name in style_buttons:
        style_button = tk.Button(style_window, text=style_name, width = button_width, command=lambda style=style_name: change_style(style))
        style_button.pack(pady=5)

    # Center the font_window within the main window
    center_window(style_window, 250, 640)  # Adjust the size as needed

def text_color_action():
    global mail_entry
    # Get the current selected text
    selected_text = mail_entry.get("sel.first", "sel.last")

    if selected_text:
        # Show color dialog
        color, _ = askcolor()

        if color:
            # Convert RGB values to hex color string
            hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
            
            # Configure the tag with the selected color
            mail_entry.tag_configure("text_color", foreground=hex_color)
            
            # Apply the tag to the selected text
            mail_entry.tag_add("text_color", "sel.first", "sel.last")

            tag_ranges = mail_entry.tag_ranges("text_color")
            if tag_ranges:
                start_index, end_index = tag_ranges[0], tag_ranges[1]
                with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
                    data = json.load(file)
                    data["Color"]["start"].append(str(start_index))
                    data["Color"]["end"].append(str(end_index))
                    data["Color"]["colors"].append(str(hex_color))
                with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
                        json.dump(data, file, indent = 2)


def align_action(alignment):
    global mail_entry

    # Get the currently selected text
    selected_text = mail_entry.get(tk.SEL_FIRST, tk.SEL_LAST)

    # If there is no selected text, do nothing
    if not selected_text:
        return

    # Configure a tag for the selected alignment
    mail_entry.tag_configure(alignment, lmargin1=0, lmargin2=0, rmargin=mail_entry.winfo_width())

    # Add the tag to the selected text
    mail_entry.tag_add(alignment, tk.SEL_FIRST, tk.SEL_LAST)

def open_align_window():

    align_window = tk.Toplevel(window)
    align_window.title("Align Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed
    new_button = tk.Button(align_window, width=button_width, text="Left", command=lambda: align_action(tk.LEFT))
    new_button.pack(pady=5)

    attach_button = tk.Button(align_window, width=button_width, text="Center", command=lambda: align_action(tk.CENTER))
    attach_button.pack(pady=5)

    saveAs_button = tk.Button(align_window, width=button_width, text="Right", command=lambda: align_action(tk.RIGHT))
    saveAs_button.pack(pady=5)

    close_button = tk.Button(align_window, width=button_width, text="Justify", command=lambda: align_action(tk.BOTH))
    close_button.pack(pady=5)

    # Center the edit_window within the main window
    center_window(align_window, 300, 170)  # Adjust the size as needed

def open_format_window():
    format_window = tk.Toplevel(window)
    format_window.title("Format Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed
    font_button = tk.Button(format_window, text="Font", command=font_action, width=button_width)
    font_button.pack(pady=5)

    copy_button = tk.Button(format_window, text="Text Style", command=text_style_action, width=button_width)
    copy_button.pack(pady=5)

    paste_button = tk.Button(format_window, text="Text Color", command=text_color_action, width=button_width)
    paste_button.pack(pady=5)

    select_all_button = tk.Button(format_window, text="Align", command=align_action, width=button_width)
    select_all_button.pack(pady=5)

    # Center the edit_window within the main window
    center_window(format_window, 300, 250)  # Adjust the size as needed

new_Window = None
file_window = None

def close_action():
    global new_Window
    global file_window

    if new_Window.winfo_exists():
        new_Window.destroy()
    if file_window.winfo_exists():
        file_window.destroy()

def saveAs_action():
    # Ask the user for the file location
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Text files", "*.html")])
    if not file_path:
        return  # User canceled the file dialog

    # Get the content from the Text widget
    text_content = mail_entry.get("1.0", tk.END)
    print(text_content)

    # Save the content to the specified file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)

def open_file_window():
    global file_window
    file_window = tk.Toplevel(window)
    file_window.title("File Options")

    # Create buttons in the Edit window with fixed width
    button_width = 15  # Adjust the width as needed
    new_button = tk.Button(file_window, text="New", command=newMessage, width=button_width)
    new_button.pack(pady=5)

    attach_button = tk.Button(file_window, text="Attach", command=attach_file, width=button_width)
    attach_button.pack(pady=5)

    saveAs_button = tk.Button(file_window, text="Save as", command=saveAs_action, width=button_width)
    saveAs_button.pack(pady=5)

    close_button = tk.Button(file_window, text="Close", command=close_action, width=button_width)
    close_button.pack(pady=5)

    # Center the edit_window within the main window
    center_window(file_window, 300, 170)  # Adjust the size as needed



def connect_server():
    global from_entry, to_entry, mail_entry, cc_entry, bcc_entry, file_mail_list
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.settimeout(1000)
            client.connect(ADDR)
            print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

            # Receive and print the server's initial response
            initial_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {initial_response}")

            # Send the MAIL FROM command
            mail_from = from_entry.get("1.0", "end-1c")
            mail_from_command = "MAIL FROM: " + mail_from + "\r\n"
            client.send(mail_from_command.encode('utf-8'))

            # Receive and print the server's response to the MAIL FROM command
            mail_from_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {mail_from_response}")

            # Send the RCPT TO command
            recipient = to_entry.get("1.0", "end-1c")
            recipient_email = "RCPT TO: " + recipient + "\r\n"
            client.send(recipient_email.encode('utf-8'))

            # Receive and print the server's response to the RCPT TO command
            rcpt_to_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {rcpt_to_response}")

            # Send DATA command
            data_command = "DATA\r\n"
            client.send(data_command.encode('utf-8'))

            # Receive and print the server's response to the DATA command
            data_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {data_response}")

            # Send the message data
            subject = subject_entry.get("1.0", "end-1c")

            with open("D:/FILE SOCKET PYTHON/data.json", "r") as file:
                data = json.load(file)
                data["RawContent"] = mail_entry.get("1.0", "end-1c")
                with open("D:/FILE SOCKET PYTHON/data.json", "w") as file:
                    json.dump(data, file, indent = 2)

            
            # Receive and print the server's response to the message data
            message_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {message_response}")

            for file in file_mail_list:
                message_file_data = (
                    f"Content-Type: application/pdf;name={file.file_name}\r\n"
                    f"Content-Disposition: attachment;filename={file.file_name}\r\n"
                    f"Content-Transfer-Encoding: base64\r\n\r\n"
                    f"{file.data_file}\r\n"
                )
                client.send(message_file_data.encode('utf-8'))
                file_response = client.recv(1024).decode('utf-8')
                print(f"[SERVER] {file_response}")
                client.send(".\r\n".encode('utf-8'))


            # Send the QUIT command
            quit_command = "QUIT\r\n"
            client.send(quit_command.encode('utf-8'))

            # Receive and print the server's response to the QUIT command
            quit_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {quit_response}")

        except Exception as e:
            print(f"Error: {e}")

def button_toolbar_clicked(button_name):
    print(f"Toolbar button {button_name} clicked!")
    if(button_name == "File"):
        open_file_window()
    if (button_name == "Edit"):
        open_edit_window()
    if(button_name == "View"):
        open_view_window()
    if(button_name == "Attach"):
        attach_file()
    if(button_name == "Remove"):
        remove_file_window()
    if(button_name == "Image"):
        insert_image()
    if(button_name == "Format"):
        open_format_window()
    if(button_name == "Send"):
        connect_server()

def button_clicked(button_name):
    print(f"{button_name} clicked!")

def on_button_click(button_name):
    print(f"{button_name} clicked!")

    label_second_part.pack_forget()
    if button_name=="Mail":
        create_mail_subframe()
    elif button_name=="Calendar":
        create_calendar_subframe()

def create_button_with_image(parent, file_path, width, height, button_name):
    image = load_and_resize_image(file_path, width, height)
    button = tk.Button(
        parent,
        image=image,
        borderwidth=0,
        cursor="hand2",
        relief=tk.FLAT,
        command=lambda: on_button_click(button_name),
        activebackground="lightblue",
    )
    button.image = image
    return button, image

def create_button_with_image_senDown(parent, file_path, width, height, button_name, command=None, text=None):
    image = load_and_resize_image(file_path, width, height)
    button_text = text if text is not None else button_name
    button = tk.Button(
        parent,
        text=button_text,
        image=image,
        cursor="hand2",
        compound=tk.LEFT,
        borderwidth=0,
        relief=tk.FLAT,
        command=command,
        activebackground="lightblue",
    )
    button.image = image
    return button

def attach_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        print(f"File attached: {file_path}")

        # Read the contents of the file into a bytes variable
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Create a FileMail object and add it to the list
        file_name = os.path.basename(file_path)
        file_mail = FileMail(file_name, file_data)
        file_mail_list.append(file_mail)

        print(f"File data:\n{file_mail.file_name}, {file_mail.data_file}")


def newMessage():
    global to_entry, subject_entry, cc_entry, bcc_entry, mail_entry, from_entry

    global new_Window
    new_Window = tk.Toplevel()
    new_Window.title("Write - ThunderOwl")
    center_window(new_Window, 950, 600)
    new_Window.resizable(False, False)

    new_Window.transient(window)
    # Set up grid weights for resizable behavior
    new_Window.rowconfigure(0, weight=1)
    new_Window.columnconfigure(0, weight=1)
    new_Window.columnconfigure(1, weight=20)

    # Toolbar frame (top)
    toolbar_frame = tk.Frame(new_Window, bg="white", bd=1, relief="solid")
    toolbar_frame.pack(side="top", fill="x", pady=2)

    # Create buttons for the toolbar
    buttons = []
    button_names = ["File", "Edit", "View", "Image", "Attach", "Format", "Options", "Tools", "Help", "Send", "Remove"]

    for name in button_names:
        button = tk.Button(toolbar_frame, text=name, command=lambda n=name: button_toolbar_clicked(n), width=6, height=1)
        button.pack(side="left", padx=5, pady=5)
        buttons.append(button)
    
    
    buttons[9].pack(side="right", padx=20, pady=5)


    # Message frame (center)
    message_frame = tk.Frame(new_Window, bd=1, relief="solid")
    message_frame.pack(side="top", fill="both", expand=True, pady=2)

    message_frame.rowconfigure(4, weight=1)  # Part 1
    message_frame.columnconfigure(3, weight=1)  # Part 2
    # Create textboxes and buttons

    field_frame = tk.Frame(message_frame)
    field_frame.pack(side="top", fill="both", expand=True)

    from_label = tk.Label(field_frame, text="From:", font=("Calibri", 12))
    from_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

    from_entry = tk.Text(field_frame, wrap="word", width=80, height=1, bd=1, relief="solid")
    from_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    from_entry.bind("<FocusIn>", lambda event: on_entry_click(event, from_entry))
    from_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, from_entry))

    # Create a frame for the text boxes with a fixed height of 200
    text_boxes_frame = tk.Frame(message_frame)
    text_boxes_frame.pack(side="top", fill="both", expand=True)
    # Configure row 1 in text_boxes_frame to have a fixed weight
    text_boxes_frame.grid_rowconfigure(1, weight=1)

    # First text box
    to_entry = tk.Text(text_boxes_frame, wrap="word", width=80, height=1, bd=1, relief="solid")
    to_entry.grid(row=2, column=1, sticky="w", pady=2)
    to_entry.bind("<FocusIn>", lambda event: on_entry_click(event, to_entry))
    to_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, to_entry))
    to_label = tk.Label(text_boxes_frame, text="To:", font=("Calibri", 12))
    to_label.grid(row=2, column=0, pady=1, padx=10, sticky="w")
    # Second text box
    subject_entry = tk.Text(text_boxes_frame, wrap="word", width=80, height=1, bd=1, relief="solid")
    subject_entry.grid(row=5, column=1, sticky="w", pady=2)
    subject_entry.bind("<FocusIn>", lambda event: on_entry_click(event, subject_entry))
    subject_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, subject_entry))
    subject_label = tk.Label(text_boxes_frame, text="Subject:", font=("Calibri", 12))
    subject_label.grid(row=5, column=0, pady=1, padx=10, sticky="w")

    cc_entry = tk.Text(text_boxes_frame, wrap="word", width=80, height=1, bd=1, relief="solid")
    cc_entry.grid(row=3, column=1, sticky="w", pady=2)
    cc_entry.bind("<FocusIn>", lambda event: on_entry_click(event, cc_entry))
    cc_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, cc_entry))
    cc_label = tk.Label(text_boxes_frame, text="CC:", font=("Calibri", 12))
    cc_label.grid(row=3, column=0, pady=1, padx=10, sticky="w")

    bcc_entry = tk.Text(text_boxes_frame, wrap="word", width=80, height=1, bd=1, relief="solid")
    bcc_entry.grid(row=4, column=1, sticky="w", pady=2)
    bcc_entry.bind("<FocusIn>", lambda event: on_entry_click(event, bcc_entry))
    bcc_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, bcc_entry))
    bcc_label = tk.Label(text_boxes_frame, text="BCC:", font=("Calibri", 12))
    bcc_label.grid(row=4, column=0, pady=1, padx=10, sticky="w")


    text_mail_frame = tk.Frame(message_frame)
    text_mail_frame.pack(side="top", fill="both", expand=True, padx=2, pady=2)
    
    mail_entry = tk.Text(text_mail_frame, wrap="word", width=950, bd=1, relief="solid")
    mail_entry.grid(row=0, column=0, sticky="w", pady=2)
    mail_entry.configure(font=("Calibri", 11))


def toggle_additional_buttons(button_name):
    global btn_inbox_sender, btn_send, btn_trash_sender, btn_inbox_receiver, btn_trash_receiver, btn_outbox, btn_trash_local
    if button_name == "Sender":
        if btn_inbox_sender.winfo_ismapped():
            btn_inbox_sender.grid_forget()
            btn_send.grid_forget()
            btn_trash_sender.grid_forget()


        else:
            btn_inbox_sender.grid(row=1, column=0, pady=5)
            btn_send.grid(row=2, column=0, pady=5)
            btn_trash_sender.grid(row=3, column=0, pady=5)

            btn_sender.configure(bg="lightblue")
            btn_receiver.configure(bg="#f0f0f0")
            btn_localStorage.configure(bg="#f0f0f0")
    elif button_name == "Receiver":
        if btn_inbox_receiver.winfo_ismapped():
            btn_inbox_receiver.grid_forget()
            btn_trash_receiver.grid_forget()


        else:
            btn_inbox_receiver.grid(row=5, column=0, pady=5)
            btn_trash_receiver.grid(row=6, column=0, pady=5)

            btn_receiver.configure(bg="lightblue")
            btn_sender.configure(bg="#f0f0f0")
            btn_localStorage.configure(bg="#f0f0f0")
    elif button_name == "LocalStorage":
        if btn_outbox.winfo_ismapped():
            btn_outbox.grid_forget()
            btn_trash_local.grid_forget()


        else:
            btn_outbox.grid(row=8, column=0, pady=5)
            btn_trash_local.grid(row=9, column=0, pady=5)

            btn_localStorage.configure(bg="lightblue")
            btn_sender.configure(bg="#f0f0f0")
            btn_receiver.configure(bg="#f0f0f0")

def search_bar_focus_in(event):
    search_entry.delete(0, tk.END)
    search_entry.config(foreground="black")

def search_bar_focus_out(event):
    if not search_entry.get():
        search_entry.insert(0, "Search...")
        search_entry.config(foreground="grey")

def perform_search():
    search_term = search_entry.get()
    # Add your search functionality here
    print(f"Searching for: {search_term}")

def create_second_part():

    global label_second_part
    second_part_frame = tk.Frame(window, bg="white")
    second_part_frame.grid(row=0, column=1, sticky="ns", padx=0, pady=0)

    image_path = "D:/FILE SOCKET PYTHON/Icons/Thunder.png"  # Replace with the path to your image
    image = load_and_resize_image(image_path, 1400, 700)  # Adjust the width and height as needed

    label_second_part = tk.Label(second_part_frame, bg="#F4F4F9", image=image)
    label_second_part.image = image  # Keep a reference to the image to prevent it from being garbage collected
    label_second_part.pack()


def create_mail_subframe():
    global search_entry, btn_inbox_receiver, btn_trash_receiver, btn_inbox_sender, btn_send, btn_trash_sender, btn_outbox, btn_trash_local, btn_sender, btn_receiver, btn_localStorage
    # Search Bar with rounded corners and border
    search_entry = ttk.Entry(window, font=("Arial", 12), width=70, style="Search.TEntry")
    search_entry.grid(row=0, column=1, pady=10, padx=5, sticky="n")
    search_entry.insert(0, "Search...")
    search_entry.config(foreground="grey")
    search_entry.bind("<FocusIn>", search_bar_focus_in)
    search_entry.bind("<FocusOut>", search_bar_focus_out)

    search_button, _ = create_button_with_image(window, 'D:/FILE SOCKET PYTHON/Icons/search_icon.png', 30, 30, 'Search_icon')
    search_button.grid(row=0, column=2, pady=10, padx=5, sticky="n")

    # Style for the rounded search bar
    style = ttk.Style()
    style.configure("Search.TEntry", borderwidth=1, relief="solid", padding=(5, 2, 5, 2), bordercolor="grey")

    second_subframe = tk.Frame(window, bg="#F4F4F9")
    second_subframe.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    second_subframe.columnconfigure(0, weight=1)  # Part 1
    second_subframe.columnconfigure(1, weight=100)  # Part 2

    graysubframe = tk.Frame(second_subframe, bg="white", bd=1,relief="solid")
    graysubframe.grid(row=0, column=1, sticky="nsew", padx=0, pady=(40,0))
    label_gray = tk.Label(graysubframe, bg="white", width=150, height = 40)
    label_gray.grid(row=0, column=1, sticky="nsew",padx=0, pady=0)

    whitesubframe = tk.Frame(second_subframe, bg="white")
    whitesubframe.grid(row=0, column=0, sticky="nsew", padx=0, pady=(40, 0))

    whitesubframe.rowconfigure(1, weight=1)  # Part 1
    whitesubframe.columnconfigure(0, weight=1)  # Part 2

    sendown_frame = tk.Frame(whitesubframe)
    sendown_frame.grid(row=0, column=0, sticky="new")

    email_frame = tk.Frame(whitesubframe)
    email_frame.grid(row=1, column=0, sticky="nsew")

    style.configure("Rounded.TButton", padding=10, borderwidth=2, relief="groove", highlightthickness=0)
    button_inside_whitesubframe = ttk.Button(sendown_frame, text="+ New message" ,style="Rounded.TButton", cursor="hand2", command=lambda: newMessage())
    button_inside_whitesubframe.grid(row=0, column=1, sticky="n", padx=25, pady=20)
    
    download_but, _ = create_button_with_image(sendown_frame, 'D:/FILE SOCKET PYTHON/Icons/download.png', 25, 25, "download")
    download_but.grid(row=0, column=0, sticky="nw", padx=25, pady=31)


    btn_sender = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/mail.png', 20, 20, 'hungm0434@gmail.com', lambda button_name="Sender": toggle_additional_buttons(button_name))
    btn_sender.configure(font=("Calibri", 11, "bold"))
    btn_sender.grid(row=0, column=0, sticky="new", padx = 30, pady=5)

    btn_receiver = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/mail.png', 20, 20, 'iamhung12@gmail.com', lambda button_name="Receiver": toggle_additional_buttons(button_name))
    btn_receiver.configure(font=("Calibri", 11, "bold"))    
    btn_receiver.grid(row=4, column=0,pady=5)

    btn_localStorage = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/folder.png', 20, 20, 'Local Folders', lambda button_name="LocalStorage": toggle_additional_buttons(button_name))
    btn_localStorage.configure(font=("Calibri", 11, "bold"))
    btn_localStorage.grid(row=7, column=0,pady=5)

    # Create buttons 4 and 5 with icons but initially hide them
    btn_inbox_sender = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/inbox.png', 20, 20, 'Inbox')
    btn_inbox_sender.pack_forget()

    btn_send = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/send.png', 20, 20, 'Send')
    btn_send.pack_forget()

    btn_trash_sender = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Trash')
    btn_trash_sender.pack_forget()

    btn_inbox_receiver = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/inbox.png', 20, 20, 'Inbox')
    btn_inbox_receiver.pack_forget()

    btn_trash_receiver = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Trash')
    btn_trash_receiver.pack_forget()

    btn_outbox = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/outbox.png', 20, 20, 'Outbox')
    btn_outbox.pack_forget()

    btn_trash_local = create_button_with_image_senDown(email_frame, 'D:/FILE SOCKET PYTHON/Icons/trash-bin.png', 20, 20, 'Trash')
    btn_trash_local.pack_forget()


def select_date(mycal, selected_date_label):
    my_date = mycal.get_date()
    selected_date_label.config(text=my_date)

def create_calendar_subframe():
    second_subframe = tk.Frame(window, bg="white")
    second_subframe.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
    second_subframe.rowconfigure(0, weight=1)
    second_subframe.columnconfigure(1, weight=1)

    # Left part (Mini Calendar)
    left_frame = tk.Frame(second_subframe, bg="#F4F4F9")
    left_frame.grid(row=0, column=0, sticky="ns")

    # Increase the font size of the calendar
    mycal = Calendar(left_frame, setmode="day", date_pattern='d/m/yy', font="Arial 10")
    mycal.pack(padx=20, pady=80)

    selected_date_label = tk.Label(left_frame, text="")
    selected_date_label.pack(padx=2, pady=2)

    open_cal = tk.Button(left_frame, text="Select Date", command=lambda: select_date(mycal, selected_date_label))
    open_cal.pack(padx=15, pady=15)

def create_buttons_frame():
    buttons_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    buttons_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    # Create buttons with images
    buttons = []
    btn_mail, _ = create_button_with_image(buttons_frame, 'D:/FILE SOCKET PYTHON/Icons/mail.png', 35, 35, 'Mail')
    btn_address_book, _ = create_button_with_image(buttons_frame, 'D:/FILE SOCKET PYTHON/Icons/phone-book.png', 35, 35, 'Address_Book')
    btn_calendar, _ = create_button_with_image(buttons_frame, 'D:/FILE SOCKET PYTHON/Icons/calendar.png', 35, 35, 'Calendar')
    btn_task, _ = create_button_with_image(buttons_frame, 'D:/FILE SOCKET PYTHON/Icons/list.png', 35, 35, 'Task')
    btn_chat, _ = create_button_with_image(buttons_frame, 'D:/FILE SOCKET PYTHON/Icons/chat.png', 35, 35, 'Chat')
    
    btn_mail.grid(row=0, column=0, sticky="ew", padx=8, pady=10)
    btn_address_book.grid(row=1, column=0, sticky="ew", padx=8, pady=10)
    btn_calendar.grid(row=2, column=0, sticky="ew", padx=8, pady=10)
    btn_task.grid(row=3, column=0, sticky="ew", padx=8, pady=10)
    btn_chat.grid(row=4, column=0, sticky="ew", padx=8, pady=10)
    buttons.append([btn_mail, btn_address_book, btn_calendar, btn_task, btn_chat])

    return buttons

window = tk.Tk()
window.title("Thunder-Owl")
center_window(window, 1400, 700)
window.resizable(False, False)
logo_image = PhotoImage(file="D:/FILE SOCKET PYTHON/Icons/owl.png")

    # Set the window icon (logo)
window.iconphoto(True, logo_image)
txt_edit = tk.Text(window)
txt_edit.config(state=tk.DISABLED)  # Make the Text widget initially non-editable

# Set up grid weights for resizable behavior
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight = 1)
window.columnconfigure(1, weight = 20)

create_second_part() # Image
# Create buttons frame (Part 1)
buttons = create_buttons_frame()

window.mainloop()
