import os
from flask import render_template, redirect, request, session, abort
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


@app.route("/store", methods=["GET"])
def store():

    if request.method == "GET":
        if "username" not in session:
            return render_template("index.html", login_message=True)

    query = utils.get_all_products()
    products = []

    for product in query:

        if product[4] > 0:
            products.append(product)

    return render_template("store.html", products=products)


@ app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "GET":
        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    return render_template("admin.html")


@ app.route("/add_product", methods=["POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["add_product_name"]
        product_description = request.form["product_description"]
        product_price = request.form["product_price"]
        product_amount = request.form["add_product_amount"]

        result = db_logic.add_new_product(
            product_name, product_description, product_price, product_amount
        )

        if result is False:
            return render_template("admin.html", error=True)

        return render_template("admin.html", success=True)


@ app.route("/increase_product_amount")
def increase_product_amount():
    # TODO: finish, this, html and css
    pass


@ app.route("/testdatabase")
def test_database():

    if db.engine.execute("SELECT 1"):
        return 'DB connection'

    return 'ERROR'


if __name__ == "__main__":
    app.run(debug=True)
