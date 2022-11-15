#!/usr/bin/env python3

from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
import requests
import random
import time
import regex as re
import entry as e

def main():
    ROOTPATH = Path(__file__).parent.parent
    USERAGENTS = ROOTPATH / "wordlists" / "useragents.txt"
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


    # ---------------------------- EXTRACT PARAMS ------------------------------- #
    def extract_parms(response):
        #split the response into a list by line
        response = response.splitlines()
        params = r"(\?|&)([^=]+)="
        all_params_uris = [url for url in response if re.search(params, url)]

        final_uris = []
        for uri in all_params_uris:
            delim = uri.find("=") + 1
            final_uri = uri[:delim] + 'FUZZ'
            final_uris.append(final_uri)
        
        
        final_uris = list(set(final_uris))
        return final_uris


    # ---------------------------- MAKE REQUEST ----------------------------------- #
    def makerequest(domain):
        result = False
        with open(USERAGENTS, 'r') as f:
            agents = f.readlines()
            agents = [agent.strip() for agent in agents]
        agent = random.choice(agents)

        headers = {'User-Agent': agent}

        url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

        try:
            response = requests.get(url, headers=headers, timeout=40)
            response.raise_for_status()
            result = response.text
            
        except requests.exceptions.ConnectionError as e:
                print("Can not connect to server.")
        except requests.exceptions.Timeout as e:
                print("Timeout Error.")
                time.sleep(2)
        except requests.exceptions.HTTPError as err:
                print(f"{err}. Retrying in 2 seconds.")
                time.sleep(2)
        except requests.exceptions.RequestException as e:
                print(" {e} Can not get target information")
        except KeyboardInterrupt as k:
                print("Interrupted by user. Exiting.")
                raise SystemExit(k)    
        finally:
            return result


    # ---------------------------- MAIN ----------------------------------- #
    def start():
        domain = website_entry.get()
        print(f"Extracting parameters from {domain}")
        savename = output_entry.get()
        savedirectory = savedirectory_entry.get()
        # input("What file would you like to save the results to? ")
        res = makerequest(domain)
        if res:
            extracted = extract_parms(res)
            with open(f'{savedirectory}/{savename} ', 'w') as f:
                for uri in extracted:
                    f.write(uri + '\n')
            print(f"Found {len(extracted)} parameters. Output written to {savedirectory}/{savename}")
        else:
            print("No parameters found.")
        window.destroy()
        e.main()


    # ---------------------------- UI SETUP ------------------------------------ #


    window = Tk()
    window.title("P-Miner")
    window.config(padx=50, pady=50, bg=BLUE)

    save_fails = IntVar()

    canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
    kapow_img = PhotoImage(file=f"{ASSETPATH}/ting.png")
    canvas.create_image(150, 100, image=kapow_img)
    canvas.grid(column=1, row=0)

    # Labels
    website_label = Label(text="Where are we looking for params:", bg=BLUE, fg=ORANGE, font=FONT)
    website_label.grid(column=0, row=1)

    output_label = Label(text="Output file name:", bg=BLUE, fg=ORANGE, font=FONT)
    output_label.grid(column=0, row=2)

    savedirectory_label = Label(text="Directory to save file:", bg=BLUE, fg=ORANGE, font=FONT)
    savedirectory_label.grid(column=0, row=3)


    # Entries
    website_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
    website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
    website_entry.insert(0, "")
    website_entry.focus()

    output_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
    output_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
    output_entry.insert(0, "")

    savedirectory_entry = Entry(bg=BLUE, fg=ORANGE, font=FONT)
    savedirectory_entry.grid(column=1, row=3, sticky="EW")
    savedirectory_entry.insert(0, "")



    # Buttons
    save_button = Button(text="Browse Directory", command=save, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    save_button.grid(column=2, row=3, sticky="EW")


    bust_button = Button(text="Mine it!", command=start, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    bust_button.grid(column=1, row=4, columnspan=2, sticky="EW")


    window.mainloop()
