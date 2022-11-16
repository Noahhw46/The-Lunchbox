#!/usr/bin/env python3

import concurrent.futures
from pathlib import Path
import requests
import time
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
import entry as e 


def main():
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
    def construct_payload(urls, wordlist):
            payloads = []
            for url in urls:
                for word in wordlist:
                    payload = url.replace('FUZZ', word)
                    payloads.append(payload)
            return payloads


# ---------------------------- PAYLOAD ----------------------------------- #
    def send_request(payload):
        response = requests.get(payload)
        header = response.headers
        body = response.text
        if response.status_code != 200:
            result = f'Error: {response.status_code} from {payload}\n{header}\n{body}'
        else:
            result = f'Success: {response.status_code} from {payload}\n{header}\n{body}'
        return result


# ---------------------------- FUNCTION ----------------------------------- #
    def main():
        url = website_entry.get()
        wordlist = wordlist_entry.get()
        parameters = parameter_entry.get()
        parameters = parameters.replace(" ", "")
        parameters = parameters.split(",")
        params_to_fuzz = ["?" + item + "=" + 'FUZZ' for item in parameters]
        full_url = [url + item for item in params_to_fuzz]
        savedirectory = savedirectory_entry.get()
        savename = output_entry.get()
        failsave = save_fails.get()
        start = time.perf_counter()
        wordlist = read_wordlist(wordlist)
        payloads = construct_payload(full_url, wordlist)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(send_request, payloads)
        for value in results:
            if "Success" not in value and failsave == 1:
                with open(f'{savedirectory}/fuzzfailures_{savename}', 'a') as f:
                    f.write(f"{value}\n")
            if "Success" in value:
                with open(f'{savedirectory}/fuzzsuccesses_{savename}', 'a', encoding="utf-8") as f:
                    f.write(f"{value}\n")
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s)')
        window.destroy()
        e.main()


# ---------------------------- UI SETUP ------------------------------------ #

# Window
    window = Tk()
    window.title("Parameter Fuzzer")
    window.config(padx=50, pady=50, bg=BLUE)

    save_fails = IntVar()

    canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
    kapow_img = PhotoImage(file=f"{ASSETPATH}/boom.png")
    canvas.create_image(159, 100, image=kapow_img)
    canvas.grid(column=0, row=0, columnspan=3)

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

    fail_box = Checkbutton(window, text="Save failures?", variable=save_fails, onvalue=1, offvalue=0,  bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    fail_box.grid(column=0, row=6, sticky="EW")


    window.mainloop()
