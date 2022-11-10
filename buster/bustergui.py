#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
import requests

BLUE = "#1E2B33"
ORANGE = "#F87D51"
FONT = "aerial", 10, "bold"


# ---------------------------- BUSTER FUNCTION ------------------------------- #
def buster():
    #protocol = input(f"Do you want HTTP or HTTPS?\n").lower() ###POSSIBLY UNNEEDED. IT'S HERE INCASE
    # name_file = input("What would you like to name your output file? Leave empty for none:\n")
    # url = input(f"What URL are we busting today?\n").lower()
    # if 'www.' not in url:
    #     url = f"www.{url}"
    #     if 'http' not in url:
    #         url = f"https://{url}"
    # wordlist = input(f"What is the word list you want to use? (Full or Relative path to word list):\n")
    print(f"Starting Busting...\n")

    wordlist = wordlist_entry.get()
    savedirectory = savedirectory_entry.get()
    url = website_entry.get()
    savename = output_entry.get()
    tosave_successes = []
    tosave_failures = []
    with open(wordlist, 'r') as f:
        all_lines = f.readlines()
        
    for line in all_lines:
            line = line.strip()
            response = requests.get(f"{url}/{line}")
            http_code = response.status_code
            # print(http_code)
            # print(type(http_code))
            #try:
            response = response.text
            if 200 <= http_code < 300:
                print(f'{http_code}: {url}/{line}')
                tosave_successes.append(f'{http_code}: {url}/{line}')
                # print(tosave_successes)
            else:
                print(f'{http_code}: {url}/{line}')
                tosave_failures.append(f'{http_code}: {url}/{line}')
                # print(tosave_failures)
    if savename != "":
        # print(savename[-4:])
        if savename[-4:] != ".txt":
            with open(f'{savedirectory}/{savename}_successes.txt', 'a') as f:
                for item in tosave_successes:
                    f.write(f"{item}\n")
            with open(f'{savedirectory}/{savename}_failures.txt', 'a') as f:
                for item in tosave_failures:
                    f.write(f"{item}\n")
        else:
            with open(f'{savedirectory}/{savename[:-4]}_successes.txt', 'a') as f:
                for item in tosave_successes:
                    f.write(f"{item}\n")
            with open(f'{savedirectory}/{savename[:-4]}_failures.txt', 'a') as f:
                for item in tosave_failures:
                    f.write(f"{item}\n")
    print(f"\nBusted!")


# ---------------------------- FIND DIRECTORY ------------------------------- #
def save():
    chosen_directory = filedialog.askdirectory(initialdir='.',title='Select a Folder')
    if chosen_directory:
        savedirectory_entry.delete(0, END)
        savedirectory_entry.insert(0, str(chosen_directory))

# ---------------------------- FIND WORDLIST ------------------------------- #
def browse():
    chosen_wordlist = filedialog.askopenfilename(initialdir='.',title='Select a File' ,filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
    if chosen_wordlist:
        wordlist_entry.delete(0, END)
        wordlist_entry.insert(0, str(chosen_wordlist))


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Project Name")
window.config(padx=50, pady=50, bg=BLUE)

canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
kapow_img = PhotoImage(file="buster/ka_pow.png")
canvas.create_image(150, 100, image=kapow_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website to bust:", bg=BLUE, fg=ORANGE, font=FONT)
website_label.grid(column=0, row=1)

output_label = Label(text="Output file name:", bg=BLUE, fg=ORANGE, font=FONT)
output_label.grid(column=0, row=2)

savedirectory_label = Label(text="Directory to save file:", bg=BLUE, fg=ORANGE, font=FONT)
savedirectory_label.grid(column=0, row=3)

wordlist_label = Label(text="Wordlist to use:", bg=BLUE, fg=ORANGE, font=FONT)
wordlist_label.grid(column=0, row=4)

# Entries
website_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.insert(0, "https://")
website_entry.focus()

output_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
output_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
output_entry.insert(0, "")

savedirectory_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
savedirectory_entry.grid(column=1, row=3, sticky="EW")
savedirectory_entry.insert(0, "")

wordlist_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
wordlist_entry.grid(column=1, row=4, sticky="EW")

# Buttons
# search_button = Button(text="Search", command=find_password, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
# search_button.grid(column=2, row=1, sticky="EW")
save_button = Button(text="Browse Directory", command=save, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
save_button.grid(column=2, row=3, sticky="EW")

browse_button = Button(text="Browse", command=browse, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
browse_button.grid(column=2, row=4, sticky="EW")

bust_button = Button(text="Bust it!", command=buster, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
bust_button.grid(column=1, row=5, columnspan=2, sticky="EW")

window.mainloop()
