
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime, timezone

app = Flask(__name__)
app.config.from_object(Config)  # Load DB config
db = SQLAlchemy(app)

# Model for Contact messages
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    email_address = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    service_type = db.Column(db.String(30), nullable=False)
    project_name = db.Column(db.String(50), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Contact {self.user_name}>"
    
    # Method to serialize the Contact object into a dictionary for JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "service_type": self.service_type,
            "project_name": self.project_name,
            "project_description": self.project_description,
            "created_at": self.created_at.isoformat()
        }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_name = request.form["user_name"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]
        service_type = request.form["service_type"]
        project_name = request.form["project_name"]
        project_description = request.form["project_description"]

        new_msg = Contact(user_name=user_name, email_address=email_address, phone_number=phone_number, service_type=service_type, project_name=project_name, project_description=project_description)
        try:
            db.session.add(new_msg)
            db.session.commit()
            flash("Thanks for contacting me! I'll get back to you soon.")
            return redirect(url_for("contact"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.")
            print(f"Error: {e}")
            return redirect(url_for("contact"))
    return render_template("contact.html")

# --- API Endpoints ---

@app.route("/api/contacts", methods=["GET", "POST"])
def manage_contacts():
    """
    Handles GET requests to list all contacts and POST requests to create a new contact.
    """
    if request.method == "POST":
        # Create a new contact from JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        required_fields = ["user_name", "email_address", "phone_number", "service_type", "project_name", "project_description"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_contact = Contact(
            user_name=data["user_name"],
            email_address=data["email_address"],
            phone_number=data["phone_number"],
            service_type=data["service_type"],
            project_name=data["project_name"],
            project_description=data["project_description"]
        )
        
        try:
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({
                "message": "Contact created successfully.",
                "contact": new_contact.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            print(f"Error creating contact: {e}")
            return jsonify({"error": "Could not create contact."}), 500

    # If it's a GET request
    contacts = Contact.query.all()
    contacts_list = [contact.to_dict() for contact in contacts]
    return jsonify(contacts_list)

@app.route("/api/contacts/<int:id>", methods=["GET"])
def get_contact(id):
    """Returns a single contact message by ID as JSON."""
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.to_dict())

@app.route("/api/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    """Deletes a contact message by ID."""
    contact = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": f"Contact with id {id} deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not delete contact."}), 500

if __name__ == "__main__":
    app.run(debug=True)
