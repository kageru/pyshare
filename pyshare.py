#!/usr/bin/env python

from string import ascii_letters, digits
from argparse import ArgumentParser
from pysftp import Connection
from subprocess import call
from random import choices
from PIL import Image
import pyperclip
import config
import sys
import os
import re

character_pool = ascii_letters + digits


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-m' '--mode', type=str, dest='mode', default=None,
                        help='Sets the input mode. Allowed values are "screenshot" and "clipboard". Implicit it file(s) are set.')
    parser.add_argument('-f', '--files', type=str, nargs='*', dest='files', help='List of files to be uploaded', default=None)
    return parser.parse_args()


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
        filename = ftp_upload(path, mode='file')[1]
        return config.url_template.format(filename)
    else:
        return curl_upload(path)


def take_screenshot() -> None:
    tempname = generate_filename(config.length, 'png')
    file = os.path.join(config.local_directory, tempname)
    call(['maim', '-sk', file])
    ftp_upload(ext='png', sourcefile=file, mode='screenshot')
    if not config.keep_local_copies:
        os.remove(file)


def ftp_upload(sourcefile, *, mode=None, ext=None) -> tuple:
    if ext is None:
        # TODO files without extension
        exts = {
            'screenshot': 'png',
            'text': 'txt',
        }
        if re.search('\.tar\.\w{1,4}]', sourcefile):
            # properly handle .tar.something files
            ext = sourcefile.split('.')[-2:]
        else:
            ext = exts.get(mode, mode not in exts and sourcefile.split('.')[-1])  # Only do the split if necessary

    with Connection(config.sftp_address, username=config.username, password=config.password,
                    private_key=config.private_key, private_key_pass=config.private_key_pass) as conn:
        conn.chdir(config.remote_directory)

        cur_name = sourcefile.split('/')[-1]
        filename = cur_name
        if mode == 'screenshot':
            os.chdir(config.local_directory)
            if conn.exists(cur_name):
                filename = find_valid_filename(prefix=config.prefix, length=config.length, ext=ext, conn=conn)
            conn.put(filename, filename)
        else:
            filename = find_valid_filename(prefix=config.prefix, length=config.length, ext=ext, conn=conn)

            if mode == 'file':
                conn.put(sourcefile, filename)

        fullpath = os.path.join(config.local_directory, filename)

        notify_user(config.url_template.format(filename))

    return fullpath, filename


def curl_upload(filename):
    return call(config.custom_curl_command)


def notify_user(url, image=None):
    print(url)
    pyperclip.copy(url)
    if image:
        img = Image.open(image)
        img.thumbnail((384, 384), Image.ANTIALIAS)
        thumbnail = os.path.join(config.local_directory, 'thumb.jpg')
        img.save(thumbnail)
        call(['notify-send', '-a pyshare', url, f'-i {thumbnail}', '-t 3000'])
        os.remove(thumbnail)
    else:
        call(['notify-send', '-a pyshare', url, '-t 3000'])


def parse_text(args):
    text = pyperclip.paste()
    if re.match(r'(https?|s?ftp)://', text):
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
    args = parse_arguments()
    if args.mode is None:
        if args.files is not None:
            args.mode = 'files'
        else:
            args.mode = 'screenshot'
    if args.mode == 'screenshot':
        take_screenshot()
    elif args.mode == 'clipboard':
        parse_text(pyperclip.paste())
    else:
        for file in args.files:
            upload_local_file(file)

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
