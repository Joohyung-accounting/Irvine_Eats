# Eats_Irvine
Irvine Eats project in Summer 2025

---

## 📌 Features

- Feature: Describe what this project is about..!

---

## ⚙️ Requirement Analysis

- [Use Case (WIP)](https://docs.google.com/document/d/1IAnVgQd9QHpj51bYlSgmeKAkl5NXA9qgdJO_fT-MpDE/edit?tab=t.0)
- [Site map (WIP)](https://docs.google.com/document/d/19GwnO8bY4xKlP4oP5uUCL7DpsvbebuYR3BsbsPs0up0/edit?tab=t.0)
- [Functional Requirements (WIP)](https://docs.google.com/document/d/1OTKmrjbNyQUgryRAbtTqK9v_dzpB85QWc0uKcX-rLSw/edit?tab=t.0#heading=h.xmffppwouut9)
- [Rubric Specification (WIP)](https://docs.google.com/document/d/1scqNvKiBJua47wc_B1eVYJyfld1IAn4bacIdrBlhtGw/edit?usp=sharing)
- [Wireframe (WIP)](https://www.figma.com/design/QgcqCbiAI8F39e5pzTTLQq/Wireframes?node-id=0-1&t=BOeItQWiqv3FYcil-1)
- [ER Diagram (WIP)](https://www.figma.com/board/mXQpHWN2LEzHCccDBezmoh/ER-diagram?node-id=1-2&t=THrdH2KD7LETpayS-0)
---

# 🚀 Eats Irvine

A full-stack web application that provides restaurant information in Irvine using the Google Places API.

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

```
git clone https://github.com/caspi46/Eats_Irvine.git
cd Eats_Irvine
```

---

### 2. Backend Setup (Flask)

```
cd irvine_eats_backend
python -m venv .venv
.venv\Scripts\activate   # Windows (PowerShell)
pip install -r requirements.txt
```

---

### 🔑 Set Google API Key

```
set google_api=YOUR_API_KEY   # Windows (PowerShell)
```

---

### 3. Seed Database (Restaurant Data)

```
python -m scripts.seed_restaurants
```

---

### 4. Run Backend Server

```
python app.py
```

Backend runs at:
http://127.0.0.1:5000

---

### 5. Frontend Setup (React)

```
cd ../irvine_eats_frontend
npm install
npm run dev
```

Frontend runs at:
http://localhost:5173

---

## 📁 Project Structure

```
Eats_Irvine/
│
├── irvine_eats_backend/
│   ├── app/
│   │   ├── routes.py
│   │   └── irvine_eats.db
│   ├── scripts/
│   └── app.py
│
├── irvine_eats_frontend/
│   └── src/
│       └── App.jsx
│
└── README.md
```

---

## 📌 Notes

* Make sure your Google API key is set before seeding the database.
* Backend must be running before starting the frontend.
* If `npm` is not recognized, install Node.js and restart your terminal.

---

## 👨‍💻 Tech Stack

* Frontend: React (Vite)
* Backend: Flask (Python)
* Database: SQLite
* API: Google Places API
