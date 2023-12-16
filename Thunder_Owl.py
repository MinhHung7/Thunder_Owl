import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import io
from tkcalendar import Calendar
import threading
import time
import os
from tkinter.colorchooser import askcolor
import socket
import json
import base64
from pathlib import Path
import customtkinter
from customtkinter import *
import re
from datetime import datetime

IP = socket.gethostbyname(socket.gethostname())
SMTP_PORT = 2225
POP3_PORT = 3335
ADDR_SMTP = (IP, SMTP_PORT)
ADDR_POP3 = (IP, POP3_PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
PATH = CRIPT_LOCATION = Path(__file__).absolute().parent

with open(PATH/'Temp_email.json', 'r') as file:
    data_copy = json.load(file)

def dowload_email_every_1_minute_thread_function():
    while (True):
        time.sleep(10)
        get_all_the_mail_from_sever_that_has_not_been_dowloaded('hoangkhang@gmail.com', 123)
        get_all_the_mail_from_sever_that_has_not_been_dowloaded('hahuy@gmail.com', 123)
        get_all_the_mail_from_sever_that_has_not_been_dowloaded('hungm0434@gmail.com', 123)
    

# ===============================================================================================
def get_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%a, %d %b %Y %H:%M:%S")
    return formatted_date
# ===============================================================================================
def fixTextForButton(fromUser, date, subject, width):
    finalText = fromUser
    for i in range(width - 20 - len(fromUser)):
        finalText += " "
    finalText = finalText + date + "\n" + "Subject: " + subject

    return finalText 
# ===============================================================================================
def resolveFile(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{data["File_content_type"]}",
        filetypes=[(f"{data["File_content_type"].upper()} files", f"*.{data["File_content_type"]}")],
        title="Save File As"
    )

    if file_path:
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(data["File_content"]))
        print(f"File '{file_path}' has been saved.")

