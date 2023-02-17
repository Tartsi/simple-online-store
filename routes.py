import os
from flask import render_template, redirect, request, session
import db_fetcher
import db_manager
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

        result = db_manager.add_user(username, password, 0)

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

        result = db_fetcher.login(username, password)

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
    """Displays store once login successfull
    """

    if request.method == "GET":
        if "username" not in session:
            return render_template("index.html", login_message=True)

    products = db_fetcher.get_all_products()

    return render_template("store.html", products=products)


@app.route("/search", methods=["POST"])
def search():
    """Shows all products with the given input
    """

    if request.method == "POST":

        name = request.form["search"]

        products = db_fetcher.search_products(name)

        if products is None:
            return render_template("store.html", products=products, no_product_found=True)

        return render_template("store.html", products=products)


@ app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "GET":
        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    users = db_fetcher.get_all_users()

    if users is None:
        # return this because no admin status user exists
        return render_template("index.html", admin_message=True)

    return render_template("admin.html", users=users)


@ app.route("/add_product", methods=["POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["add_product_name"]
        product_description = request.form["product_description"]
        product_price = request.form["product_price"]
        product_amount = request.form["add_product_amount"]

        result = db_manager.add_new_product(
            product_name, product_description, product_price, product_amount
        )

        if result is False:
            return render_template("admin.html", duplicate_error=True)

        return render_template("admin.html", add_success=True)


@ app.route("/increase_product_amount", methods=["POST"])
def increase_product_amount():

    if request.method == "POST":

        product_name = request.form["increase_product_name"]
        product_amount = request.form["increase_amount"]

        result = db_manager.increase_product_amount(
            product_name, product_amount)

        if result is False:
            return render_template("admin.html", increase_error=True)

        return render_template("admin.html", increase_success=True)


@app.route("/add_review/<int:product_id>", methods=["GET", "POST"])
def add_review(product_id):

    if request.method == "GET":

        if "username" not in session:
            return render_template("index.html", login_message=True)

        return render_template("add_review.html", product_id=product_id)

    if request.method == "POST":

        user_id = session["user_id"]
        rating = request.form["rating"]
        description = request.form["description"]

        if db_fetcher.check_review_adding(user_id, product_id):
            return render_template("add_review.html", product_id=product_id, multiple_review=True)

        result = db_manager.add_new_review(
            user_id, product_id, rating, description)

        if not result:
            return render_template("add_review.html", product_id=product_id, failure=True)

        return render_template("add_review.html", product_id=product_id, success=True)


@app.route("/show_reviews/<int:product_id>", methods=["GET"])
def show_reviews(product_id):

    if request.method == "GET":

        if "username" not in session:
            return render_template("index.html", login_message=True)

    reviews = db_fetcher.get_reviews(product_id)

    if reviews is not None:
        product_name = reviews[0][5]
        product_average_rating = reviews[0][6]
    else:
        product_name = None
        product_average_rating = None

    return render_template("show_reviews.html", reviews=reviews, product_name=product_name, product_average_rating=product_average_rating)


@app.route("/delete_product/<int:product_id>", methods=["GET"])
def delete_product(product_id):

    if request.method == "GET":

        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    result = db_manager.delete_product(product_id)

    if not result:
        return redirect("/logout")

    return redirect("/store")


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():

    if request.method == "GET":

        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    if request.method == "POST":

        username = request.form["username"]
        result = db_manager.delete_user(username)

        if not result:
            return render_template("admin.html", user_delete_error=True)

        return render_template("admin.html", user_delete_success=True)


@ app.route("/testdatabase")
def test_database():

    if db.engine.execute("SELECT 1"):
        return 'DB connection'

    return 'ERROR'


if __name__ == "__main__":
    app.run(debug=True)
