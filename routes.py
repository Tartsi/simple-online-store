import os
from flask import render_template, redirect, request, session
import utils
import db_logic
from app import app
from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        result = db_logic.add_user(username, password, 0)

        if result is False:
            return render_template("register.html", error=True)

        return render_template("login.html", success=True)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        result = utils.login(username, password)

        if result is False:
            return render_template("login.html", error=True)

        session["username"] = username
        session["user_id"] = result[0]
        session["admin_status"] = result[2]
        session["csrf_token"] = os.urandom(16).hex()
        return redirect("/store")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/store")
def store():
    products = utils.get_all_products()
    return render_template("store.html", products=products)


@app.route("/testdatabase")
def test_database():

    if db.engine.execute("SELECT 1"):
        return 'DB connection'

    return 'ERROR'


if __name__ == "__main__":
    app.run(debug=True)
