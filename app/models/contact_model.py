# /app/models/contact_model.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Initialize 'db' object here, but bind it to the app in server.py
db = SQLAlchemy()

class Contact(db.Model):
    """Model to store contact form submissions."""
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    email_address = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    service_type = db.Column(db.String(30), nullable=False)
    project_name = db.Column(db.String(50), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Contact {self.user_name}>"
    
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
    