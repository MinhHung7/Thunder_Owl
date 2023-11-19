import tkinter as tk

def create_frames():
    whitesubframe = tk.Frame(window, bg="white", bd=1, relief="solid")
    whitesubframe.grid(row=0, column=0, sticky="nsew")

    sendown_frame = tk.Frame(whitesubframe, bg="gray", bd=1, relief="solid")
    sendown_frame.grid(row=0, column=0, sticky="new")
    sendown_label = tk.Label(sendown_frame, text='A', bg="gray", width=40, height=5)
    sendown_label.grid(row=0, column=0, padx=0, pady=0)

    email_frame = tk.Frame(whitesubframe, bg="white", bd=1, relief="solid")
    email_frame.grid(row=1, column=0, sticky="new")
    email_label = tk.Label(email_frame, text='B', bg="white", width=40, height=5)
    email_label.grid(row=0, column=0, padx=0, pady=0)

window = tk.Tk()
window.title("Test")
window.geometry("400x400")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

create_frames()

window.mainloop()