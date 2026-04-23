from flask import Flask, request, jsonify
import sqlite3
import os
import subprocess

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

# ── Hardcoded secret (уязвимость намеренная, исправим в secure_app.py) ──
API_KEY = "demo_training_key_do_not_use"

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

@app.route('/')
def index():
    return jsonify({
        "app": "User Management API (VULNERABLE version)",
        "endpoints": ["/user?id=<id>", "/search?username=<name>", "/api/data", "/execute?cmd=<cmd>"]
    })

@app.route('/user')
def get_user():
    """SQL-инъекция через конкатенацию строк"""
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "Missing id parameter"}), 400

    conn = get_db()
    # ❌ УЯЗВИМОСТЬ: прямая конкатенация — SQL Injection
    query = f"SELECT id, username, email FROM users WHERE id = {user_id}"
    try:
        cursor = conn.execute(query)
        user = cursor.fetchone()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    conn.close()

    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/search')
def search_users():
    """SQL-инъекция через LIKE"""
    username = request.args.get('username', '')
    conn = get_db()
    # ❌ УЯЗВИМОСТЬ: SQL Injection
    query = f"SELECT id, username, email FROM users WHERE username LIKE '%{username}%'"
    cursor = conn.execute(query)
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/api/data')
def get_data():
    """Hardcoded API key"""
    # ❌ УЯЗВИМОСТЬ: секрет прямо в коде
    return jsonify({"api_key": API_KEY, "message": "Sensitive data"})

@app.route('/execute')
def execute_command():
    """Command Injection"""
    cmd = request.args.get('cmd', 'echo Hello')
    # ❌ УЯЗВИМОСТЬ: shell=True + пользовательский ввод
    result = subprocess.check_output(cmd, shell=True, text=True)
    return jsonify({"output": result})

if __name__ == '__main__':
    init_db()
    # ❌ УЯЗВИМОСТЬ: debug=True в production
    app.run(debug=True, host='0.0.0.0', port=5000)
