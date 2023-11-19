import smtplib
import ssl
from tkinter import Tk, Label, Entry, Button, Text, messagebox

smtp_port = 587
smtp_server = "smtp.gmail.com"
email_from = "hungm0434@gmail.com"
pswd = "gktlrndfkgadbacv"
simple_email_context = ssl.create_default_context()


def send_email(to, cc, bcc, subject, message):
    try:
        # Connect to the server
        print("Connecting to server...")
        with smtplib.SMTP(smtp_server, smtp_port) as TIE_server:
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pswd)
            print("Connected to server :-)")
            
            # Construct the message headers
            headers = f"To: {to}\n"
            if cc:
                headers += f"CC: {cc}\n"
            if bcc:
                headers += f"BCC: {bcc}\n"
            headers += f"Subject: {subject}\n\n"
            
            # Send the actual email
            print()
            print(f"Sending email to - {to}")
            TIE_server.sendmail(email_from, [to] + (cc.split(',') if cc else []) + (bcc.split(',') if bcc else []), headers + message)
            print(f"Email successfully sent to - {to}")
            messagebox.showinfo("Success", f"Email sent to {to} successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI setup
def send_email_from_gui():
    to = entry_email_to.get()
    cc = entry_cc.get()
    bcc = entry_bcc.get()
    subject = entry_subject.get()
    message = text_message.get("1.0", "end-1c")

    send_email(to, cc, bcc, subject, message)

root = Tk()
root.title("Email Sender")

# Labels
Label(root, text="To Email:").grid(row=0, column=0, pady=10)
Label(root, text="CC:").grid(row=1, column=0, pady=10)
Label(root, text="BCC:").grid(row=2, column=0, pady=10)
Label(root, text="Subject:").grid(row=3, column=0, pady=10)
Label(root, text="Message:").grid(row=5, column=0, pady=10)

# Entry widgets
entry_email_to = Entry(root, width=30)
entry_cc = Entry(root, width=30)
entry_bcc = Entry(root, width=30)
entry_subject = Entry(root, width=40)
text_message = Text(root, height=10, width=40)

# Place entry widgets on the grid
entry_email_to.grid(row=0, column=1)
entry_cc.grid(row=1, column=1)
entry_bcc.grid(row=2, column=1)
entry_subject.grid(row=3, column=1)
text_message.grid(row=5, column=1)

# Button to send email
send_button = Button(root, text="Send Email", command=send_email_from_gui)
send_button.grid(row=6, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