# ===============================================================================================
def resolveMail(user, Mail_box, index):
    global detailMailListFolderFrame, resolveTagName, content_Text

    with open(PATH/"database.json", "r") as file:
        data = json.load(file)
        data["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Have_been_read"] = 1
    
    with open(PATH/'database.json', 'w') as file:
        json.dump(data, file, indent=2)

    # detailMailListFolderFrame.rowconfigure(0, weight=1)
    detailMailListFolderFrame.rowconfigure(1, weight=1)
    detailMailListFolderFrame.columnconfigure(0, weight=1)

    header_frame = CTkFrame(master=detailMailListFolderFrame, fg_color="#27272A", border_width=3, border_color="#323742", height=130)
    header_frame.grid(row=0, column=0, sticky = "nsew")
    content_frame = CTkFrame(master=detailMailListFolderFrame, fg_color="white", border_width=3)
    content_frame.grid(row=1, column=0, sticky = "nsew")
    file_frame = CTkScrollableFrame(master=detailMailListFolderFrame, fg_color="#3F3F46", height=40, orientation = "horizontal")
    file_frame.grid(row=2, column=0, sticky = "nsew")

    with open(PATH/"database.json", "r") as file:
        database = json.load(file)

    for file in database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["File_list"]:
        file_button = CTkButton(file_frame, text = file["File_name"], fg_color="#484F60", font=("Montserra", 14), hover_color="#707A94", cursor = "hand2", text_color="#91F3FD", height = 50, command=lambda data = file: resolveFile(data))
        file_button.pack(side = tk.LEFT, padx = 5)
    disable(header_frame)

    header_frame.rowconfigure(0, weight=1)
    header_frame.rowconfigure(1, weight=1)
    header_frame.rowconfigure(2, weight=1)
    header_frame.rowconfigure(3, weight=1)
    

    from_header_text = ">>> From: " + database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["From"]
    length_To_Header = len(database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["From"]) + 3
    for i in range(125 - length_To_Header):
        from_header_text += " " 
    from_header_text += database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Date"]
    from_header_label = CTkLabel(master = header_frame, text = from_header_text, font = ("Montserrat", 17))    
    from_header_label.grid(row=0, column=0, padx = 20, pady = 5, sticky = "w")
    
    to_header_text = ">>> To: " + database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["To"]
    to_header_label = CTkLabel(master = header_frame, text = to_header_text, font = ("Montserrat", 17))
    to_header_label.grid(row=1, column=0, padx = 20, pady = 4, sticky = "w")
    
    text_cc = ">>> Cc: "
    if not database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Cc"]:
        text_cc += "None"
    
    for user_cc in database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Cc"]:
        text_cc = text_cc + " " + user_cc

    cc_header_label = CTkLabel(master = header_frame, text =  text_cc, font = ("Montserrat", 17))
    cc_header_label.grid(row=2, column=0, padx = 20, pady = 4, sticky = "w")
    
    subject_header_label = CTkLabel(master = header_frame, text = ">>> Subject: " + database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Subject"], font = ("Montserrat", 17))
    subject_header_label.grid(row=3, column=0, padx = 20, pady = 10, sticky = "w")

    content_frame.rowconfigure(0, weight=1)
    content_frame.columnconfigure(0, weight=1)
    content_Text = tk.Text(content_frame, bd=1, relief = "solid", borderwidth=2, font = ("Calibri", 12), background="#282C34", foreground="white")
    content_Text.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

#================================================================================================
    target_mail = database["User_list"][user]["Mail_box"][Mail_box]["Email_list"][index]["Main_content"]
    content_Text.insert(tk.END, target_mail["RawContent"])

    for key in target_mail["Style"]:
        mode = key
        for index, items in enumerate(target_mail["Style"][key]["start"]):
            start_position = items
            end_position = target_mail["Style"][key]["end"][index]

            change_style_resolve(start_position, end_position, mode)

    for index, items in enumerate(target_mail["Font"]["start"]):
        start_position = items
        end_position = target_mail["Font"]["end"][index]
        mode = target_mail["Font"]["NameFont"][index]

        change_font_resolve(start_position, end_position, mode)

    for index, items in enumerate(target_mail["Color"]["start"]):
        start_position = items
        end_position = target_mail["Color"]["end"][index]
        mode = target_mail["Color"]["colors"][index]

        change_color_resolve(start_position, end_position, mode)

    for index, items in enumerate(target_mail["Image"]["position"]):
        position = items
        data = base64.b64decode(target_mail["Image"]["data"][index])
        height = target_mail["Image"]["height"][index]
        width = target_mail["Image"]["width"][index]

        resolve_image(data, position, height, width)

    
  
# ===============================================================================================
def resolve_image(image_data, position, height, width):
    global content_Text, image_references
    img = Image.open(io.BytesIO(image_data))
    
    max_width = 300
    scale_factor = max_width / width
    new_size = (int(width * scale_factor), int(height * scale_factor))
    img = img.resize(new_size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    # Insert an invisible image at the specified position
    content_Text.image_create(position, image=img)
    image_references.append(img)
# ===============================================================================================
def change_style_resolve(start, end, mode):
    global resolveTagName, content_Text
    content_Text.tag_configure(resolveTagName, **tag_styles[mode])
    content_Text.tag_add(resolveTagName, start, end)
    resolveTagName = resolveTagName + 1

def change_font_resolve(start, end, mode):
    global resolveTagName, content_Text
    content_Text.tag_configure(resolveTagName, font = mode)
    content_Text.tag_add(resolveTagName, start, end)
    resolveTagName = resolveTagName + 1

def change_color_resolve(start, end, color):
    global resolveTagName, content_Text
    content_Text.tag_configure(resolveTagName, foreground = color)
    content_Text.tag_add(resolveTagName, start, end)
    resolveTagName = resolveTagName + 1


# ===============================================================================================
def getFolderMessage(user, folder):
    global detailMailListFolderFrame
    new_Window = CTkToplevel(window)
    new_Window.geometry("1400x700")
    new_Window.title(f"{folder} - ThunderOwl")
    new_Window.iconbitmap(PATH/"Icons/owl_icon.ico")
    new_Window.resizable(False, False)

    new_Window.transient(window)

    new_Window.rowconfigure(0, weight=1)
    new_Window.columnconfigure(0, weight=1)
    new_Window.columnconfigure(1, weight=5)

    mailListFolderFrame = CTkScrollableFrame(master = new_Window, corner_radius=10, fg_color="#18181B",scrollbar_button_color = "#323742", scrollbar_button_hover_color="#323742", border_width=3, border_color="#323742")
    mailListFolderFrame.grid(row = 0, column = 0, sticky = "nsew")
    #disable(mailListFolderFrame)
    detailMailListFolderFrame = CTkFrame(master = new_Window, fg_color="#18181B", corner_radius=10, border_width=3, border_color="#323742")
    detailMailListFolderFrame.grid(row = 0, column = 1, sticky = "nsew")
    disable(detailMailListFolderFrame)

    with open(PATH/"Database.json", "r") as file:
        database = json.load(file)

    if len(database["User_list"][user]["Mail_box"][folder]["Email_list"]) == 0:
        image_path = PATH/"Icons/letter.png"  # Replace with the path to your image
        image = load_and_resize_image(image_path, 1100, 693)  # Adjust the width and height as needed

        label_second_part = customtkinter.CTkLabel(master = detailMailListFolderFrame, image=image, text = "", anchor = "s")
        label_second_part.pack(padx=3, pady=3)
    
    for index, mail in enumerate(database["User_list"][user]["Mail_box"][folder]["Email_list"]):
        textButton = fixTextForButton(mail["From"], mail["Date"], mail["Subject"], 40)
        mailFolderButton = CTkButton(mailListFolderFrame, height = 40, width = 290, text = textButton, fg_color="#323742", font=("Montserra", 14), hover_color="#1A3145", command=lambda user=user, mail_box = folder, index = index: resolveMail(user, mail_box, index))
        
        if mail["Have_been_read"] == 0:
            mailFolderButton.configure(text_color = "white", font = ("Montserra",14, "bold"))
        else:
            mailFolderButton.configure(fg_color = "#282C34")
        mailFolderButton.pack(pady = 2)

        disable(mailFolderButton)


# ===============================================================================================
# Tắt grid_propate -> frame giữ nguyên không thay đổi kích thước
def disable(frame):
    frame.configure(height=frame["height"],width=frame["width"])
    frame.grid_propagate(0)
# ===================== LẬP TỨC GỬI TOÀN BỘ FILE TEMP_EMAIL.JSON TỚI SERVER ==========================
def send_data_to_server(user):

    with open(PATH/'Temp_email.json', 'r') as f:
        data = json.load(f)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect(ADDR_SMTP)
            response = client.recv(1024).decode()
            print(response)

            # Send EHLO command
            client.sendall(b'EHLO test mail server\n')
            response = client.recv(1024).decode()
            print(response)

            # Send MAIL FROM command
            client.sendall(f'MAIL FROM: <{data["From"]}>\r\n'.encode())
            response = client.recv(1024).decode()
            print(response)

            # Send RCPT TO command
            client.sendall(f'RCPT TO: <{user}>\r\n'.encode())
            response = client.recv(1024).decode()
            print(response)

            # Send DATA command
            client.sendall(b'DATA\r\n')
            response = client.recv(1024).decode()
            print(response)

            # Serialize the JSON data
            with open(PATH/'Temp_email.json', "rb") as attachment:
                attachment_content = attachment.read()
                encoded_content = base64.b64encode(
                    attachment_content).decode()
                # Split the content into lines of a maximum length
                lines = [encoded_content[i:i + 998]
                            for i in range(0, len(encoded_content), 998)]
                # Send each line separately
                for line in lines:
                    client.send((line + '\r\n').encode('utf-8'))

            # Send the end of email content
            client.sendall(b'\r\n.\r\n')
            response = client.recv(1024).decode()
            print(response)

            # Send QUIT
            client.sendall(b'QUIT\r\n')
            response = client.recv(1024).decode()
            print(response)
            print("Send successfully")
        except Exception as e:
            print(f"Error: {e}")
    
# ========================= Phần nhận =========================
def is_valid_string(input_string, list_of_keywords):
    input_string = input_string.lower()
    for keyword in list_of_keywords:
        keyword = keyword.lower()
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b')
        if pattern.search(input_string):
            return True  
    return False 
# ========================== Nhận data ==============================
def recvall(sock):
    BUFF_SIZE = 1024 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def get_data_from_server(user, password, mail_id):
    final = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(ADDR_POP3)
        response = recvall(client_socket).decode()
        print(response)
        # Send USER command
        client_socket.sendall(f'USER {user}\r\n'.encode())
        response = recvall(client_socket).decode()
        print(response)

        # Send PASS command
        client_socket.sendall(f'PASS {password}\r\n'.encode())
        response = recvall(client_socket).decode()
        print(response)

        # Send STAT command to get the number of messages in the mailbox
        client_socket.sendall(b'STAT\r\n')
        response = recvall(client_socket).decode()
        print(response)

        # Send LIST command to get the list of messages and their sizes
        client_socket.sendall(b'LIST\r\n')
        response = recvall(client_socket).decode()
        print(response)

        # Select the first message (you might want to choose a different message number)
        client_socket.sendall(f'RETR {mail_id}\r\n'.encode())
        response = recvall(client_socket)
        final = response.decode()

        # Send QUIT
        client_socket.sendall(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

    print("Email received successfully!")
    return final
def proccess_data_so_we_can_convert_to_json_file(raw_data):
    lines = raw_data.splitlines()
    # Remove the first and last lines
    result_lines = lines[1:-1]
    # Join the remaining lines into a new string
    result_string = '\n'.join(result_lines)

    # Decode
    decoded_string_that_can_be_write_directly_into_json = base64.b64decode(result_string).decode()
    return decoded_string_that_can_be_write_directly_into_json
def write_the_data_received_to_the_temporary_json_file_to_help_us_read_easier(decoded_string_that_can_be_write_directly_into_json):
    with open(PATH/'Buffer.json', 'w') as file:
        file.write(decoded_string_that_can_be_write_directly_into_json)
def clean_the_temporary_json_file_afer_we_done_with_it():
    with open(PATH/'Buffer.json', 'w') as file:
        pass
def choose_which_mail_box_base_on_user_config(user):
    with open(PATH/'database.json', 'r') as file:
        database = json.load(file)
    with open(PATH/'Buffer.json', 'r') as file:
        buffer_json = json.load(file)

    final_mailbox = 'Inbox'
    for condition in database['User_list'][user]['Filter']:
        target_string = None
        if condition['Target'] == 'Subject': # Check the Subject part
            target_string = buffer_json['Subject']
        elif condition['Target'] == 'To':
            target_string = buffer_json['To']
        elif condition['Target'] == 'From':
            target_string = buffer_json['From']
        elif condition['Target'] == 'RawContent':
            target_string = buffer_json['Main_content']['RawContent']
        elif condition['Target'] == 'Subject and RawContent':
            target_string = buffer_json['Subject'] + buffer_json['Main_content']['RawContent']

        # Check điều kiện trên target string
        keyword_list = condition['Key_word']
        valid = is_valid_string(target_string, keyword_list)
        
        if (valid):
            final_mailbox = condition['Mail_box']
            break
    return final_mailbox
# ====================================== Phân tích ======================================================
def after_decided_the_mailbox_now_we_take_the_buffer_json_and_add_it_to_the_database(user, final_mailbox):
    # turn the buffer json into a dictionary
    with open(PATH/'Buffer.json', 'r') as file:
        dict_data = json.load(file)
    with open(PATH/'database.json', 'r') as file:
        database = json.load(file)
    database['User_list'][user]['Mail_box'][final_mailbox]['Email_list'].append(dict_data)
    database['User_list'][user]['Mail_box'][final_mailbox]['Number_of_email'] += 1
    database['User_list'][user]['Mail_box']['Number_of_email_total'] += 1
    with open(PATH/'database.json', 'w') as file:
        json.dump(database, file, indent=2)

def check_to_see_how_many_mail_are_there_in_the_acount_of_the_user(user, password):
    number_of_line = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(ADDR_POP3)
        response = recvall(client_socket).decode()
        print(response)
        # Send USER command
        client_socket.sendall(f'USER {user}\r\n'.encode())
        response = recvall(client_socket).decode()
        print(response)

        # Send PASS command
        client_socket.sendall(f'PASS {password}\r\n'.encode())
        response = recvall(client_socket).decode()
        print(response)

        # Send STAT command to get the number of messages in the mailbox
        client_socket.sendall(b'STAT\r\n')
        response = recvall(client_socket).decode()
        print(response)

        # Send LIST command to get the list of messages and their sizes
        client_socket.sendall(b'LIST\r\n')
        response = recvall(client_socket).decode()
        print(response)
        line_count = len(response.splitlines())
        number_of_line = line_count - 2

        # Send QUIT
        client_socket.sendall(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()
        print(response)
    
    return number_of_line

def get_the_number_of_mail_the_user_already_has(user, password):
    with open(PATH/'database.json', 'r') as file:
        database = json.load(file)
    return database['User_list'][user]['Mail_box']['Number_of_email_total']
# ======================================= Tổng hợp ====================================================
def get_all_the_mail_from_sever_that_has_not_been_dowloaded(user, password):
    mail_in_server = check_to_see_how_many_mail_are_there_in_the_acount_of_the_user(user, password)
    mail_in_database = get_the_number_of_mail_the_user_already_has(user, password)

    for id in range(mail_in_database + 1, mail_in_server + 1):
        data = get_data_from_server(user, password, id)
        decoded_string_that_can_be_write_directly_into_json = proccess_data_so_we_can_convert_to_json_file(data)
        write_the_data_received_to_the_temporary_json_file_to_help_us_read_easier(decoded_string_that_can_be_write_directly_into_json)
        final_mailbox = choose_which_mail_box_base_on_user_config(user)
        after_decided_the_mailbox_now_we_take_the_buffer_json_and_add_it_to_the_database(user, final_mailbox)
        clean_the_temporary_json_file_afer_we_done_with_it()
# ======================================================================================================
# ======================================================================================================

# ========================================================================================
class FileMail:
    def __init__(self, file_name, file_data):
        self.file_name = file_name
        self.file_data = file_data

file_mail_list = []  # List to store FileMail objects

btn_sender = btn_receiver1 = btn_receiver2 = btn_project_receiver1 = btn_project_receiver2 = btn_project = btn_important_receiver1 = btn_important_receiver2 = btn_important = btn_work = btn_work_receiver1 = btn_work_receiver2 = btn_spam = btn_spam_receiver1 = btn_spam_receiver2 = btn_inbox_receiver1 = btn_inbox_receiver2 = None
btn_receive_all = btn_receive_all1 = btn_receive_all2 = None
btn_inbox = None
detailMailListFolderFrame = None

to_entry = None
from_entry = None
subject_entry = None
cc_entry = None
bcc_entry = None
mail_entry = None

buttons = []

image_references = []

tagName = 0
resolveTagName = 0
content_Text = None


def on_entry_click(event, entry_widget):
    entry_widget.configure(border_color = "#84EFB9")

def on_entry_leave(event, entry_widget):
    entry_widget.configure(border_color = "gray")


def load_and_resize_image(file_path, width, height):
    original_image = Image.open(file_path)
    photo_image = customtkinter.CTkImage(original_image, size = (width, height))
    return photo_image

def remove_file_mail(index):
    if 0 <= index < len(file_mail_list):
        removed_file_mail = file_mail_list.pop(index)
        print(f"Removed file: {removed_file_mail.file_name}")

def remove_file_window():
    
    global new_Window, file_mail_list
    remove_Window = CTkToplevel(new_Window)
    remove_Window.geometry("300x350")
    remove_Window.title("Remove - ThunderOwl")
    remove_Window.resizable(False, False)

    remove_Window.transient(new_Window)

    # Create a label to display file list
    label = CTkLabel(remove_Window, text="File Mail List:")
    label.pack(pady=5)

    # Create a listbox to show files
    listbox = tk.Listbox(remove_Window, selectmode=tk.SINGLE)
    for i, file_mail in enumerate(file_mail_list):
        listbox.insert(tk.END, f"{i}: {file_mail.file_name}")
    listbox.pack(pady=10)

    # Create an entry for the user to input the index
    index_entry = tk.Entry(remove_Window, width=15)
    index_entry.pack(pady=10)

    # Create a button to perform removal
    remove_button = customtkinter.CTkButton(
        remove_Window,
        text="Remove",     
        corner_radius=10,
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


def open_edit_window(event):

    global new_Window, edit_menu
    edit_menu = tk.Menu(new_Window, tearoff=0, background="#D6F2FE")
    edit_menu.add_command(label="Cut", command=cut_action)
    edit_menu.add_command(label="Copy", command=copy_action)
    edit_menu.add_command(label="Paste", command=paste_action)
    edit_menu.add_command(label="Select All", command=select_all_action)
    edit_menu.add_command(label="Find", command=find_action)
    edit_menu.add_command(label="Find and Replace", command=find_replace_action)
    edit_menu.post(event.x_root, event.y_root)

def zoomIn_action():
    global mail_entry
    
    _ , current_size = mail_entry.cget("font").split()
    current_size = int(current_size)
    current_size += 1
    mail_entry.configure(font=("Calibri", int(current_size)))

def zoomOut_action():
    global mail_entry
    
    _ , current_size = mail_entry.cget("font").split()
    current_size = int(current_size)
    current_size -= 1
    mail_entry.configure(font=("Calibri", int(current_size)))

def reset_action():
    global mail_entry
    mail_entry.configure(font=("Calibri", 12))

def open_view_window(event):

    global new_Window, view_menu
    view_menu = tk.Menu(new_Window, tearoff=0, background="#D6F2FE")
    view_menu.add_command(label="Zoom In", command=zoomIn_action)
    view_menu.add_command(label="Zoom Out", command=zoomOut_action)
    view_menu.add_command(label="Reset", command=reset_action)
    view_menu.post(event.x_root, event.y_root)


def getIndexImage(event):
    global cursor_index
    cursor_index = mail_entry.index(tk.CURRENT)
    with open(PATH/"Temp_email.json", "r") as file:
        data = json.load(file)
        data["Main_content"]["Image"]["position"].append(cursor_index)
    with open(PATH/"Temp_email.json", "w") as file:
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

        with open(PATH/"Temp_email.json", "r") as file:
            data = json.load(file)
            with open(file_path, "rb") as f:
                image_data = f.read()
                data["Main_content"]["Image"]["data"].append(base64.b64encode(image_data).decode('utf-8'))
            data["Main_content"]["Image"]["width"].append(new_width)
            data["Main_content"]["Image"]["height"].append(new_height)
        with open(PATH/"Temp_email.json", "w") as file:
                json.dump(data, file, indent = 2)

def change_font(font_name):

    global mail_entry, tagName
    print(font_name)
    mail_entry.tag_configure(tagName, font=font_name)
    mail_entry.tag_add(tagName, "sel.first", "sel.last")

    tag_ranges = mail_entry.tag_ranges(tagName)
    tagName = tagName + 1
    if tag_ranges:
        start, end = tag_ranges[0], tag_ranges[1]

        with open(PATH/"Temp_email.json", "r") as file:
            data = json.load(file)
            data["Main_content"]["Font"]["start"].append(str(start))
            data["Main_content"]["Font"]["end"].append(str(end))
            data["Main_content"]["Font"]["NameFont"].append(font_name)
        with open(PATH/"Temp_email.json", "w") as file:
                json.dump(data, file, indent = 2)


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
    global tagName
    mail_entry.tag_configure(tagName, **tag_styles[tag])
            
    # Apply the tag to the selected text
    mail_entry.tag_add(tagName, "sel.first", "sel.last")

    tag_ranges = mail_entry.tag_ranges(tagName)
    tagName = tagName + 1
    if tag_ranges:
        start_index, end_index = tag_ranges[0], tag_ranges[1]
        with open(PATH/"Temp_email.json", "r") as file:
            data = json.load(file)
            data["Main_content"]["Style"][tag]["start"].append(str(start_index))
            data["Main_content"]["Style"][tag]["end"].append(str(end_index))
        with open(PATH/"Temp_email.json", "w") as file:
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


def text_color_action():
    global mail_entry, tagName
    # Get the current selected text
    selected_text = mail_entry.get("sel.first", "sel.last")
    print(selected_text)

    if selected_text:
        # Show color dialog
        color, _ = askcolor()

        if color:
            # Convert RGB values to hex color string
            hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
            
            # Configure the tag with the selected color
            mail_entry.tag_configure(tagName, foreground=hex_color)
            
            # Apply the tag to the selected text
            mail_entry.tag_add(tagName, "sel.first", "sel.last")

            tag_ranges = mail_entry.tag_ranges(tagName)
            tagName = tagName + 1
            if tag_ranges:
                start_index, end_index = tag_ranges[0], tag_ranges[1]
                with open(PATH/"Temp_email.json", "r") as file:
                    data = json.load(file)
                    data["Main_content"]["Color"]["start"].append(str(start_index))
                    data["Main_content"]["Color"]["end"].append(str(end_index))
                    data["Main_content"]["Color"]["colors"].append(str(hex_color))
                with open(PATH/"Temp_email.json", "w") as file:
                        json.dump(data, file, indent = 2)


def open_format_window(event):

    global new_Window, format_menu
    format_menu = tk.Menu(new_Window, tearoff=0, background="#D6F2FE")
    font_sub_menu = tk.Menu(new_Window, tearoff=False)
    format_menu.add_cascade(label="Font", menu=font_sub_menu)
    fonts = ["Arial", "Terminal", "Roman", "Roboto", "Stencil", "Verdana", "Tahoma", "Calibri", "Gigi", "Broadway"
                    , "Wingdings", "Meiryo", "@SimSun", "Georgia", "Impact", "Courier"]
    for font in fonts:
        font_sub_menu.add_command(label=font, command=lambda font = font :change_font(font))

    style_sub_menu = tk.Menu(new_Window, tearoff=False)
    format_menu.add_cascade(label="Style", menu=style_sub_menu)
    styles = ["Bold", "Italic", "Underline", "Strikethrough", "Superscript", "Subscript", "Emphasis", "Code"]
    for style in styles:
        style_sub_menu.add_command(label=style, command=lambda style=style :change_style(style))

    format_menu.add_command(label="Color", command=text_color_action)
    format_menu.post(event.x_root, event.y_root)

new_Window = None
file_menu = None

def close_action():
    global new_Window
    global file_menu

    if new_Window.winfo_exists():
        new_Window.destroy()
    if file_menu.winfo_exists():
        file_menu.destroy()

def saveAs_action():
    # Ask the user for the file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return  # User canceled the file dialog

    # Get the content from the Text widget
    text_content = mail_entry.get("0.0", "end")
    print(text_content)

    # Save the content to the specified file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)


def open_file_window(event):

    global new_Window, file_menu
    file_menu = tk.Menu(new_Window, tearoff=0, background="#D6F2FE")
    file_menu.add_command(label="New", command=newMessage)
    file_menu.add_command(label="Attach", command=attach_file)
    file_menu.add_command(label="Save as", command=saveAs_action)
    file_menu.add_command(label="Close", command=close_action)
    file_menu.post(event.x_root, event.y_root)


def json_fully_complete_now_send_the_json_file_to_server():
    global from_entry, to_entry, mail_entry, cc_entry, bcc_entry, file_mail_list

    with open(PATH/"Temp_email.json", "r") as file:
        data = json.load(file)
        data["Main_content"]["RawContent"] = mail_entry.get("0.0", "end")
    with open(PATH/"Temp_email.json", "w") as file:
            json.dump(data, file, indent = 2)


    with open(PATH/"Temp_email.json", "r") as file:
        data = json.load(file)   
        data["From"] = from_entry.get()
        data["Subject"] = subject_entry.get()
        data["Date"] = get_date()

        data["To"] = to_entry.get()

        cc_list = cc_entry.get().split()
        for name in cc_list:
            data["Cc"].append(name)

        if not file_mail_list:
            data["Content_type"] = "json"
        else:
            data["Content_type"] = "multipart/mixed"
            
            for file in file_mail_list:
                file_content = base64.b64encode(file.file_data).decode('utf-8')
                file_content_type = file.file_name.split(".")[-1]
                file_name = file.file_name

                file_block = {
                    "File_content": file_content,
                    "File_content_type": file_content_type,
                    "File_name": file_name
                }
                data["File_list"].append(file_block) 

    with open(PATH/'Temp_email.json', 'w') as file:
        json.dump(data, file, indent=2)

    to_user_list = data["To"].split()
    for user in to_user_list:
        send_data_to_server(user)
    
    for user in data["Cc"]:
        send_data_to_server(user)

    bcc_list = bcc_entry.get().split()
    data["Cc"].clear()
    with open(PATH/'Temp_email.json', 'w') as file:
        json.dump(data, file, indent=2)
    for user in bcc_list:
        send_data_to_server(user)

    # Đưa file json tạm về trạng thái ban đầu
    with open(PATH/'Temp_email.json', 'w') as f:
        json.dump(data_copy, f, indent= 2)

def button_toolbar_clicked(button_name):
    global buttons
    print(f"Toolbar button {button_name} clicked!")
    if(button_name == "File"):
        buttons[0].bind("<Button-1>", open_file_window)
    if (button_name == "Edit"):
        buttons[1].bind("<Button-1>", open_edit_window)
    if(button_name == "View"):
        buttons[2].bind("<Button-1>", open_view_window)
    if(button_name == "Attach"):
        attach_file()
    if(button_name == "Remove"):
        remove_file_window()
    if(button_name == "Image"):
        insert_image()
    if(button_name == "Format"):
        buttons[5].bind("<Button-1>", open_format_window)
    if(button_name == "Send"):
        json_fully_complete_now_send_the_json_file_to_server()

def button_clicked(button_name):
    print(f"{button_name} clicked!")

def on_button_click(button_name):
    print(f"{button_name} clicked!")

    label_second_part.pack_forget()   
    if button_name=="Mail":
        dowload_email_every_1_minute_thread = threading.Thread(target=dowload_email_every_1_minute_thread_function)
        dowload_email_every_1_minute_thread.start()
        create_mail_subframe()
    elif button_name=="Sign out":
        window.destroy()
    elif button_name=="Calendar":
        create_calendar_subframe()

def create_button_with_image(parent, file_path, width, height, button_name):
    image = load_and_resize_image(file_path, width, height)
    button = customtkinter.CTkButton(
        parent,
        image=image,
        text = button_name,
        corner_radius=7,
        command=lambda: on_button_click(button_name),
        anchor="w",
    )
    button.configure(width = width, height = height)

    if button_name == "Download":
        button.configure(text = "")
    if button_name == "Logo":
        button.configure(font = ("Arial", 15))
    return button, image

def create_button_with_image_senDown(parent, file_path, width, height, button_name, user, command=None):
    image = load_and_resize_image(file_path, width, height)
    button = customtkinter.CTkButton(
        parent,
        text=button_name,
        image=image,
        cursor="hand2",
        corner_radius=10,
        command=command,
        anchor="w",
    )

    #if(button)
    if(button_name!="hungm0434@gmail.com" and button_name != "hahuy@gmail.com" and button_name != "hoangkhang@gmail.com"):
        button.configure(font=("Montserrat", 12, "bold"),
        fg_color = "#282C34",
        hover_color = "#484F60",
        text_color = "#979EAF"
    )
        
    if(button_name!="hungm0434@gmail.com" and button_name != "hahuy@gmail.com" and button_name != "hoangkhang@gmail.com" and button_name != "Download"):
        with open(PATH/"database.json", "r") as file:
            database = json.load(file)
        
        unreadMail = 0
        for data in database["User_list"][user]["Mail_box"][button_name]["Email_list"]:
            if data["Have_been_read"] == 0:
                unreadMail += 1

        if unreadMail != 0:
            button.configure(text = button_name + f'  ({unreadMail})')
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

def newMessage():
    global to_entry, subject_entry, cc_entry, bcc_entry, mail_entry, from_entry
    global buttons
    global new_Window
    global file_mail_list

    file_mail_list = []

    new_Window = CTkToplevel(window)
    new_Window.geometry("950x600")
    new_Window.title("Write - ThunderOwl")
    new_Window.iconbitmap(PATH/"Icons/owl_icon.ico")
    new_Window.resizable(False, False)

    new_Window.transient(window)

    # Toolbar frame (top)
    new_Window.columnconfigure(0, weight=1)

    toolbar_frame = CTkFrame(new_Window, border_color="#7cbf86", border_width=1, fg_color="#282C34")
    toolbar_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Create buttons for the toolbar
    buttons = []
    button_names = ["File", "Edit", "View", "Image", "Attach", "Format", "Tools", "Help", "Send", "Remove"]

    for name in button_names:
        button = customtkinter.CTkButton(toolbar_frame, text=name, corner_radius=5, height=30, width=50, command=lambda n=name: button_toolbar_clicked(n), fg_color= "#323742", text_color= "#AAB0BE", hover_color="#484F60")
        button.pack(side="left", padx=5, pady=5)
        buttons.append(button)
    
    
    buttons[8].pack(side="right", padx=20, pady=5)
    # Create textboxes and buttons

    field_frame = CTkFrame(new_Window, border_color="#7cbf86", border_width=1, fg_color="#282C34")
    field_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=0)

    field_frame.rowconfigure(5, weight=1)
    field_frame.columnconfigure(0, weight=1)
    field_frame.columnconfigure(1, weight=30)

    from_label = customtkinter.CTkLabel(field_frame, text="From:", font=("Arial", 15), fg_color="#282C34", text_color="white")
    from_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

    from_entry = CTkEntry(field_frame, placeholder_text="From", width = 800, fg_color="#323742")
    from_entry.grid(row=0, column=1, pady=5, padx=0, sticky="w")

    from_entry.bind("<FocusIn>", lambda event: on_entry_click(event, from_entry))
    from_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, from_entry))

    # First text box
    to_entry = CTkEntry(field_frame, placeholder_text="To", width = 800, fg_color="#323742")
    to_entry.grid(row=1, column=1, sticky="w", pady=2, padx = 0)
    to_entry.bind("<FocusIn>", lambda event: on_entry_click(event, to_entry))
    to_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, to_entry))
    to_label = customtkinter.CTkLabel(field_frame, text="To:", font=("Arial", 15), fg_color="#282C34", text_color="white")
    to_label.grid(row=1, column=0, pady=2, padx=10, sticky="w")
    # Second text box
    subject_entry = CTkEntry(field_frame, placeholder_text="Subject", width = 800, fg_color="#323742")
    subject_entry.grid(row=2, column=1, sticky="w", pady=5)
    subject_entry.bind("<FocusIn>", lambda event: on_entry_click(event, subject_entry))
    subject_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, subject_entry))
    subject_label = customtkinter.CTkLabel(field_frame, text="Subject:", font=("Arial", 15), fg_color="#282C34", text_color="white")
    subject_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

    cc_entry = CTkEntry(field_frame, placeholder_text="Cc", width = 800, fg_color="#323742")
    cc_entry.grid(row=3, column=1, sticky="w", pady=2)
    cc_entry.bind("<FocusIn>", lambda event: on_entry_click(event, cc_entry))
    cc_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, cc_entry))
    cc_label = customtkinter.CTkLabel(field_frame, text="Cc:", font=("Arial", 15), fg_color="#282C34", text_color="white")
    cc_label.grid(row=3, column=0, pady=2, padx=10, sticky="w")

    bcc_entry = CTkEntry(field_frame, placeholder_text="Bcc", width = 800, fg_color="#323742")
    bcc_entry.grid(row=4, column=1, sticky="w", pady=5)
    bcc_entry.bind("<FocusIn>", lambda event: on_entry_click(event, bcc_entry))
    bcc_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, bcc_entry))
    bcc_label = customtkinter.CTkLabel(field_frame, text="Bcc:", font=("Arial", 15), fg_color="#282C34", text_color="white")
    bcc_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")


    text_mail_frame = CTkFrame(new_Window, border_color="#282C34", border_width=2, fg_color = "#84EFB9", corner_radius=10, height=330, width=100)
    text_mail_frame.grid(row=2, column=0, sticky="nsew", padx=3, pady=2)
    disable(text_mail_frame)

    text_mail_frame.rowconfigure(0, weight=1)
    text_mail_frame.columnconfigure(0, weight=1)
    
    mail_entry = tk.Text(text_mail_frame, bd=1, relief="solid", borderwidth=2, background="#282C34", foreground="white", insertbackground="white")
    mail_entry.grid(row=0, column=0, sticky="nsew", padx = 3, pady=3)
    mail_entry.configure(font=("Calibri", 12))


