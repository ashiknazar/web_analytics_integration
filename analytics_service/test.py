import sqlite3

DB_NAME = "demo.db"

def show_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, ip_address, browser, received_at
        FROM analytics_events
        ORDER BY received_at DESC
    """)

    rows = cursor.fetchall()

    if not rows:
        print("No analytics data found.")
    else:
        for row in rows:
            print(f"""
ID        : {row[0]}
IP        : {row[1]}
Browser   : {row[2]}
Timestamp : {row[3]}
----------------------------
""")

    conn.close()

if __name__ == "__main__":
    show_data()
