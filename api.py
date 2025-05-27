from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from enum import Enum
import logging
import os
from datetime import datetime

# os.environ['FLASK_ENV'] = 'production'
# logging.getLogger('werkzeug').setLevel(logging.ERROR)

class TextColor(Enum):
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    BRIGHT_BLACK   = '\033[90m'
    BRIGHT_RED     = '\033[91m'
    BRIGHT_GREEN   = '\033[92m'
    BRIGHT_YELLOW  = '\033[93m'
    BRIGHT_BLUE    = '\033[94m'
    RESET   = '\033[0m'

def colortxt(text, color):
    return f"{color.value}{text}{TextColor.RESET.value}"

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
DATABASE = "users.db"

class Note:
    def __init__(self, username, title, content, code):
        self.owner = username
        self.title = title
        self.content = content
        self.code = code

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            username TEXT NOT NULL,
            time TIMESTAMP NOT NULL,
            code TEXT NOT NULL
        );
        """)

def get_user(username):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

def all_users():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.execute("SELECT username FROM users")
        return [x[0] for x in cur.fetchall()]

def getnotes(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from notes WHERE username = ?", (username,))
        return [Note(x[3], x[1], x[2], x[-1]) for x in cursor.fetchall()]

from flask import redirect
import random
import string
def generate():
    rand = ''.join([x for x in string.ascii_letters])
    rand = [x for x in rand]
    random.shuffle(rand)
    rand = "".join(rand)
    rand = rand[random.randint(0, len(rand)-1):-1][:10]
    return rand.lower()
@app.route("/delete_note", methods=["POST"])
def delete_note():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    title = request.form.get("title")
    content = request.form.get("content")

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "DELETE FROM notes WHERE username = ? AND title = ? AND content = ?",
            (username, title, content)
        )
        conn.commit()

    return redirect(url_for("index"))


@app.route("/")
def index():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    with sqlite3.connect(DATABASE) as conn:
        raw_notes = conn.execute(
            "SELECT title, content, time, code FROM notes WHERE username = ? ORDER BY time DESC",
            (username,)
        ).fetchall()
    notes = [
        (title, content, datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime("%b %d, %Y at %I:%M %p"), code)
        for title, content, time, code in raw_notes
    ]
    return render_template("index.html", username=username, notes=notes)


@app.route("/about")
def about():
    username = session.get("username")
    return render_template("about.html", username=username)

@app.route("/contact")
def contact():
    username = session.get("username")
    return render_template("contact.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = get_user(username)
        if user and user[2] == password:  # password is 3rd column
            session["username"] = username
            flash("Logged in successfully!")
            return redirect(url_for("index"))
        flash("Invalid username or password")
    username = session.get("username")
    return render_template("login.html", username=username)


@app.route("/create_note", methods=["GET", "POST"])
def create_note():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        title = content[:20] + "..." if len(content) > 20 else content

        if content:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    "INSERT INTO notes (title, content, username, time, code) VALUES (?, ?, ?, ?, ?)",
                    (title, content, username, datetime.now(), generate())
                )
                conn.commit()
            flash("Note saved successfully!")
            return redirect(url_for("index"))
        else:
            flash("Note content cannot be empty.")

    return redirect(url_for("create"))

@app.route("/create", methods=["GET", "POST"])
def create():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))
    username = session.get('username')
    return render_template("create.html", username=username)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))
    username = session.get('username')
    return render_template("edit.html", username=username, noteid=request.args.get('id'))

@app.route("/edit_note", methods=["POST"])
def edit_note():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))


    with sqlite3.connect(DATABASE) as conn:
        conn.execute(   
            "UPDATE notes set content = ? WHERE code = ?",
            (request.form.get('content'),request.args.get('id'),)
        )
        conn.commit()

    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if get_user(username):
            flash("Username already exists, please choose another.")
            return render_template("signup.html")
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        flash("Account created! Please log in.")
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template("signup.html", username=username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0", port=5000, debug=True)
