# Cypherware – Webapp

This is the Cypherware project built with **Flask (Python)**.  
The design has a retro 90s / Matrix aesthetic, and it includes an introduction, projects, and contact information.

---

## 🚀 Features
- Flask-based backend
- HTML templates with custom styling
- Retro 90s Matrix-inspired design
- Home page with greeting:
    -To be define

---

## 📂 Project Structure
├── server.py             # Flask entry point
├── templates/
│   ├── base.html
│   ├── home.html
│   └── …
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt
├── .gitignore
└── README.

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
    -To be define

python3 -m venv myenv
source myenv/bin/activate   # macOS/Linux
myenv\bin\activate      # Windows

pip install -r requirements.txt

#run
export FLASK_APP=server.py && flask run --debug
```

📌 Future Improvements
	•	Add more sections (Projects, About, Blog, Contact).
	•	Improve responsiveness for mobile devices.
	•	Deploy to a hosting service (Heroku, Vercel, etc.).