#!/usr/bin/env python

from string import ascii_letters, digits
from argparse import ArgumentParser
from pysftp import Connection
from subprocess import call
from random import choices
import pyperclip
import config
import sys
import os
import re

character_pool = ascii_letters + digits


def generate_filename(length, ext, prefix=''):
    return prefix + ''.join(choices(character_pool, k=length)) + '.' + ext


def find_valid_filename(prefix, length, ext, conn):
    filename = generate_filename(prefix=prefix, length=length, ext=ext)
    i = 0
    while conn.exists(filename):
        filename = generate_filename(length=length, ext=ext, prefix=prefix)
        i += 1
        if i > 1000:
            # completely, definitely, totally justified recursion... yay?
            return find_valid_filename(prefix, length + 1, ext, conn)
    return filename

def upload_local_file(path: str) -> str:
    if config.uploader in ['ftp', 'sftp']:
        filename = ftp_upload(path)[1]
        return config.url_template.format(filename)
    else:
        return curl_upload(path)


def take_screenshot() -> None:
    tmppath = os.path.join(config.local_directory, 'tmp')
    tmpdir = os.listdir(tmppath)
    for f in tmpdir:
        os.remove(os.path.join(tmppath, f))
    # you can also use programs like escrotum here, but i3-scrot was much faster for me
    call(['i3-scrot', '-s'])
    file = os.path.join(config.local_directory, 'tmp', os.listdir(tmppath)[0])
    ftp_upload(ext='png', sourcefile=file)
    os.remove(file)


def ftp_upload(sourcefile, *, mode=None, ext=None) -> tuple:
    if ext is None:
        # TODO files without extension
        exts = {
            'screenshot': 'png',
            'text': 'txt',
            }
        ext = exts.get(mode, mode not in exts and sourcefile.split('.')[-1])  # Only do the split if necessary

    with Connection(config.sftp_address, username=config.username, password=config.password,
            private_key=config.private_key, private_key_pass=config.private_key_pass) as conn:
        conn.chdir(config.remote_directory)
        
        filename = find_valid_filename(prefix=config.prefix, length=config.length, ext=ext, conn=conn)
        fullpath = os.path.join(config.local_directory, filename)

        if mode == 'file':
            conn.put(sourcefile, filename)
        
        notify_user(config.url_template.format(filename))

    return fullpath, filename


def curl_upload(filename):
    return call(config.custom_curl_command)


def notify_user(url):
    print(url)
    pyperclip.copy(url)
    call(['notify-send', url])


def parse_clipboard(args):
        text = pyperclip.paste()
        if re.match(r'https?://', text):
            mirror_file(text)
        elif os.path.isfile(text):
            upload_local_file(text)
        else:
            upload_text(text)


def mirror_file(text):
    os.chdir(config.local_directory)
    call(['wget', text])
    filename = text.rsplit('/', 1)[1]
    url = upload_local_file(os.path.join(config.local_directory, filename))
    os.remove(os.path.join(config.local_directory, filename))
    notify_user(url)


def upload_text(text):
    filename = generate_filename(config.length, 'txt')
    with open(os.path.join(config.local_directory, filename), 'w') as file:
        file.write(text)
    url = upload_local_file(os.path.join(config.local_directory, filename))
    os.remove(os.path.join(config.local_directory, filename))
    notify_user(url)


if __name__ == '__main__':
    if len(sys.argv) == 1:    
        take_screenshot()
    else:
        for text in sys.argv[1:]:
            parse_clipboard(text)
    
    """
    if config.uploader in ['ftp', 'sftp']:
        if args.files is not None:
            for file in args.files:
                upload_local_file(file) 
        elif args.mode == 'text':
            parse_clipboard(args)
        else:
            take_screenshot()
                  
    elif args.files is not None:
       
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
