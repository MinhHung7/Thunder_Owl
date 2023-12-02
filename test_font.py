import tkinter as tk
from tkinter import font

# Create a root window (it won't be shown)
root = tk.Tk()

# Get the list of supported fonts
supported_fonts = font.families()

# Filter and print only fonts with one word
single_word_fonts = [font_name for font_name in supported_fonts if ' ' not in font_name]
print(single_word_fonts)

# Close the root window (it was created just to get the font families)
root.destroy()
