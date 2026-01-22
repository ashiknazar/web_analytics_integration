from flask import Flask, request, send_from_directory
import sqlite3
import json

app = Flask(__name__)
DB_NAME = "demo.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                browser TEXT,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/collect", methods=["POST"])
def collect():
    raw = request.data.decode("utf-8")
    print("RAW EVENT:", raw)

    data = json.loads(raw) if raw else {}

    browser = data.get("browser", "unknown")
    ip_address = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO analytics_events (ip_address, browser) VALUES (?, ?)",
            (ip_address, browser)
        )

    return "", 204


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/")
def health():
    return {"service": "analytics", "status": "running"}


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
