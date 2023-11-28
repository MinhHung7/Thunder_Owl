import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage
from PIL import Image, ImageTk
from tkcalendar import Calendar


btn_inbox_sender=None
btn_send=None
btn_trash_sender=None

btn_inbox_receiver = None
btn_trash_receiver = None

btn_trash_local=None
btn_outbox=None

def on_entry_click(event, entry_widget):
    entry_widget.config(highlightbackground="#86b7fe", highlightcolor="#86b7fe", highlightthickness=3)

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

def button_toolbar_clicked(button_name):
    print(f"Toolbar button {button_name} clicked!")
    if(button_name == "Attach"):
        attach_file()

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
        # You can store the file_path or perform other actions with it

def newMessage():
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
    button_names = ["File", "Edit", "View", "Insert", "Attach", "Format", "Options", "Tools", "Help", "Send"]

    for name in button_names:
        button = tk.Button(toolbar_frame, text=name, command=lambda n=name: button_toolbar_clicked(n), width=6, height=1)
        button.pack(side="left", padx=5, pady=5)
        buttons.append(button)
    
    
    buttons[9].pack(side="right", padx=20, pady=5)


    # Message frame (center)
    message_frame = tk.Frame(new_Window, bd=1, relief="solid")
    message_frame.pack(side="top", fill="both", expand=True, pady=2)

    message_frame.rowconfigure(3, weight=1)  # Part 1
    message_frame.columnconfigure(3, weight=1)  # Part 2
    # Create textboxes and buttons

    field_frame = tk.Frame(message_frame)
    field_frame.pack(side="top", fill="both", expand=True)

    from_label = tk.Label(field_frame, text="From:", font=("Calibri", 12))
    from_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

    from_entry = tk.Entry(field_frame, font=("Calibri", 12), width=70, bd=1, relief="solid")
    from_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    from_entry.bind("<FocusIn>", lambda event: on_entry_click(event, from_entry))
    from_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, from_entry))

    cc_button = tk.Button(field_frame, text="CC", command=lambda: on_button_click("CC"))
    cc_button.grid(row=0, column=2, pady=5, padx=2, sticky="e")

    bcc_button = tk.Button(field_frame, text="BCC", command=lambda: on_button_click("BCC"))
    bcc_button.grid(row=0, column=3, pady=5, padx=5, sticky="e")

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
    subject_entry.grid(row=3, column=1, sticky="w", pady=2)
    subject_entry.bind("<FocusIn>", lambda event: on_entry_click(event, subject_entry))
    subject_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, subject_entry))
    subject_label = tk.Label(text_boxes_frame, text="Subject:", font=("Calibri", 12))
    subject_label.grid(row=3, column=0, pady=1, padx=10, sticky="w")


    text_mail_frame = tk.Frame(message_frame)
    text_mail_frame.pack(side="top", fill="both", expand=True, padx=2, pady=2)
    
    mail_entry = tk.Text(text_mail_frame, wrap="word", width=950, height=300, bd=1, relief="solid")
    mail_entry.grid(row=0, column=0, sticky="w", pady=2)
    mail_label = tk.Label(text_mail_frame, font=("Calibri", 12))
    mail_label.grid(row=0, column=0, pady=1, padx=10, sticky="w")
    #Additional components can be added as needed



# ... (rest of your code)


def toggle_additional_buttons(button_name):
    global btn_inbox_sender, btn_send, btn_trash_sender, btn_inbox_receiver, btn_trash_receiver, btn_outbox, btn_trash_local
    if button_name == "Sender":
        if btn_inbox_sender.winfo_ismapped():
            btn_inbox_sender.grid_forget()
            btn_send.grid_forget()
            btn_trash_sender.grid_forget()

            btn_sender.configure(bg="#f0f0f0")
        else:
            btn_inbox_sender.grid(row=1, column=0, pady=5)
            btn_send.grid(row=2, column=0, pady=5)
            btn_trash_sender.grid(row=3, column=0, pady=5)

            btn_sender.configure(bg="lightblue")
    elif button_name == "Receiver":
        if btn_inbox_receiver.winfo_ismapped():
            btn_inbox_receiver.grid_forget()
            btn_trash_receiver.grid_forget()

            btn_receiver.configure(bg="#f0f0f0")
        else:
            btn_inbox_receiver.grid(row=5, column=0, pady=5)
            btn_trash_receiver.grid(row=6, column=0, pady=5)

            btn_receiver.configure(bg="lightblue")
    elif button_name == "LocalStorage":
        if btn_outbox.winfo_ismapped():
            btn_outbox.grid_forget()
            btn_trash_local.grid_forget()

            btn_localStorage.configure(bg="#f0f0f0")
        else:
            btn_outbox.grid(row=8, column=0, pady=5)
            btn_trash_local.grid(row=9, column=0, pady=5)

            btn_localStorage.configure(bg="lightblue")

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
