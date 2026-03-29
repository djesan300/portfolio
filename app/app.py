from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "portfolio"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "password")
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
        );
    """)
    cur.execute("SELECT COUNT(*) FROM skills")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO skills (name) VALUES
            ('Ansible'), ('Docker'), ('Linux'), ('AWS EC2'), ('PostgreSQL');
        """)
    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO projects (name, description) VALUES
            ('Portfolio site', 'Flask + PostgreSQL + Docker + Ansible'),
            ('Ansible automation', 'Автоматизация деплоя на EC2');
        """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM skills")
    skills = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT name, description FROM projects")
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", skills=skills, projects=projects)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5050)
