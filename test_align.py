import tkinter as tk

class MyMailApp:
    def __init__(self, master):
        self.master = master
        self.mail_entry = tk.Text(master)
        # Other initialization code...

    def align_action(self, alignment):
        selected_text = self.mail_entry.get(tk.SEL_FIRST, tk.SEL_LAST)

        if not selected_text:
            return

        self.mail_entry.tag_configure(alignment, lmargin1=0, lmargin2=0, rmargin=self.mail_entry.winfo_width())
        self.mail_entry.tag_add(alignment, tk.SEL_FIRST, tk.SEL_LAST)

    def open_align_window(self):
        align_window = tk.Toplevel(self.master)
        align_window.title("Align Options")

        button_width = 15

        options = [("Left", tk.LEFT), ("Center", tk.CENTER), ("Right", tk.RIGHT), ("Justify", tk.BOTH)]
        for text, command in options:
            button = tk.Button(align_window, width=button_width, text=text, command=lambda c=command: self.align_action(c))
            button.pack(pady=5)

        self.center_window(align_window, 300, 170)


if __name__ == "__main__":
    window = tk.Tk()
    app = MyMailApp(window)
    window.mainloop()
