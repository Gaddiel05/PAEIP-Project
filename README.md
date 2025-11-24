# PAEIP-Project

## 📊 Pan-African Economic Intelligence Platform (PAEIP)

This project is a Flask-based web application that provides an interactive economic dashboard for East African countries, built using:
- Flask (backend)
- SQLite (database)
- Chart.js (interactive charts)
- HTML/CSS/JS (front-end)
- CSV export functionality
- User authentication (signup/signin)

It loads macroeconomic data from the JSON file, East-African-data.json, and stores it into an SQLite database (paei.db).

## ✨ Features

### ✅ Dashboard

Interactive dashboard showing:
- Population
- GDP growth
- GDP sector composition
- Employment sectors
- FDI
- Unemployment
- Inflation
- Nominal GDP

All displayed as dynamic charts (Chart.js) and KPIs.

### ✅ Filters

- Filter by country
- Filter by year
- Auto-refresh of charts and KPIs

### ✅ Authentication

- User signup
- User login
- Sessions
- Password hashing (Werkzeug)

### ✅ Database

- SQLite with:
    - metrics table (economic indicators)
    - users table (name, email, hashed password)



