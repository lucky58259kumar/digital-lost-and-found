from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# =========================
# DATABASE CONFIGURATION
# =========================

# Store the database in the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "lost_found.db")


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lost_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            location TEXT,
            date_lost TEXT,
            contact TEXT,
            status TEXT DEFAULT 'LOST'
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")
    print("Database location:", DATABASE)


# IMPORTANT:
# Initialize database when Flask imports this file.
# This works with Gunicorn on Render.
init_db()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REPORT LOST ITEM
# =========================

@app.route("/lost", methods=["GET", "POST"])
def lost():

    if request.method == "POST":

        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        date_lost = request.form.get("date_lost", "").strip()
        contact = request.form.get("contact", "").strip()

        # Basic validation
        if not item_name or not category:
            return "Item name and category are required.", 400

        print("\n========== LOST ITEM SUBMITTED ==========")
        print("Item Name:", item_name)
        print("Category:", category)
        print("Description:", description)
        print("Location:", location)
        print("Date Lost:", date_lost)
        print("Contact:", contact)
        print("Status: LOST")
        print("=========================================\n")

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO lost_items
            (
                item_name,
                category,
                description,
                location,
                date_lost,
                contact,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item_name,
            category,
            description,
            location,
            date_lost,
            contact,
            "LOST"
        ))

        conn.commit()
        conn.close()

        return render_template("success.html")

    return render_template("lost.html")


# =========================
# REPORT FOUND ITEM
# =========================

@app.route("/found", methods=["GET", "POST"])
def found():

    if request.method == "POST":

        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        date_found = request.form.get("date_found", "").strip()
        contact = request.form.get("contact", "").strip()

        # Basic validation
        if not item_name or not category:
            return "Item name and category are required.", 400

        print("\n========== FOUND ITEM SUBMITTED ==========")
        print("Item Name:", item_name)
        print("Category:", category)
        print("Description:", description)
        print("Location:", location)
        print("Date Found:", date_found)
        print("Contact:", contact)
        print("Status: FOUND")
        print("==========================================\n")

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO lost_items
            (
                item_name,
                category,
                description,
                location,
                date_lost,
                contact,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item_name,
            category,
            description,
            location,
            date_found,
            contact,
            "FOUND"
        ))

        conn.commit()
        conn.close()

        return render_template("success.html")

    return render_template("found.html")


# =========================
# SEARCH LOST & FOUND ITEMS
# =========================

@app.route("/search", methods=["GET", "POST"])
def search():

    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

    else:
        keyword = request.args.get("keyword", "").strip()

    conn = get_db_connection()

    # =========================
    # SHOW ALL ITEMS
    # =========================

    if keyword == "":

        items = conn.execute("""
            SELECT *
            FROM lost_items
            ORDER BY id DESC
        """).fetchall()

    # =========================
    # SEARCH ITEMS
    # =========================

    else:

        search_keyword = "%" + keyword + "%"

        items = conn.execute("""
            SELECT *
            FROM lost_items
            WHERE item_name LIKE ?
               OR category LIKE ?
               OR description LIKE ?
               OR location LIKE ?
               OR status LIKE ?
            ORDER BY id DESC
        """, (
            search_keyword,
            search_keyword,
            search_keyword,
            search_keyword,
            search_keyword
        )).fetchall()

    conn.close()

    return render_template(
        "search.html",
        items=items,
        keyword=keyword
    )


# =========================
# HEALTH CHECK
# =========================

@app.route("/health")
def health():
    return "Digital Lost & Found is running successfully!"


# =========================
# RUN APPLICATION LOCALLY
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )