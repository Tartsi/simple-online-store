from flask import render_template, redirect, request
from app import app
from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/testdatabase")
def test_database():

    if db.engine.execute("SELECT 1"):
        return 'DB connection'

    return 'ERROR'


if __name__ == "__main__":
    app.run(debug=True)
