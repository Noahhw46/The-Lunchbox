#!/usr/bin/env python3

from pathlib import Path
import requests
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory

ROOTPATH = Path(__file__).parent.parent
ASSETPATH = f"{ROOTPATH}/assets"
BLUE = "#1E2B33"
ORANGE = "#F87D51"
FONT = "aerial", 10, "bold"

# ---------------------------- BUSTER FUNCTION ----------------------------- #
def buster(url, wordlist):
    busted_successes = []
    busted_failures = []
    with open(wordlist, 'r') as f:
        all_lines = f.readlines()
        
        for line in all_lines:
            line = line.strip()
            response = requests.get(f"{url}/{line}")
            http_code = response.status_code
            response = response.text
            if 200 <= http_code < 300:
                print(f'{http_code}: {url}/{line}')
                busted_successes.append(f'{http_code}: {url}/{line}')
            elif http_code != 404:
                print(f'{http_code}: {url}/{line}')
                busted_failures.append(f'{http_code}: {url}/{line}')
    return busted_successes, busted_failures
 

# ---------------------------- FIND DIRECTORY ------------------------------ #
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


# ---------------------------- RECURSIVE ----------------------------------- #
def recursive(url, wordlist, successful_urls, failure_urls):
    with open(wordlist, 'r') as f:
        all_lines = f.readlines()
    all_lines = [line.strip() for line in all_lines]
    for word in all_lines:
        response = requests.get(f"{url}/{word}")
        http_code = response.status_code

        if 200 <= http_code < 300:
            print(f'{http_code}: {url}/{word}')
            successful_urls.append(f'{url}/{word}')
            recursive(f'{url}/{word}', wordlist, successful_urls, failure_urls)
            
        elif http_code != 404:
            print(f'{http_code}: {url}/{word}')
            failure_urls.append(f'{url}/{word}')

    return successful_urls, failure_urls


# ---------------------------- RECURSIVE ----------------------------------- #
def main():
    url = website_entry.get()
    wordlist = wordlist_entry.get()
    successful_urls = []
    failure_urls = []
    savedirectory = savedirectory_entry.get()
    savename = output_entry.get()
    recurse = is_recursive.get()
    failsave = save_fails.get()
    results = []
    if recurse == 0:
        print("Busting...")
        results = buster(url, wordlist)
        print("Busted...")
    else:
        print("Recursive Busting...")
        results = recursive(url, wordlist, successful_urls, failure_urls)
        print("Recursive Busted...")

    with open(f'{savedirectory}/successes_{savename}', 'a') as f:
        for item in results[0]:
            f.write(f"{item}\n")
    if failsave == 1:
        with open(f'{savedirectory}/failures_{savename}', 'a') as f:
            for item in results[1]:
                f.write(f"{item}\n")
    print("Done!")


# ---------------------------- UI SETUP ------------------------------------ #
window = Tk()
window.title("SpiderBuster")
window.config(padx=50, pady=50, bg=BLUE)

is_recursive = IntVar()
save_fails = IntVar()

canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
kapow_img = PhotoImage(file=f"{ASSETPATH}/ka_pow.png")
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
save_button = Button(text="Browse Directory", command=save, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
save_button.grid(column=2, row=3, sticky="EW")

browse_button = Button(text="Browse", command=browse, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
browse_button.grid(column=2, row=4, sticky="EW")

bust_button = Button(text="Bust it!", command=main, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
bust_button.grid(column=1, row=5, columnspan=2, sticky="EW")

recursive_box = Checkbutton(window, text="Recursive", variable=is_recursive, onvalue=1, offvalue=0,  bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
recursive_box.grid(column=1, row=6, sticky="EW")

fail_box = Checkbutton(window, text="Save failures?", variable=save_fails, onvalue=1, offvalue=0,  bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
fail_box.grid(column=2, row=6, sticky="EW")


window.mainloop()
