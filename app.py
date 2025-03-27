from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "/mnt/data/app.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if request.method == "POST":
        text = request.form.get("message")
        c.execute("INSERT INTO messages (text) VALUES (?)", (text,))
        conn.commit()
    
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    conn.close()
    
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
