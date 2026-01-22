from flask import Flask, request, send_from_directory
import psycopg2
import psycopg2.extras
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ---------------- CONFIG ----------------
# Replace these with your Render PostgreSQL credentials
DB_CONFIG = {
    "host": "YOUR_DB_HOST",
    "port": 5432,
    "dbname": "YOUR_DB_NAME",
    "user": "YOUR_DB_USER",
    "password": "YOUR_DB_PASSWORD"
}

# ---------------- DATABASE ----------------
def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Create table if it doesn't exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        event TEXT,
        visitor_id TEXT,
        session_id TEXT,
        page TEXT,
        referrer TEXT,
        browser TEXT,
        ip_address TEXT,
        screen TEXT,
        data JSONB,
        timestamp BIGINT,
        received_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
        conn.commit()
    print("Database initialized.")

# ---------------- ROUTES ----------------

@app.route("/collect", methods=["POST"])
def collect():
    raw = request.data.decode("utf-8")
    if not raw:
        return "", 204

    event = json.loads(raw)
    ip_address = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    insert_sql = """
    INSERT INTO events (
        event, visitor_id, session_id, page,
        referrer, browser, ip_address, screen, data, timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        event.get("event"),
        event.get("visitor_id"),
        event.get("session_id"),
        event.get("page"),
        event.get("referrer"),
        event.get("browser"),
        ip_address,
        event.get("screen"),
        json.dumps(event),
        event.get("timestamp")
    )

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(insert_sql, values)
        conn.commit()

    return "", 204

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/")
def health():
    return {"status": "analytics running"}

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
