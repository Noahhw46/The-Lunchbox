#!/usr/bin/env python3

from buster import bustergui as bg
from fuzzer import fuzzergui as fg
from param_miner import pminer_gui as pg
# from mitm_attack import mitm as mm
from pathlib import Path
from tkinter import *

def busted():
    window.destroy()
    bg.main()

def fuzzed():
    window.destroy()
    fg.main()

def mined():
    window.destroy()
    pg.main()

ROOTPATH = Path(__file__).parent
ASSETPATH = f"{ROOTPATH}/assets"
BLUE = "#1E2B33"
ORANGE = "#F87D51"
FONT = "aerial", 10, "bold"

window = Tk()
window.title("My First Red Team Tools")
window.config(padx=50, pady=50, bg=BLUE)


canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
kapow_img = PhotoImage(file=f"{ASSETPATH}\\wow.png")
canvas.create_image(150, 100, image=kapow_img)
canvas.grid(column=1, row=0)


# Labels
buster_label = Label(text="Bust Some Web Directories", bg=BLUE, fg=ORANGE, font=FONT)
buster_label.grid(column=0, row=1)

param_label = Label(text="Check For Known parameters", bg=BLUE, fg=ORANGE, font=FONT)
param_label.grid(column=0, row=2)

fuzzer_label = Label(text="Test Some Parameters", bg=BLUE, fg=ORANGE, font=FONT)
fuzzer_label.grid(column=0, row=3)

mitm_label = Label(text="Man-in-the-Middle", bg=BLUE, fg=ORANGE, font=FONT)
mitm_label.grid(column=0, row=4)


# Buttons
buster_button = Button(text="Buster", command=busted, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
buster_button.grid(column=1, row=1, sticky="EW")

param_button = Button(text="P-Miner", command=pg, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
param_button.grid(column=2, row=4, sticky="EW")

fuzzer_button = Button(text="Fuzzer", command=fuzzed, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
fuzzer_button.grid(column=1, row=3, columnspan=2, sticky="EW")

# mitm_button = Button(text="Bust it!", command=mm, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
# mitm_button.grid(column=1, row=5, columnspan=2, sticky="EW")

exit_button = Button(text="Bye!", command=window.destroy, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
exit_button.grid(column=1, row=5, columnspan=2, sticky="EW")



window.mainloop()
