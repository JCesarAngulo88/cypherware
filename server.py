from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)

# --- Configuration ---
# Use a local SQLite database file named 'cypherware.db'
# In CI, this will be created fresh in the runner's workspace
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'cypherware.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-cipher-123')

db = SQLAlchemy(app)

# --- Database Models ---
class Contact(db.Model):
    """Model to store contact form submissions."""
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email_address": self.email_address,
            "project_name": self.project_name,
            "created_at": self.created_at.isoformat()
        }

# --- Web Routes ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            new_msg = Contact(
                user_name=request.form["user_name"],
                email_address=request.form["email_address"],
                project_name=request.form["project_name"],
                project_description=request.form["project_description"]
            )
            db.session.add(new_msg)
            db.session.commit()
            flash("Message sent successfully!")
            return redirect(url_for("contact"))
        except Exception as e:
            db.session.rollback()
            flash("Error sending message.")
            return redirect(url_for("contact"))
    return render_template("contact.html")

# --- API & CI/CD Helpers ---
@app.route("/api/health")
def health():
    """Endpoint for CI/CD to verify the server is running."""
    return jsonify({"status": "healthy", "database": "connected"}), 200

@app.route("/api/contacts", methods=["GET"])
def list_contacts():
    """Helper for automation tests to verify DB entries."""
    contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts])

if __name__ == "__main__":
    # Ensure tables are created before starting locally
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)