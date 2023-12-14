import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class MailApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mail App")

        # Initialize some sample data
        self.emails = [
            {"sender": "john.doe@example.com", "subject": "Meeting Tomorrow", "read": False},
            {"sender": "jane.smith@example.com", "subject": "Vacation Plans", "read": True},
            # Add more sample emails as needed
        ]

        # Create GUI components
        self.create_menu()
        self.create_email_list()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Compose Email", command=self.compose_email)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_email_list(self):
        self.email_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.email_listbox.pack(pady=10)

        for email in self.emails:
            status_icon = "🔴" if not email["read"] else "🟢"
            self.email_listbox.insert(tk.END, f"{status_icon} {email['sender']} - {email['subject']}")

        self.email_listbox.bind("<Double-Button-1>", self.open_email)

    def compose_email(self):
        sender = simpledialog.askstring("Compose Email", "Enter sender email:")
        subject = simpledialog.askstring("Compose Email", "Enter subject:")
        content = simpledialog.askstring("Compose Email", "Enter email content:", widget=tk.Text)

        if sender and subject and content:
            new_email = {"sender": sender, "subject": subject, "read": False}
            self.emails.append(new_email)
            self.update_email_list()
            messagebox.showinfo("Compose Email", "Email sent successfully!")

    def open_email(self, event):
        selected_index = self.email_listbox.curselection()
        if selected_index:
            selected_email = self.emails[selected_index[0]]
            selected_email["read"] = True
            self.update_email_list()
            messagebox.showinfo("Email Details", f"Sender: {selected_email['sender']}\nSubject: {selected_email['subject']}")

    def show_about(self):
        about_text = "Mail App\nVersion 1.0\n\nDeveloped by Your Name"
        messagebox.showinfo("About", about_text)

    def update_email_list(self):
        self.email_listbox.delete(0, tk.END)
        for email in self.emails:
            status_icon = "🔴" if not email["read"] else "🟢"
            self.email_listbox.insert(tk.END, f"{status_icon} {email['sender']} - {email['subject']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MailApp(root)
    root.mainloop()
