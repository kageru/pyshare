#!/usr/bin/env python

import sys
from subprocess import call
import os
from pysftp import Connection
from tkinter import Tk, Button
from string import ascii_letters, digits
from random import choices
import config

character_pool = ascii_letters + digits


def find_filename(prefix, length, ext, conn):
    def generate_filename(prefix, length, ext):
        return prefix + ''.join(choices(character_pool, k=length)) + '.' + ext

    filename = generate_filename(prefix, length, ext)
    i = 0
    while conn.exists(filename):
        filename = generate_filename(prefix, length, ext)
        i += 1
        if i > 1000:
            # using recursion here feels... questionable at best, but it's faster than using % every loop
            find_filename(prefix, length + 1, ext, conn)


def upload_local_file(path: str, conn: Connection):
    raise NotImplementedError('soon(tm)')


def upload_screenshot(filename: str, conn: Connection):
    call(["escrotum", "{}".format(filename), "-s"])
    conn.put(filename)


def prepare_upload(mode='screenshot', ext=None) -> str:
    if mode == 'screenshot' and ext == None:
        ext = 'png'

    with Connection(config.sftp_address, username=config.username, password=config.password) as conn:
        with conn.cd(config.remote_directory):
            filename = find_filename(config.prefix, config.length, ext, conn) + '.{}'.format(ext)

            filepath = os.path.join(config.local_directory, filename)

    return filepath


link = config.link_template.format(filename)

# copy link to clipboard
# https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python#4203897
print(link)
r = Tk()
r.clipboard_clear()
r.clipboard_append(link)
r.after(2000, sys.exit)
# also show a little button that does nothing.
# Well, it informs you that your link is ready, so that's something, I guess
rButton = Button(r, text=f"{link}", font=("Verdana", 12), bg="black", command=sys.exit)
rButton.pack()
r.geometry('400x50+700+500')
r.mainloop()
