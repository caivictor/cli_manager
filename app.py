from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.expanduser("~/.cli_manager.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.png", mimetype="image/png")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/commands')
def get_commands():
    sort_by = request.args.get('sort', 'last_used')
    search_query = request.args.get('q', '').lower()
    
    conn = get_db_connection()
    c = conn.cursor()
    
    query = "SELECT * FROM commands"
    params = []
    
    if search_query:
        query += " WHERE lower(command) LIKE ?"
        params.append(f"%{search_query}%")
        
    if sort_by == 'frequency':
        query += " ORDER BY frequency DESC, last_used DESC"
    else:
        query += " ORDER BY last_used DESC"
        
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    commands = [dict(row) for row in rows]
    return jsonify(commands)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
