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

            # Send the HELO or EHLO command
            helo_command = "EHLO client\r\n"  # You can use HELO instead of EHLO if needed
            client.send(helo_command.encode('utf-8'))

            # Receive and print the server's response to the HELO or EHLO command
            helo_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {helo_response}")

            # Send the MAIL FROM command
            mail_from_command = "MAIL FROM: <your_email@example.com>\r\n"
            client.send(mail_from_command.encode('utf-8'))

            # Receive and print the server's response to the MAIL FROM command
            mail_from_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {mail_from_response}")

            # Send the RCPT TO command
            rcpt_to_command = "RCPT TO: <recipient_email@example.com>\r\n"
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

        self.sender_label = tk.Label(master, text="Sender:")
        self.sender_entry = tk.Entry(master)
        self.sender_label.pack()
        self.sender_entry.pack()

        self.recipient_label = tk.Label(master, text="Recipient:")
        self.recipient_entry = tk.Entry(master)
        self.recipient_label.pack()
        self.recipient_entry.pack()

        self.subject_label = tk.Label(master, text="Subject:")
        self.subject_entry = tk.Entry(master)
        self.subject_label.pack()
        self.subject_entry.pack()

        self.message_label = tk.Label(master, text="Message:")
        self.message_entry = tk.Text(master, height=5, width=30)
        self.message_label.pack()
        self.message_entry.pack()

        self.send_mail_button = tk.Button(master, text="Send Mail", command=self.connect_server)
        self.send_mail_button.pack(pady=10)

    def connect_server(self):
        try:
            sender = self.sender_entry.get()
            recipient = self.recipient_entry.get()
            subject = self.subject_entry.get()
            message = self.message_entry.get("1.0", "end-1c")

            # Check if any of the required fields is empty
            if not all([sender, recipient, subject, message]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return

            # Construct the email content
            email_content = f"Subject: {subject}\r\nFrom: {sender}\r\nTo: {recipient}\r\n\r\n{message}\r\n.\r\n"

            # Send the email content to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((socket.gethostbyname(socket.gethostname()), 2225))
                client.sendall(email_content.encode('utf-8'))

            messagebox.showinfo("Success", "Mail sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error sending mail: {e}")

def main():
    root = tk.Tk()
    app = MailApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
