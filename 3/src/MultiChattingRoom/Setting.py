'''
    Settings about internet.
    Optimize codes in order to read and modify easily.
'''

from time import ctime, sleep
from multiprocessing import Process, Queue
from select import select
from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, dialog, filedialog
from threading import *
import os
import struct

len_of_data = struct.calcsize('128sq')
HOST = "127.0.0.1"
PORT = 8080
ADDR = {HOST, PORT}


# set window in the center
def set_window_center(root, width=300, height=150):
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    x = (window_width - width) / 2
    y = (window_height - height) / 2
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))


def set_main_window(root):
    # adding input box of HOST, PORT and so on
    pad = 10
    # Host input box
    Label(root, text="Host:").grid(row=0, column=0, padx=pad, pady=pad)
    en_host = Entry(root)
    en_host.insert(0, HOST)
    en_host.grid(row=0, column=1, padx=pad, pady=pad)
    # Port input box
    Label(root, text="Port:").grid(row=1, column=0, padx=pad, pady=pad)
    en_port = Entry(root)
    en_port.insert(0, PORT)
    en_port.grid(row=1, column=1, padx=pad, pady=pad)
    return pad, en_host, en_port


def missing_conf(path, who):
    if not os.path.exists(path):
        root = Tk()
        root.withdraw()
        if who == "Client":
            messagebox.showerror("Error", "You are missing configuration file, Please download again!")
        elif who == "Server":
            messagebox.showerror("Error", "You are missing configuration file, Please check it!")
        sys.exit(1)
    else:
        return


