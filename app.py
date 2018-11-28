import signal
import sqlite3
import time

from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
conn = sqlite3.connect('stig.db', check_same_thread=False)

# ready database
conn.execute('CREATE TABLE IF NOT EXISTS pastes (paste TEXT, created INTEGER, expiration INTEGER)')
conn.execute('CREATE TABLE IF NOT EXISTS files (paste TEXT, name TEXT, data BLOB)')
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# def encrypt(text):
#     key = "0123456789012345"
#     crypto = AES.new(key.encode(), AES.MODE_CBC)
#     print("IV: " + str(crypto.iv))
#     print("Padded: " + str(pad(text.encode(), 16)))
#     encrypted = crypto.iv + crypto.encrypt(pad(text.encode(), 16))
#     print("Encrypted: " + str(encrypted))
#     return encrypted
# conn.execute('INSERT INTO files VALUES ("6d4628d7-a555-4bbb-97be-626aaa57b8de", ?, ?)', (encrypt("secret.txt"),encrypt("attack at dawn!"),))
conn.commit()


def sigint():
    print("CTRL-C caught; writing changes to database")
    conn.commit()


@app.route('/')
def index():
    return render_template('index.j2', name="wow")


@app.route('/<uuid:uuid>', methods=['GET'])
def view(uuid):
    c = conn.cursor()
    c.execute("SELECT created FROM pastes WHERE paste = ?", (str(uuid),))
    created_tuple = c.fetchone()
    if created_tuple is None:
        return "Paste not found. Has it expired?", 404
    created = datetime.fromtimestamp(created_tuple[0] // 1000)

    c = conn.cursor()
    files = []
    for row in c.execute("SELECT name, data FROM files WHERE paste = ?", (str(uuid),)):
        files.append({"name": b64encode(row[0]).decode("utf-8"), "data": b64encode(row[1]).decode("utf-8")})
    if len(files) == 0:
        return "No files found for paste.", 404

    return render_template('view.j2', created=created, files=files)


@app.route('/post', methods=['POST'])
def post():
    return ''


@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.fromtimestamp(int(round(time.time())))
    diff = now - dt

    periods = (
        (diff.days // 365, "year", "years"),
        (diff.days // 30, "month", "months"),
        (diff.days // 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds // 3600, "hour", "hours"),
        (diff.seconds // 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return str(period) + " " + (singular if period == 1 else plural) + " ago"
    return default


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint) # set sigint handler
    app.run()
