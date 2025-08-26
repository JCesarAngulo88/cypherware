# export FLASK_APP=server.py && flask run --debug

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")  # Load DB config
db = SQLAlchemy(app)

# Model for Contact messages
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

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
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_msg = Contact(name=name, email=email, message=message)
        db.session.add(new_msg)
        db.session.commit()
        flash("Thanks for contacting me! I'll get back to you soon.")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.secret_key = "supersecretkey"  # needed for flash messages
    app.run(debug=True)
