# this file can be run on a server to act as the endpoint of the script.
# I mainly want to test whether this is faster than sftp

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_file() -> tuple:
    if 'file' in request.files:
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        file.save(filename)
        return filename, 201
    return 'you\'re doing this wrong', 418

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
