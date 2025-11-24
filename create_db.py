# create_db.py
import json
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

JSON_PATH = "East-African-data.json"
DB_PATH = "paei.db"

def ensure_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # metrics table: one row per country per year (year as integer starting 2015)
    c.execute("""
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        year INTEGER NOT NULL,
        nominalGDP REAL,
        gdpGrowth REAL,
        unemployment REAL,
        imports REAL,
        exports REAL,
        nationalDebt REAL,
        gdpPerCapita REAL,
        povertyRate REAL,
        agricultureShare REAL,
        industryShare REAL,
        servicesShare REAL,
        miningShare REAL,
        othersShare REAL,
        agricultureEmployment REAL,
        industryEmployment REAL,
        servicesEmployment REAL,
        miningEmployment REAL,
        othersEmployment REAL,
        population REAL,
        inflation REAL,
        fdi REAL,
        exchangeRate REAL,
        interestRate REAL,
        foreignReserves REAL,
        publicSpending REAL,
        budgetDeficit REAL
    )
    """)

    c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    return conn, c

def load_json_and_insert(conn, c):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # We'll assume the arrays correspond to years 2015..2024 (10 values)
    base_year = 2015
    for country, metrics in data.items():
        # determine length (use min length across metrics arrays)
        lengths = [len(v) for k,v in metrics.items() if isinstance(v, list)]
        n = min(lengths) if lengths else 0
        for i in range(n):
            year = base_year + i
            row = {
                'country': country,
                'year': year,
                'nominalGDP': metrics.get('nominalGDP', [None])[i],
                'gdpGrowth': metrics.get('gdpGrowth', [None])[i],
                'unemployment': metrics.get('unemployment', [None])[i],
                'imports': metrics.get('imports', [None])[i],
                'exports': metrics.get('exports', [None])[i],
                'nationalDebt': metrics.get('nationalDebt', [None])[i],
                'gdpPerCapita': metrics.get('gdpPerCapita', [None])[i],
                'povertyRate': metrics.get('povertyRate', [None])[i],
                'agricultureShare': metrics.get('agricultureShare', [None])[i],
                'industryShare': metrics.get('industryShare', [None])[i],
                'servicesShare': metrics.get('servicesShare', [None])[i],
                'miningShare': metrics.get('miningShare', [None])[i],
                'othersShare': metrics.get('othersShare', [None])[i],
                'agricultureEmployment': metrics.get('agricultureEmployment', [None])[i],
                'industryEmployment': metrics.get('industryEmployment', [None])[i],
                'servicesEmployment': metrics.get('servicesEmployment', [None])[i],
                'miningEmployment': metrics.get('miningEmployment', [None])[i],
                'othersEmployment': metrics.get('othersEmployment', [None])[i],
                'population': metrics.get('population', [None])[i],
                'inflation': metrics.get('inflation', [None])[i],
                'fdi': metrics.get('fdi', [None])[i],
                'exchangeRate': metrics.get('exchangeRate', [None])[i],
                'interestRate': metrics.get('interestRate', [None])[i],
                'foreignReserves': metrics.get('foreignReserves', [None])[i],
                'publicSpending': metrics.get('publicSpending', [None])[i],
                'budgetDeficit': metrics.get('budgetDeficit', [None])[i],
            }
            placeholders = ",".join("?"*len(row))
            columns = ",".join(row.keys())
            c.execute(f"INSERT INTO metrics ({columns}) VALUES ({placeholders})", tuple(row.values()))
    conn.commit()

def create_sample_user(conn, c):
    # Create an example user: email: admin@example.com password: secret123
    pw = generate_password_hash("secret123")
    try:
        c.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                  ("Admin User", "admin@example.com", pw))
        conn.commit()
    except Exception as e:
        print("Sample user creation failed:", e)

def build_database():
    conn, c = ensure_db()
    load_json_and_insert(conn, c)
    create_sample_user(conn, c)
    conn.close()
    print("Database created at paei.db using", JSON_PATH)

if __name__ == "__main__":
    build_database()
