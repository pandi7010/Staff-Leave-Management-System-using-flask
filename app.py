from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB = 'database.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        conn.execute('''
            CREATE TABLE leave_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                date TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'Pending'
            );
        ''')
        conn.commit()
        conn.close()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    leaves = conn.execute('SELECT * FROM leave_requests ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', leaves=leaves)

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    department = request.form['department']
    date = request.form['date']
    reason = request.form['reason']
    conn = get_db()
    conn.execute('INSERT INTO leave_requests (name, department, date, reason) VALUES (?, ?, ?, ?)', 
                 (name, department, date, reason))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>/<string:action>')
def update_status(id, action):
    if action in ['Approved', 'Rejected']:
        conn = get_db()
        conn.execute('UPDATE leave_requests SET status = ? WHERE id = ?', (action, id))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
