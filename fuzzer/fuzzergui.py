#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

BLUE = "#1E2B33"
ORANGE = "#F87D51"
FONT = "aerial", 10, "bold"


def test_func():
    print("test")


# ---------------------------- FIND WORDLIST ------------------------------- #
def browse():
    chosen_wordlist = filedialog.askopenfilename(initialdir='/',title='Select a File' ,filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
    if chosen_wordlist:
        wordlist_entry.insert(0, chosen_wordlist)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Project Name")
window.config(padx=50, pady=50, bg=BLUE)

canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
kapow_img = PhotoImage(file="ka_pow.png")
canvas.create_image(150, 100, image=kapow_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website to bust:", bg=BLUE, fg=ORANGE, font=FONT)
website_label.grid(column=0, row=1)

output_label = Label(text="Output file name:", bg=BLUE, fg=ORANGE, font=FONT)
output_label.grid(column=0, row=2)

wordlist_label = Label(text="Wordlist to use:", bg=BLUE, fg=ORANGE, font=FONT)
wordlist_label.grid(column=0, row=3)

# Entries
website_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.insert(0, "https://")
website_entry.focus()

output_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
output_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
output_entry.insert(0, "")

wordlist_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
wordlist_entry.grid(column=1, row=3, sticky="EW")

# Buttons
# search_button = Button(text="Search", command=find_password, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
# search_button.grid(column=2, row=1, sticky="EW")

browse_button = Button(text="Browse", command=browse, bg=BLUE, fg=ORANGE, font=FONT,
                         highlightthickness=0)
browse_button.grid(column=2, row=3, sticky="EW")

bust_button = Button(text="Bust it!", command=test_func, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
bust_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
