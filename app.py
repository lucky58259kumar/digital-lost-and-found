from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "lost_found.db"


# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect(DATABASE)

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

    # Add status column to an existing database
    try:
        conn.execute(
            "ALTER TABLE lost_items ADD COLUMN status TEXT DEFAULT 'LOST'"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    conn.commit()
    conn.close()


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

        item_name = request.form.get("item_name")
        category = request.form.get("category")
        description = request.form.get("description")
        location = request.form.get("location")
        date_lost = request.form.get("date_lost")
        contact = request.form.get("contact")

        # Print submitted data in terminal
        print("\n========== LOST ITEM SUBMITTED ==========")
        print("Item Name:", item_name)
        print("Category:", category)
        print("Description:", description)
        print("Location:", location)
        print("Date Lost:", date_lost)
        print("Contact:", contact)
        print("Status: LOST")
        print("=========================================\n")

        # Save to database
        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO lost_items
            (item_name, category, description, location, date_lost, contact, status)
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

        item_name = request.form.get("item_name")
        category = request.form.get("category")
        description = request.form.get("description")
        location = request.form.get("location")
        date_found = request.form.get("date_found")
        contact = request.form.get("contact")

        # Print submitted data in terminal
        print("\n========== FOUND ITEM SUBMITTED ==========")
        print("Item Name:", item_name)
        print("Category:", category)
        print("Description:", description)
        print("Location:", location)
        print("Date Found:", date_found)
        print("Contact:", contact)
        print("Status: FOUND")
        print("==========================================\n")

        # Save to database
        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO lost_items
            (item_name, category, description, location, date_lost, contact, status)
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

        return "Found item submitted successfully!"

    return render_template("found.html")


# =========================
# SEARCH LOST & FOUND ITEMS
# =========================

@app.route("/search", methods=["GET", "POST"])
def search():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    items = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

    elif request.method == "GET":
        keyword = request.args.get("keyword", "").strip()

    # Show all items if search box is empty
    if keyword == "":

        items = conn.execute("""
            SELECT *
            FROM lost_items
            ORDER BY id DESC
        """).fetchall()

    else:

        search_keyword = "%" + keyword + "%"

        items = conn.execute("""
            SELECT *
            FROM lost_items
            WHERE item_name LIKE ?
               OR category LIKE ?
               OR description LIKE ?
               OR location LIKE ?
            ORDER BY id DESC
        """, (
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
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    init_db()
    app.run(debug=True)