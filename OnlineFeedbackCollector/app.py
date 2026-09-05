from flask import (Flask,render_template,request,redirect,url_for,flash,jsonify,Response,session,)
import sqlite3
import csv
import io
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comments TEXT NOT NULL,
            date_submitted TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    comments = request.form.get("comments", "").strip()

    try:
        rating = int(request.form.get("rating", "0"))
    except ValueError:
        rating = 0

    if not name or not email or not comments or rating not in range(1, 6):
        flash("Please complete all fields and select a rating from 1 to 5.", "error")
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute(
        "INSERT INTO feedback (name, email, rating, comments, date_submitted) VALUES (?, ?, ?, ?, ?)",
        (name, email, rating, comments, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()

    flash("Thank you! Your feedback has been submitted successfully.", "success")
    return redirect(url_for("index"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Demo credentials: change before deployment.
        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin_login.html")


@app.route("/admin-logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():
    conn = get_db()
    feedback = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    total = conn.execute("SELECT COUNT(*) AS c FROM feedback").fetchone()["c"]
    avg = conn.execute("SELECT AVG(rating) AS a FROM feedback").fetchone()["a"] or 0
    distribution = [
        conn.execute(
            "SELECT COUNT(*) AS c FROM feedback WHERE rating = ?", (r,)
        ).fetchone()["c"]
        for r in range(1, 6)
    ]
    conn.close()
    return render_template(
        "admin.html",
        feedback=feedback,
        total=total,
        average=round(avg, 2),
        distribution=distribution,
    )


@app.route("/api/feedback")
@admin_required
def api_feedback():
    conn = get_db()
    rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/export-csv")
@admin_required
def export_csv():
    conn = get_db()
    rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "rating", "comments", "date_submitted"])
    for row in rows:
        writer.writerow(
            [
                row["id"],
                row["name"],
                row["email"],
                row["rating"],
                row["comments"],
                row["date_submitted"],
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=feedback.csv"},
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
