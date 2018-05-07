#!/usr/bin/env python

from string import ascii_letters, digits
from argparse import ArgumentParser
from pysftp import Connection
from subprocess import call, check_output
from random import choices
from datetime import date
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
                        help='Sets the input mode. Allowed values are "screenshot" and "clipboard". Implicit it if file(s) are set.')
    parser.add_argument('-f', '--files', type=str, nargs='*', dest='files', help='List of files to be uploaded', default=None)
    parser.add_argument('-e', '--edit', type=bool, dest='edit', default=False, help='Open the screenshot in gimp to edit it before uploading')
    return parser.parse_args()


def generate_filename(length: int, ext: str) -> str:
    filename = config.prefix + ''.join(choices(character_pool, k=length)) + '.' + ext
    return filename


def get_local_full_path() -> str:
    if config.local_directory_nesting:
        folder = get_date_folder()
        return os.path.join(config.local_directory, folder)
    return config.local_directory


def get_date_folder() -> str:
    return date.today().strftime(config.local_directory_nesting)


def upload_local_file(path: str) -> None:
    if config.uploader in ['ftp', 'sftp']:
        filename = ftp_upload(path)
        if config.preserve_folders_on_remote:
            filename = os.path.join(get_date_folder(), filename)
        url = config.url_template.format(filename)
    else:
        url = curl_upload(path)
    notify_user(url)


def take_screenshot(edit=False) -> None:
    full_path = get_local_full_path()
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    tempname = generate_filename(config.length, 'png')
    file = os.path.join(get_local_full_path(), tempname)
    call(['maim', '-suk', file])
    Image.open(file).convert('RGB').save(file)
    if edit:
        call(['gimp', file])
    upload_local_file(file)
    if not config.keep_local_copies:
        os.remove(file)


def get_extension(filename: str) -> str:
    """
    Returns the extension of a file/full path as a string.
    Emtpy if the file has no extension.
    .tar.xx archives are handled accordingly.
    """
    filename = os.path.basename(filename)
    if re.search('\.tar\.\w{1,4}', filename):
        num_exts = 2
    else:
        num_exts = 1
    extension = '.'.join(filename.split('.')[-num_exts:])
    return extension


def ftp_upload(sourcefile: str) -> str:


    def prepare_remote_folder(conn) -> None:
        "Create the necessary folder(s) on the remote server and change the directory accordingly"
        if config.preserve_folders_on_remote:
            full_remote_dir = os.path.join(config.remote_directory, get_date_folder())
        else:
            full_remote_dir = config.remote_directory
        if not conn.exists(full_remote_dir):
            conn.makedirs(full_remote_dir)
        conn.chdir(full_remote_dir)


    extension = get_extension(sourcefile)
    with Connection(config.sftp_address, username=config.username, password=config.password, port=config.sftp_port,
                    private_key=config.private_key, private_key_pass=config.private_key_pass) as conn:
        prepare_remote_folder(conn)
        extension = get_extension(sourcefile)
        dest_name = generate_filename(config.length, extension)
        while conn.exists(dest_name):
            dest_name = generate_filename(config.length, extension)
        conn.put(sourcefile, dest_name)
        return dest_name


def curl_upload(filename: str) -> str:
    return check_output(config.curl_command.format(filename), shell=True).decode()[:-1]


def notify_user(url:str, image=None) -> None:
    print(url)
    pyperclip.copy(url)
    if config.enable_thumbnails and image:
        img = Image.open(image)
        img.thumbnail((384, 384), Image.ANTIALIAS)
        thumbnail = os.path.join(config.local_directory, 'thumb.jpg')
        img.save(thumbnail)
        call(['notify-send', '-a', 'pyshare', url, '-i',  thumbnail, '-t', '3000'])
        os.remove(thumbnail)
    else:
        call(['notify-send', '-a', 'pyshare', url, '-t', '3000'])


def parse_text(text):
    if re.match(r'(https?|s?ftp)://', text):
        mirror_file(text)
    elif os.path.isfile(text):
        upload_local_file(text)
    else:
        upload_text(text)


def mirror_file(text: str):
    os.chdir(config.local_directory)
    call(['wget', text])
    filename = text.rsplit('/', 1)[1]
    url = upload_local_file(os.path.join(config.local_directory, filename))
    os.remove(os.path.join(config.local_directory, filename))


def upload_text(text):
    filename = generate_filename(config.length, 'txt')
    with open(os.path.join(config.local_directory, filename), 'w') as file:
        file.write(text)
    url = upload_local_file(os.path.join(config.local_directory, filename))
    os.remove(os.path.join(config.local_directory, filename))


if __name__ == '__main__':
    args = parse_arguments()
    if args.mode is None:
        if args.files is not None:
            args.mode = 'files'
        else:
            args.mode = 'screenshot'
    if args.mode == 'screenshot':
        take_screenshot(args.edit)
    elif args.mode in ('clipboard', 'text', 'b'):
        parse_text(pyperclip.paste())
    else:
        for file in args.files:
            upload_local_file(file)

