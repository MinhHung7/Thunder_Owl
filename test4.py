import socket
import tkinter as tk
from tkinter import messagebox

IP = socket.gethostbyname(socket.gethostname())
PORT = 2225
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def connect_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect(ADDR)
            print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

            # Receive and print the server's initial response
            initial_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {initial_response}")

            # # Send the HELO or EHLO command
            # helo_command = "EHLO client\r\n"  # You can use HELO instead of EHLO if needed
            # client.send(helo_command.encode('utf-8'))

            # # Receive and print the server's response to the HELO or EHLO command
            # helo_response = client.recv(1024).decode('utf-8')
            # print(f"[SERVER] {helo_response}")

            # Send the MAIL FROM command
            # mail_from_command = "MAIL FROM: <your_email@example.com>\r\n"
            # client.send(mail_from_command.encode('utf-8'))

            # # Receive and print the server's response to the MAIL FROM command
            # mail_from_response = client.recv(1024).decode('utf-8')
            # print(f"[SERVER] {mail_from_response}")

            # Send the RCPT TO command
            rcpt_to_command = input()
            rcpt_to_command = "RCPT TO: " + rcpt_to_command + "\r\n"
            client.send(rcpt_to_command.encode('utf-8'))

            # Receive and print the server's response to the RCPT TO command
            rcpt_to_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {rcpt_to_response}")

            # Send data command
            data_command = "DATA\r\n"
            client.send(data_command.encode('utf-8'))

            # Receive and print the server's response to the DATA command
            data_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {data_response}")

            # Send the message data
            message_data = (
                "Subject: Your Subject\r\n"
                "From: your_email@example.com\r\n"
                "To: recipient_email@example.com\r\n"
                "\r\n"
                "Your email content goes here.\r\n"
                ".\r\n"  # This dot indicates the end of the message
            )
            client.send(message_data.encode('utf-8'))

            # Receive and print the server's response to the message data
            message_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {message_response}")

            # Send the QUIT command
            quit_command = "QUIT\r\n"
            client.send(quit_command.encode('utf-8'))

            # Receive and print the server's response to the QUIT command
            quit_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {quit_response}")

        except Exception as e:
            print(f"Error: {e}")

class MailApp:
    def __init__(self, master):
        self.master = master
        master.title("Mail Application")

        self.connect_button = tk.Button(master, text="Connect to Server", command=self.connect_server)
        self.connect_button.pack(pady=10)

        self.send_mail_button = tk.Button(master, text="Send Mail", command=self.send_mail)
        self.send_mail_button.pack(pady=10)

    def connect_server(self):
        try:
            # Call your existing connect_server function here
            connect_server()
            messagebox.showinfo("Success", "Connected to the server successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the server: {e}")

    def send_mail(self):
        try:
            # Call your existing connect_server function here
            connect_server()
            messagebox.showinfo("Success", "Mail sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error sending mail: {e}")

def main():
    root = tk.Tk()
    app = MailApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
