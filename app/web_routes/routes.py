from flask import Blueprint, render_template, session, request, redirect, url_for

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
def home():
    return render_template("home.html")

@web_bp.route("/game")
def game():
    return render_template("gamefile.html", user=session.get("user"))