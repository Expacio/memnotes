from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    jsonify,
)
from flask import redirect
import random
import string
from enum import Enum
import logging
import os
import db
from datetime import datetime



class TextColor(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    RESET = "\033[0m"


def colortxt(text, color):
    return f"{color.value}{text}{TextColor.RESET.value}"


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "aahshit"
DATABASE = "users.db"


class Note:
    def __init__(self, username, title, content, code):
        self.owner = username
        self.title = title
        self.content = content
        self.code = code


get_user = db.get_user
all_users = db.all_users
getnotes = db.get_notes


def generate():
    rand = "".join([x for x in string.ascii_letters])
    rand = [x for x in rand]
    random.shuffle(rand)
    rand = "".join(rand)
    rand = rand[random.randint(0, len(rand) - 1) : -1][:10]
    return rand.lower()


@app.route("/delete_note", methods=["POST"])
def delete_note():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    title = request.form.get("title")
    content = request.form.get("content")

    db.delete_note(username, title, content)

    return redirect(url_for("index"))


@app.route("/search")
def searchnotes():
    query = request.args.get("q", "").lower().strip()
    username = session.get("username")
    if username:
        return jsonify(db.search_notes(query, username, conn))
    else:
        return jsonify({"error": "not logged in!!!!"})


@app.route("/")
def index():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    raw_notes = db.get_notes(username)
    raw_notes = [(x["title"], x["content"], x["time"], x["code"]) for x in raw_notes]
    notes = [
        (title, content, time.strftime("%b %d, %Y at %I:%M %p"), code)
        for title, content, time, code in raw_notes
    ]
    if not request.args.get("query"):
        return render_template(
            "index.html", username=username, notes=notes, show_search_box=True
        )
    queried_notes = db.search_notes(request.args.get("query"), username, conn)
    return render_template(
        "index.html",
        did_search=True,
        username=username,
        notes=queried_notes,
        show_search_box=False,
        query=request.args.get("query"),
    )


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
        if user and user["password"] == password:  # password is 3rd column
            session["username"] = username
            flash("Logged in successfully!")
            print("redirecting")
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
            db.create_note(title, content, username, datetime.now(), generate())
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
    username = session.get("username")
    return render_template("create.html", username=username)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template(
        "edit.html", username=username, noteid=request.args.get("id")
    )


@app.route("/edit_note", methods=["POST"])
def edit_note():
    username = session.get("username")
    if (not username) or username not in all_users():
        return redirect(url_for("login"))

    db.edit_note(request.args.get("id"), request.form.get("content"))

    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if get_user(username):
            flash("Username already exists, please choose another.")
            return render_template("signup.html")
        db.create_account(username, password)
        flash("Account created! Please log in.")
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template("signup.html", username=username)


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!")
    return redirect(url_for("index"))


# if __name__ == "__main__": # no need, this launch is handled by Vercel
#     app.run("0.0.0.0", port=5000, debug=True)
