# 📊 Pan-African Economic Intelligence Platform (PAEIP)

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

### ✅ CSV Export

- A dedicated page to download the full dataset
- File generated dynamically from the SQLite database
- Only available for logged-in users

### ✅ Clean UI

- Modern layout
- Soft gradient background
- Light-blue brand color (instead of the darker purple)

## 📁 Project Structure

```
├── app.py
├── create_db.py
├── requirements.txt
├── README.md
├── paei.db                   # auto-created after running create_db.py
│
├── East-African-data.json    # cointains the dataset in json format
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── signup.html
│   ├── signin.html
│   ├── dashboard.html
│   └── download.html
│
└── static/
    ├── css/style.css
    └── js/dashboard.js
```

## 🛠 Installation & Setup

1. **First option: Run the deployed version using:**
```
https://paeip-dashboard.onrender.com
```
2. **Second option: Clone and run the program locally**

1️⃣ **Clone the Project**
```
git clone https://github.com/Gaddiel05/PAEIP-Project.git
cd paei_dashboard
```
2️⃣ **Create and Activate a Virtual Environment**
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
Windows:
```
python -m venv venv
venv\Scripts\activate
```

3️⃣ **Install Dependencies**
```
pip install -r requirements.txt
```
> No need to install sqlite3 or json — they are included in Python’s standard library.

4️⃣ **Create the Database**
```
python create_db.py
```

▶️ **Running the Application**
Start the Flask server:
```
python app.py
```
Then open in the browser:
```
http://127.0.0.1:5000
```

## 📝 Authors
Gaddiel Irakoze

## License
This project is for academic purposes and not intended for commercial use.
