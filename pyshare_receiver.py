# this file can be run on a server to act as the endpoint of the script.
# I mainly want to test whether this is faster than sftp

from flask import Flask, request
from werkzeug.utils import secure_filename
from hashlib import sha3_256
from users import users

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


@app.route('/', methods=['POST'])
def receive_file() -> tuple:
    if 'file' in request.files:
        if authenticate(request) is True:
            file = request.files.get('file')
            filename = secure_filename(file.filename)
            file.save(filename)
            return filename, 201
        else:
            return 'Wrong or no credentials', 403
    return 'you\'re doing this wrong', 418


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
