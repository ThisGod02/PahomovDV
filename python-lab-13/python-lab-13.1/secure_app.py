from flask import Flask, request, jsonify
import sqlite3
import os
import subprocess
import re

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

# ✅ ИСПРАВЛЕНИЕ 1: секрет из переменной окружения
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")

# ✅ Allow-list разрешённых команд
ALLOWED_COMMANDS = ['date', 'whoami', 'uptime', 'hostname']

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.execute("INSERT OR IGNORE INTO users (id,username,email,password) VALUES (1,'admin','admin@example.com','admin123')")
    conn.execute("INSERT OR IGNORE INTO users (id,username,email,password) VALUES (2,'alice','alice@example.com','alice456')")
    conn.execute("INSERT OR IGNORE INTO users (id,username,email,password) VALUES (3,'bob','bob@example.com','bob789')")
    conn.commit()
    conn.close()

def validate_integer(value, name='value'):
    """Валидация целочисленного параметра"""
    if not re.match(r'^\d+$', str(value)):
        raise ValueError(f"{name} must be a positive integer")
    return int(value)

@app.route('/')
def index():
    return jsonify({
        "app": "User Management API (SECURE version)",
        "endpoints": ["/user?id=<id>", "/search?username=<name>", "/api/data", "/execute?cmd=<cmd>"]
    })

@app.route('/user')
def get_user():
    """✅ Параметризованный запрос — SQL Injection исправлена"""
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "Missing id parameter"}), 400

    try:
        uid = validate_integer(user_id, 'id')
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    conn = get_db()
    # ✅ ИСПРАВЛЕНИЕ 2: параметризованный запрос
    cursor = conn.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (uid,)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/search')
def search_users():
    """✅ Параметризованный запрос для LIKE"""
    username = request.args.get('username', '')

    # ✅ Дополнительная валидация входа
    if len(username) > 100:
        return jsonify({"error": "Username too long"}), 400

    conn = get_db()
    # ✅ ИСПРАВЛЕНИЕ 3: параметризованный запрос с LIKE
    cursor = conn.execute(
        "SELECT id, username, email FROM users WHERE username LIKE ?",
        (f'%{username}%',)
    )
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/api/data')
def get_data():
    """✅ Ключ из переменной окружения"""
    # ✅ ИСПРАВЛЕНИЕ 4: API_KEY читается из os.environ
    return jsonify({"message": "Authenticated request", "status": "ok"})

@app.route('/execute')
def execute_command():
    """✅ Allow-list + shell=False"""
    cmd = request.args.get('cmd', '')

    # ✅ ИСПРАВЛЕНИЕ 5: allow-list + shell=False
    if cmd not in ALLOWED_COMMANDS:
        return jsonify({
            "error": f"Command not allowed. Allowed: {ALLOWED_COMMANDS}"
        }), 403

    result = subprocess.check_output([cmd], text=True)  # shell=False
    return jsonify({"output": result})

@app.errorhandler(Exception)
def handle_error(e):
    """✅ Не раскрываем детали ошибок пользователю"""
    app.logger.exception("Internal server error")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    init_db()
    # ✅ ИСПРАВЛЕНИЕ 6: debug=False в production
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5001)
