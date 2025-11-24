# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

if not os.path.exists("paei.db"):
    import create_db

DB_PATH = "paei.db"
SECRET_KEY = "replace_this_with_a_strong_random_secret"

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

# Pages
@app.route("/")
def home():
    return render_template("home.html", user=session.get('user'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        pw_hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                       (name, email, pw_hash))
            db.commit()
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Email already used")
    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = {"id": user['id'], "name": user['name'], "email": user['email']}
            return redirect(url_for('dashboard'))
        else:
            return render_template("signin.html", error="Invalid credentials")
    return render_template("signin.html")

@app.route("/signout")
def signout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    if not session.get('user'):
        return redirect(url_for('signin'))
    return render_template("dashboard.html", user=session.get('user'))

# API endpoints
@app.route("/api/countries")
def api_countries():
    db = get_db()
    rows = db.execute("SELECT DISTINCT country FROM metrics ORDER BY country").fetchall()
    countries = [r['country'] for r in rows]
    return jsonify(countries)

@app.route("/api/years")
def api_years():
    db = get_db()
    rows = db.execute("SELECT DISTINCT year FROM metrics ORDER BY year").fetchall()
    years = [r['year'] for r in rows]
    return jsonify(years)

@app.route("/api/data")
def api_data():
    """
    Query parameters:
     - country (optional)
     - year (optional, integer)
    """
    country = request.args.get('country')
    year = request.args.get('year', type=int)

    db = get_db()
    query = "SELECT * FROM metrics WHERE 1=1"
    params = []
    if country:
        query += " AND country = ?"
        params.append(country)
    if year:
        query += " AND year = ?"
        params.append(year)
    query += " ORDER BY year ASC"
    rows = db.execute(query, params).fetchall()
    result = [dict(r) for r in rows]
    return jsonify(result)

@app.route("/download")
def download_page():
    if not session.get('user'):
        return redirect(url_for('signin'))
    return render_template("download.html", user=session.get('user'))


@app.route("/api/download_csv")
def download_csv():
    if not session.get('user'):
        return redirect(url_for('signin'))

    import csv
    from io import StringIO
    db = get_db()

    # Fetch all data
    rows = db.execute("SELECT * FROM metrics ORDER BY country, year").fetchall()
    if not rows:
        return "No data available", 404

    # Convert SQLite rows → CSV using StringIO buffer
    si = StringIO()
    writer = csv.writer(si)

    # Write header
    writer.writerow(rows[0].keys())

    # Write rows
    for r in rows:
        writer.writerow([r[k] for k in r.keys()])

    output = si.getvalue()
    si.close()

    # Send file as download
    from flask import Response
    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=paei_data_export.csv"
        }
    )

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("Database not found. Run create_db.py first.")
    app.run(debug=True, host="0.0.0.0", port=5000)