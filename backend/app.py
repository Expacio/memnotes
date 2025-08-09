
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import random, string

DATABASE = os.environ.get("MEMNOTES_DB", "users.db")

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
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

def generate_code():
    rand = ''.join([x for x in string.ascii_letters])
    rand = [x for x in rand]
    random.shuffle(rand)
    rand = "".join(rand)
    rand = rand[random.randint(0, len(rand)-1):-1][:10]
    return rand.lower()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me")

@app.route('/api/ping')
def ping():
    return jsonify({"status":"ok"})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return jsonify({'error':'username and password required'}), 400
    if get_user(username):
        return jsonify({'error':'username_taken'}), 409
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    return jsonify({'message':'account_created'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    user = get_user(username)
    if user and user[2] == password:
        session['username'] = username
        return jsonify({'message':'logged_in'}), 200
    return jsonify({'error':'invalid_credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message':'logged_out'}), 200

@app.route('/api/notes', methods=['GET','POST'])
def notes():
    # GET -> list notes for the logged in user (username passed in session or query param for simplicity)
    if request.method == 'GET':
        username = request.args.get('username') or session.get('username')
        if not username:
            return jsonify({'error':'not_authenticated'}), 401
        with sqlite3.connect(DATABASE) as conn:
            raw = conn.execute("SELECT id, title, content, time, code FROM notes WHERE username = ? ORDER BY time DESC",(username,)).fetchall()
        notes = [{'id': r[0], 'title': r[1], 'content': r[2], 'time': r[3], 'code': r[4]} for r in raw]
        return jsonify(notes)
    else:
        username = session.get('username') or (request.get_json() or {}).get('username')
        if not username:
            return jsonify({'error':'not_authenticated'}), 401
        data = request.get_json() or {}
        content = (data.get('content') or '').strip()
        title = data.get('title') or (content[:20] + '...' if len(content)>20 else content)
        if not content:
            return jsonify({'error':'empty_content'}), 400
        code = generate_code()
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO notes (title, content, username, time, code) VALUES (?, ?, ?, ?, ?)", (title, content, username, datetime.now(), code))
            conn.commit()
        return jsonify({'message':'saved','code':code}), 201

@app.route('/api/notes/<code>', methods=['GET','PUT','DELETE'])
def notes_detail(code):
    username = session.get('username') or request.args.get('username')
    if not username:
        return jsonify({'error':'not_authenticated'}), 401
    with sqlite3.connect(DATABASE) as conn:
        if request.method == 'GET':
            cur = conn.execute("SELECT id, title, content, time, code FROM notes WHERE code = ? AND username = ?", (code, username)).fetchone()
            if not cur:
                return jsonify({'error':'not_found'}), 404
            return jsonify({'id':cur[0],'title':cur[1],'content':cur[2],'time':cur[3],'code':cur[4]})
        elif request.method == 'PUT':
            data = request.get_json() or {}
            content = data.get('content')
            conn.execute("UPDATE notes SET content = ? WHERE code = ? AND username = ?", (content, code, username))
            conn.commit()
            return jsonify({'message':'updated'})
        else:
            conn.execute("DELETE FROM notes WHERE code = ? AND username = ?", (code, username))
            conn.commit()
            return jsonify({'message':'deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)), debug=True)
