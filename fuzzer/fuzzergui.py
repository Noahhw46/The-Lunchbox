#!/usr/bin/env python3

import concurrent.futures
from pathlib import Path
import requests
import time
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory


ROOTPATH = Path(__file__).parent.parent
ASSETPATH = f"{ROOTPATH}/assets"
BLUE = "#1E2B33"
ORANGE = "#F87D51"
FONT = "aerial", 10, "bold"


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


# ---------------------------- READ WORDLIST ------------------------------- #
def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines


# ---------------------------- PAYLOAD ----------------------------------- #
def construct_payload(url, wordlist):
        payloads = []
        for word in wordlist:
            payload = url.replace('FUZZ', word)
            payloads.append(payload)
        return payloads


# ---------------------------- PAYLOAD ----------------------------------- #
def send_request(payload):
    response = requests.get(payload)
    if response.status_code != 200 and response.status_code != 404:
        print(f'Error: {response.status_code} from {payload}')
    else:
        print(f'Success: {response.status_code} from {payload}')
        print(response.headers)




# ---------------------------- FUNCTION ----------------------------------- #
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

    start = time.perf_counter()
    wordlist = read_wordlist(wordlist)
    payloads = construct_payload(url, wordlist)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, payloads)
    finish = time.perf_counter()
    with open(f'{savedirectory}/successes_{savename}', 'a') as f:
        for item in results[0]:
            f.write(f"{item}\n")
    if failsave == 1:
        with open(f'{savedirectory}/failures_{savename}', 'a') as f:
            for item in results[1]:
                f.write(f"{item}\n")
    print(f'Finished in {round(finish-start, 2)} second(s)')

# ---------------------------- RECURSIVE ----------------------------------- #
def oldmain():
    url = website_entry.get()
    wordlist = wordlist_entry.get()
    successful_urls = []
    failure_urls = []
    savedirectory = savedirectory_entry.get()
    savename = output_entry.get()
    recurse = is_recursive.get()
    failsave = save_fails.get()
    results = []

# ---------------------------- UI SETUP ------------------------------------ #


window = Tk()
window.title("Parameter Fuzzer")
window.config(padx=50, pady=50, bg=BLUE)

is_recursive = IntVar()
save_fails = IntVar()

canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
kapow_img = PhotoImage(file=f"{ASSETPATH}/ka-pow.png")
canvas.create_image(150, 100, image=kapow_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website to fuzz:", bg=BLUE, fg=ORANGE, font=FONT)
website_label.grid(column=0, row=1)

parameter_label = Label(text="Parameter to fuzz:", bg=BLUE, fg=ORANGE, font=FONT)
parameter_label.grid(column=0, row=2)

output_label = Label(text="Output file name:", bg=BLUE, fg=ORANGE, font=FONT)
output_label.grid(column=0, row=3)

savedirectory_label = Label(text="Directory to save file:", bg=BLUE, fg=ORANGE, font=FONT)
savedirectory_label.grid(column=0, row=4)

wordlist_label = Label(text="Wordlist to use:", bg=BLUE, fg=ORANGE, font=FONT)
wordlist_label.grid(column=0, row=5)


# Entries
website_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.insert(0, "https://")
website_entry.focus()

parameter_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
parameter_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
parameter_entry.insert(0, "")

output_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
output_entry.grid(column=1, row=3, columnspan=2, sticky="EW")
output_entry.insert(0, "")

savedirectory_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
savedirectory_entry.grid(column=1, row=4, sticky="EW")
savedirectory_entry.insert(0, "")

wordlist_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
wordlist_entry.grid(column=1, row=5, sticky="EW")


# Buttons
save_button = Button(text="Browse Directory", command=save, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
save_button.grid(column=2, row=4, sticky="EW")

browse_button = Button(text="Browse", command=browse, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
browse_button.grid(column=2, row=5, sticky="EW")

bust_button = Button(text="Fuzz it!", command=main, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
bust_button.grid(column=1, row=6, columnspan=2, sticky="EW")

recursive_box = Checkbutton(window, text="Recursive", variable=is_recursive, onvalue=1, offvalue=0,  bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
recursive_box.grid(column=1, row=7, sticky="EW")

fail_box = Checkbutton(window, text="Save failures?", variable=save_fails, onvalue=1, offvalue=0,  bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
fail_box.grid(column=2, row=7, sticky="EW")


window.mainloop()
