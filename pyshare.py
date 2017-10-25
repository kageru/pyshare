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
tk = Tk()


def generate_filename(prefix, length, ext):
    return prefix + ''.join(choices(character_pool, k=length)) + '.' + ext


def find_filename(prefix, length, ext, conn):
    filename = generate_filename(prefix, length, ext)
    i = 0
    while conn.exists(filename):
        filename = generate_filename(prefix, length, ext)
        i += 1
        if i > 1000:
            # completely, definitely, totally justified recursion... yay?
            find_filename(prefix, length + 1, ext, conn)


def upload_local_file(path: str, conn: Connection) -> Exception:
    # does this even return an exception? probably not. does it matter? definitely not
    raise NotImplementedError('soon(tm)')


def take_screenshot(filename: str) -> None:
    call(["escrotum", "{}".format(filename), "-s"])


def ftp_upload(mode='screenshot', ext=None) -> tuple:
    if mode == 'screenshot' and ext is None:
        ext = 'png'

    with Connection(config.sftp_address, username=config.username, password=config.password) as conn:
        with conn.cd(config.remote_directory):
            filename = find_filename(config.prefix, config.length, ext, conn) + '.{}'.format(ext)
            fullpath = os.path.join(config.local_directory, filename)

            take_screenshot(filename)

            conn.put(filename)
    return fullpath, filename


def curl_upload(filename):
    if config.custom_curl_command is not None:
        return call(config.custom_curl_command)
    else:
        return call(
            f'curl -k -F"file=@{filename}" -F"name={config.username}" -F"passwd={config.password}" {config.curl_target}')


def set_clipboard(text):
    tk.clipboard_clear()
    tk.clipboard_append(text)


def get_clipboard():
    result = tk.selection_get(selection="CLIPBOARD")


def notify_user(url):
    print(url)
    # also show a little button that does nothing.
    # Well, it informs you that your link is ready, so that's something, I guess
    rButton = Button(tk, text=f"{url}", font=("Verdana", 12), bg="black", command=sys.exit)
    rButton.pack()
    tk.geometry('400x50+700+500')
    tk.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 1:
        mode = 'file'
        # mode = sys.argv[1]
        file = sys.argv[1]
    else:
        mode = 'screenshot'
        ext = 'png'
    if mode == 'screenshot':
        pass
    elif mode=='file':
        pass
    elif mode=='text':
        pass

    """
    if config.uploader in ['ftp', 'sftp']:
        if mode != 'screenshot' and '.' in file:
            ext = '.' + file.rsplit('.', 1)[1]
        # TODO: mode file for FTP
        fullpath, filename = ftp_upload(mode, ext)
    elif config.uploader == 'curl':
        if mode=='screenshot':
            filename = generate_filename(length=config.length, ext='.png')
            fullpath = os.path.join(config.local_directory, filename)
            take_screenshot(fullpath)
        else:
            fullpath = file
        curl_upload(fullpath)
    else:
        print('Unknown mode')
        sys.exit(-1)
    url = config.url_template.format(filename)
    notify_user(url)
    """