def toggle_additional_buttons(button_name):
    global btn_sender, btn_receiver1, btn_receiver2, btn_project_receiver1, btn_project_receiver2, btn_project, btn_important_receiver1, btn_important_receiver2, btn_important, btn_work, btn_work_receiver1, btn_work_receiver2, btn_spam, btn_spam_receiver1, btn_spam_receiver2, btn_inbox, btn_inbox_receiver1, btn_inbox_receiver2, btn_receive_all, btn_receive_all1, btn_receive_all2
    if button_name == "hungm0434@gmail.com":
        if btn_inbox.winfo_ismapped():
            btn_inbox.grid_forget()
            btn_spam.grid_forget()
            btn_work.grid_forget()
            btn_important.grid_forget()
            btn_project.grid_forget()
            btn_receive_all.grid_forget()
        else:
            btn_receive_all.grid(row=1, column=0, pady=5)
            btn_inbox.grid(row=2, column=0, pady=5)
            btn_spam.grid(row=3, column=0, pady=5)
            btn_work.grid(row=4, column=0, pady=5)
            btn_important.grid(row=5, column=0, pady=5)
            btn_project.grid(row=6, column=0, pady=5)

    elif button_name == "hahuy@gmail.com":
        if btn_inbox_receiver1.winfo_ismapped():
            btn_inbox_receiver1.grid_forget()
            btn_spam_receiver1.grid_forget()
            btn_work_receiver1.grid_forget()
            btn_important_receiver1.grid_forget()
            btn_project_receiver1.grid_forget()
            btn_receive_all1.grid_forget()

        else:
            btn_receive_all1.grid(row=8, column=0, pady=5)
            btn_inbox_receiver1.grid(row=9, column=0, pady=5)
            btn_spam_receiver1.grid(row=10, column=0, pady=5)
            btn_work_receiver1.grid(row=11, column=0, pady=5)
            btn_important_receiver1.grid(row=12, column=0, pady=5)
            btn_project_receiver1.grid(row=13, column=0, pady=5)
    elif button_name == "hoangkhang@gmail.com":
        if btn_inbox_receiver2.winfo_ismapped():
            btn_inbox_receiver2.grid_forget()
            btn_spam_receiver2.grid_forget()
            btn_work_receiver2.grid_forget()
            btn_important_receiver2.grid_forget()
            btn_project_receiver2.grid_forget()
            btn_receive_all2.grid_forget()

        else:
            btn_receive_all2.grid(row=15, column=0, pady=5)
            btn_inbox_receiver2.grid(row=16, column=0, pady=5)
            btn_spam_receiver2.grid(row=17, column=0, pady=5)
            btn_work_receiver2.grid(row=18, column=0, pady=5)
            btn_important_receiver2.grid(row=19, column=0, pady=5)
            btn_project_receiver2.grid(row=20, column=0, pady=5)


