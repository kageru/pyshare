#!/usr/bin/env python3
# this file can be run on a server to act as the endpoint of the script.
# I mainly want to test whether this is faster than sftp

from flask import Flask, request
from werkzeug.utils import secure_filename
from hashlib import sha3_256
from users import users
import os
import config
from string import ascii_letters, digits
from random import choices

character_pool = ascii_letters + digits

app = Flask(__name__)


def salthash(password, salt):
    return sha3_256((password + salt).encode('utf8')).hexdigest()


def authenticate(request):
    print(request.form)
    if 'name' not in request.form or 'passwd' not in request.form:
        return False
    name = request.form.get('name')
    passwd = request.form.get('passwd')
    if name in users:
        user = users.get(name)
        if salthash(passwd, user[1]) == user[0]:
            return True
    return False


def find_filename(length, ext):
    def generate_filename(length, ext):
        return ''.join(choices(character_pool, k=length)) + ext

    filename = generate_filename(length, ext)
    i = 0
    while os.path.exists(os.path.join(config.remote_directory, filename)):
        i += 1
        if i > 1000:
            length += 1
            i = 0
        filename = generate_filename(length, ext)
    return filename


@app.route('/', methods=['POST'])
def receive_file() -> tuple:
    if 'file' in request.files:
        if authenticate(request) is True:
            file = request.files.get('file')
            filename = secure_filename(file.filename)
            if '.' in filename:
                extension = '.' + filename.rsplit('.', 1)[1]
            else:
                extension = ''
            storename = find_filename(config.length, extension)
            file.save(os.path.join(config.remote_directory, storename))
            return config.url_template.format(storename), 201
        else:
            return 'Wrong or no credentials', 403
    return 'you\'re doing this wrong', 418


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