def create_second_part():

    global label_second_part, second_part_frame
    second_part_frame = CTkFrame(master=window, border_color="#323742", border_width=2)
    second_part_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    image_path = PATH/"Icons/Thunder.png"  # Replace with the path to your image
    image = load_and_resize_image(image_path, 1230, 769)  # Adjust the width and height as needed

    label_second_part = customtkinter.CTkLabel(master = second_part_frame, image=image, text = "", anchor = "s")
    label_second_part.pack(padx=4, pady=4)


def create_mail_subframe():
    global btn_sender, btn_receiver1, btn_receiver2, btn_project_receiver2, btn_project_receiver1, btn_project, btn_important_receiver1, btn_important_receiver2, btn_important, btn_work, btn_work_receiver1, btn_work_receiver2, btn_spam, btn_spam_receiver1, btn_spam_receiver2, btn_inbox, btn_inbox_receiver1, btn_inbox_receiver2, btn_receive_all, btn_receive_all1, btn_receive_all2
    global second_part_frame

    second_part_frame.destroy()

    second_subframe = customtkinter.CTkFrame(window, fg_color="#282C34")
    second_subframe.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    second_subframe.columnconfigure(0, weight=1)  # Part 1
    second_subframe.columnconfigure(1, weight=20)  # Part 2
    second_subframe.rowconfigure(0, weight=1)

    whitesubframe = customtkinter.CTkFrame(second_subframe, fg_color="#282C34", corner_radius=15)
    whitesubframe.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    disable(whitesubframe)

    graysubframe = customtkinter.CTkFrame(second_subframe, border_width=3, border_color="#323742", fg_color="white")
    graysubframe.grid(row=0, column=1, sticky="nsew", padx=3, pady=2)
    image_path = PATH/"Icons/thankYou.png"  # Replace with the path to your image
    image = load_and_resize_image(image_path, 975, 690)  # Adjust the width and height as needed
    disable(whitesubframe)

    label_second_part = customtkinter.CTkLabel(master = graysubframe, image=image, text = "", anchor = "s")
    label_second_part.pack(padx=3, pady=3)


    whitesubframe.rowconfigure(1, weight=1)  # Part 1
    whitesubframe.rowconfigure(0, weight=25)
    whitesubframe.columnconfigure(0, weight=1)  # Part 2

    sendown_frame = customtkinter.CTkFrame(whitesubframe, fg_color="#1E2128")
    sendown_frame.grid(row=1, column=0, sticky="nsew", padx = 2, pady=0)

    email_frame = customtkinter.CTkScrollableFrame(whitesubframe, fg_color="#1E2128", scrollbar_button_color = "#323742", scrollbar_button_hover_color="#323742", border_width=2, border_color="#282C34")
    email_frame.grid(row=0, column=0, sticky="nsew", padx = 2, pady=2)

    button_inside_whitesubframe = customtkinter.CTkButton(sendown_frame, text="+ NEW MESSAGE" ,font = ("Montserrat", 15), fg_color="#00CCC7", corner_radius=12, height=50, anchor = "center", command=lambda: newMessage(), text_color="black")
    button_inside_whitesubframe.grid(row=0, column=0, sticky="nse", padx=36, pady=25)


    btn_sender = create_button_with_image_senDown(email_frame, PATH/'Icons/mail.png', 20, 20, 'hungm0434@gmail.com', 'hungm0434@gmail.com', lambda user = "hungm0434@gmail.com": toggle_additional_buttons(user))
    btn_sender.configure(font=("Montserrat", 12, "bold"), anchor = "w", height = 40, fg_color = "#323742", hover_color = "#484F60", text_color = "#AAB0BE")   
    btn_sender.grid(row=0, column=0, sticky="nsew", padx = 5, pady=5)

    btn_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/mail.png', 20, 20, 'hahuy@gmail.com','hungm0434@gmail.com', lambda user = "hahuy@gmail.com": toggle_additional_buttons(user))
    btn_receiver1.configure(font=("Montserrat", 12, "bold"), anchor = "w", height = 40, fg_color = "#323742", hover_color = "#484F60", text_color = "#AAB0BE")   
    btn_receiver1.grid(row=7, column=0, sticky="nsew", padx = 5, pady=5)

    btn_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/mail.png', 20, 20, 'hoangkhang@gmail.com', 'hungm0434@gmail.com',lambda user = "hoangkhang@gmail.com": toggle_additional_buttons(user))
    btn_receiver2.configure(font=("Montserrat", 12, "bold"), anchor = "w", height = 40, fg_color = "#323742", hover_color = "#484F60", text_color = "#AAB0BE")   
    btn_receiver2.grid(row=14, column=0, sticky="nsew", padx = 5, pady=5)



    # Create buttons 4 and 5 with icons but initially hide them
    btn_receive_all = create_button_with_image_senDown(email_frame, PATH/'Icons/download.png', 20, 20, 'Download', "hungm0434@gmail.com", lambda user="hungm0434@gmail.com": get_all_the_mail_from_sever_that_has_not_been_dowloaded(user, 123))
    btn_receive_all.pack_forget()
    btn_inbox = create_button_with_image_senDown(email_frame, PATH/'Icons/inbox.png', 20, 20, 'Inbox',"hungm0434@gmail.com", lambda user="hungm0434@gmail.com": getFolderMessage(user, 'Inbox'))
    btn_inbox.pack_forget()
    btn_project = create_button_with_image_senDown(email_frame, PATH/'Icons/project_icon.png', 20, 20, 'Project',"hungm0434@gmail.com",lambda user="hungm0434@gmail.com": getFolderMessage(user, 'Project'))
    btn_project.pack_forget()
    btn_work = create_button_with_image_senDown(email_frame, PATH/'Icons/work_icon.png', 20, 20, 'Work',"hungm0434@gmail.com",lambda user="hungm0434@gmail.com": getFolderMessage(user, 'Work'))
    btn_work.pack_forget()
    btn_important = create_button_with_image_senDown(email_frame, PATH/'Icons/important_icon.png', 20, 20, 'Important', "hungm0434@gmail.com",lambda user="hungm0434@gmail.com": getFolderMessage(user, 'Important'))
    btn_important.pack_forget()
    btn_spam = create_button_with_image_senDown(email_frame, PATH/'Icons/spam_icon.png', 20, 20, 'Spam', "hungm0434@gmail.com",lambda user="hungm0434@gmail.com": getFolderMessage(user, 'Spam'))
    btn_spam.pack_forget()

    
    btn_receive_all1 = create_button_with_image_senDown(email_frame, PATH/'Icons/download.png', 20, 20, 'Download',"hahuy@gmail.com", lambda user="hahuy@gmail.com": get_all_the_mail_from_sever_that_has_not_been_dowloaded(user, 123))
    btn_receive_all1.pack_forget()
    btn_inbox_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/inbox.png', 20, 20, 'Inbox',"hahuy@gmail.com", lambda user="hahuy@gmail.com": getFolderMessage(user, 'Inbox'))
    btn_inbox_receiver1.pack_forget()
    btn_work_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/work_icon.png', 20, 20, 'Work',"hahuy@gmail.com", lambda user="hahuy@gmail.com": getFolderMessage(user, 'Work'))
    btn_work_receiver1.pack_forget()
    btn_spam_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/spam_icon.png', 20, 20, 'Spam',"hahuy@gmail.com", lambda user="hahuy@gmail.com": getFolderMessage(user, 'Spam'))
    btn_spam_receiver1.pack_forget()
    btn_important_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/important_icon.png', 20, 20, 'Important',"hahuy@gmail.com", lambda user="hahuy@gmail.com": getFolderMessage(user, 'Important'))
    btn_important_receiver1.pack_forget()
    btn_project_receiver1 = create_button_with_image_senDown(email_frame, PATH/'Icons/project_icon.png', 20, 20, 'Project', "hahuy@gmail.com",lambda user="hahuy@gmail.com": getFolderMessage(user, 'Project'))
    btn_project_receiver1.pack_forget()

    btn_receive_all2 = create_button_with_image_senDown(email_frame, PATH/'Icons/download.png', 20, 20, 'Download',"hoangkhang@gmail.com", lambda user="hoangkhang@gmail.com": get_all_the_mail_from_sever_that_has_not_been_dowloaded(user, 123))
    btn_receive_all2.pack_forget()
    btn_inbox_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/inbox.png', 20, 20, 'Inbox',"hoangkhang@gmail.com", lambda user="hoangkhang@gmail.com": getFolderMessage(user, 'Inbox'))
    btn_inbox_receiver2.pack_forget()
    btn_work_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/work_icon.png', 20, 20, 'Work',"hoangkhang@gmail.com", lambda user="hoangkhang@gmail.com": getFolderMessage(user, 'Work'))
    btn_work_receiver2.pack_forget()
    btn_spam_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/spam_icon.png', 20, 20, 'Spam', "hoangkhang@gmail.com",lambda user="hoangkhang@gmail.com": getFolderMessage(user, 'Spam'))
    btn_spam_receiver2.pack_forget()
    btn_important_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/important_icon.png', 20, 20, 'Important', "hoangkhang@gmail.com",lambda user="hoangkhang@gmail.com": getFolderMessage(user, 'Important'))
    btn_important_receiver2.pack_forget()
    btn_project_receiver2 = create_button_with_image_senDown(email_frame, PATH/'Icons/project_icon.png', 20, 20, 'Project', "hoangkhang@gmail.com",lambda user="hoangkhang@gmail.com": getFolderMessage(user, 'Project'))
    btn_project_receiver2.pack_forget()



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

    open_cal = customtkinter.CTkButton(left_frame, text="Select Date",corner_radius=10,  command=lambda: select_date(mycal, selected_date_label))
    open_cal.pack(padx=15, pady=15)

def create_buttons_frame():
    buttons_frame = CTkFrame(master = window, fg_color="#282C34")
    buttons_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    buttons_frame.rowconfigure(0, weight=20)
    buttons_frame.rowconfigure(1, weight=1)
    buttons_frame.columnconfigure(0, weight=1)
 
    buttons_sub_frame = CTkFrame(master = buttons_frame, fg_color="#282C34", border_color="#323742", border_width=3, corner_radius=10, height=600)
    buttons_sub_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    logout_frame = CTkFrame(master = buttons_frame, border_color="#323742", border_width=3, fg_color="#282C34")
    logout_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
    btn_logout = CTkButton(logout_frame, text='Sign out')
    btn_logout.configure(fg_color = "#282C34", text_color = "#AAB0BE", font=("Montserrat", 15), height = 35, hover_color = "#282C34", cursor = "hand2", command = lambda: on_button_click("Sign out"))
    # Create buttons with images
    global buttons

    btn_logo, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/owl.png', 60, 60, '')
    btn_logo.configure(fg_color = "#282C34", state = "disabled", anchor = "center")
    btn_text = CTkButton(buttons_sub_frame, text = 'THUNDER OWL', fg_color = "#282C34", state = "disabled", text_color_disabled = "#00CCC7", font = ("Montserrat Medium", 14))
    btn_mail, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/mail.png', 29, 29, 'Mail')
    btn_mail.configure(fg_color = "#323742", text_color = "#AAB0BE", font=("Montserrat", 15), height = 50, width=100, hover_color = "#484F60")
    disable(btn_mail)
    btn_address_book, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/phone-book.png', 30, 30, 'Address')
    btn_address_book.configure(fg_color = "#323742", text_color = "#AAB0BE", font=("Montserrat", 15),  height = 50, hover_color = "#484F60")
    btn_calendar, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/calendar.png', 30, 30, 'Calendar')
    btn_calendar.configure(fg_color = "#323742", text_color = "#AAB0BE", font=("Montserrat", 15),  height = 50,hover_color = "#484F60")
    btn_task, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/list.png', 30, 30, 'Task')
    btn_task.configure(fg_color = "#323742", text_color = "#AAB0BE", font=("Montserrat", 15),  height = 50 , hover_color = "#484F60")
    btn_chat, _ = create_button_with_image(buttons_sub_frame, PATH/'Icons/chat.png', 30, 30, 'Chat')
    btn_chat.configure(fg_color = "#323742", text_color = "#AAB0BE", font=("Montserrat", 15),  height = 50 , hover_color = "#484F60")
    
    
    btn_logo.grid(row=0, column=0, sticky="nsew", padx=13, pady=2)
    btn_text.grid(row=1, column=0, sticky="nsew", padx=13, pady=2)
    btn_mail.grid(row=2, column=0, sticky="nsew", padx=13, pady=3)
    btn_address_book.grid(row=3, column=0, sticky="nsew", padx=13, pady=3)
    btn_calendar.grid(row=4, column=0, sticky="nsew", padx=13, pady=3)
    btn_task.grid(row=5, column=0, sticky="nsew", padx=13, pady=3)
    btn_chat.grid(row=6, column=0, sticky="nsew", padx=13, pady=3)
    btn_logout.grid(row=7, column=0, sticky="nsew", padx=10, pady=20)
    buttons.append([btn_logo, btn_mail, btn_address_book, btn_calendar, btn_task, btn_chat, btn_logout])

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Thunder-Owl")
window.geometry("1400x700")
window.iconbitmap(PATH/"Icons/owl_icon.ico")
window.resizable(False, False)

# Set up grid weights for resizable behavior
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight = 1)
window.columnconfigure(1, weight = 3)

create_second_part() # Image
# Create buttons frame (Part 1)
create_buttons_frame()

window.mainloop()
