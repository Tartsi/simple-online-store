import os
from flask import render_template, redirect, request, session
import db_fetcher
import db_manager
from app import app
from db import db

# Generic placeholder, modify this as you will, use it to check admin-registrations
my_admin_password = "admin123"


@ app.route("/testdatabase")
def test_database():

    # After setting up test your connection with this!
    # Manually insert the /testdatabase - part!

    if db.engine.execute("SELECT 1"):
        return 'DB connection'

    return 'ERROR'


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
        admin = request.form.get("admin") == "on"

        if admin:  # if admin checkbox is checked

            admin_password = request.form["admin_password"]

            if admin_password != my_admin_password:
                return render_template("register.html", wrong_admin_password=True)

            result = db_manager.add_user(username, password, 1)

            if result is False:
                return render_template("register.html", error=True)

            return render_template("login.html", admin_success=True)

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
        session["cart"] = []
        session["grand_total"] = 0
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


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "GET":
        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    users = db_fetcher.get_all_users()

    if users is None:
        # return this because no admin status user exists
        return render_template("index.html", admin_message=True)

    completed_orders = db_fetcher.get_all_completed_orders()
    order_information = []

    for item in completed_orders:

        user_order_name = item[0]
        user_products = item[1]
        order_date_created = item[2]
        order_address = item[3]
        order_grand_total = item[4]

        order_dict = {"user_order_name": user_order_name,
                      "user_products": user_products,
                      "order_date_created": order_date_created,
                      "order_address": order_address,
                      "order_grand_total": order_grand_total}

        order_information.append(order_dict)

    return render_template("admin.html", users=users, order_information=order_information)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    products = db_fetcher.get_all_products()

    product_quantity = int(request.form["add_cart_quantity"])

    if product_quantity > db_fetcher.get_product_amount(product_id):
        return render_template("store.html", products=products, out_of_stock=True)

    product_name = db_fetcher.get_product_name(product_id)

    if product_name is None:
        return render_template("store.html", products=products, no_product_found=True)

    product_price = db_fetcher.get_product_price(product_id)
    total_price = product_quantity * product_price

    product = {"name": product_name,
               "quantity": int(product_quantity), "total_price": int(total_price)}

    updated = False

    for index, product_in_cart in enumerate(session["cart"]):
        if product_in_cart["name"] == product_name:
            session["cart"][index] = product
            updated = True
            break

    if not updated:
        session["cart"].append(product)

    grand_total = 0

    for cart_product in session["cart"]:

        grand_total += cart_product["total_price"]

    session["grand_total"] = grand_total

    session.modified = True

    return render_template("store.html", products=products, add_cart_success=True)


@app.route("/add_product", methods=["POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["add_product_name"]
        product_description = request.form["product_description"]
        product_price = request.form["product_price"]
        product_amount = request.form["add_product_amount"]

        result = db_manager.add_new_product(
            product_name, product_description, product_price, product_amount
        )
        users = db_fetcher.get_all_users()
        completed_orders = db_fetcher.get_all_completed_orders()

        order_information = []

        for item in completed_orders:

            user_order_name = item[0]
            user_products = item[1]
            order_date_created = item[2]
            order_address = item[3]
            order_grand_total = item[4]

            order_dict = {"user_order_name": user_order_name,
                          "user_products": user_products,
                          "order_date_created": order_date_created,
                          "order_address": order_address,
                          "order_grand_total": order_grand_total}

            order_information.append(order_dict)

        if users is None:
            # return this because no admin status user exists
            return render_template("index.html", admin_message=True)

        if result is False:
            return render_template("admin.html", duplicate_error=True, users=users, order_information=order_information)

    return render_template("admin.html", add_success=True, users=users, order_information=order_information)


@app.route("/increase_product_amount", methods=["POST"])
def increase_product_amount():

    if request.method == "POST":

        product_name = request.form["increase_product_name"]
        product_amount = request.form["increase_amount"]

        result = db_manager.increase_product_amount(
            product_name, product_amount)
        users = db_fetcher.get_all_users()
        completed_orders = db_fetcher.get_all_completed_orders()

        order_information = []

        for item in completed_orders:
            user_order_name = item[0]
            user_products = item[1]
            order_date_created = item[2]
            order_address = item[3]
            order_grand_total = item[4]

            order_dict = {"user_order_name": user_order_name,
                          "user_products": user_products,
                          "order_date_created": order_date_created,
                          "order_address": order_address,
                          "order_grand_total": order_grand_total}

            order_information.append(order_dict)

        if users is None:
            # return this because no admin status user exists
            return render_template("index.html", admin_message=True)

        if result is False:
            return render_template("admin.html", increase_error=True, users=users, order_information=order_information)

        return render_template("admin.html", increase_success=True, users=users, order_information=order_information)


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


@app.route("/checkout", methods=["GET"])
def checkout():

    if request.method == "GET":

        if "username" not in session:
            return render_template("index.html", login_message=True)

    return render_template("checkout.html")


@app.route("/purchase", methods=["POST"])
def purchase():

    if request.method == "POST":

        if "username" not in session:
            return render_template("index.html", login_message=True)

        user_id = session["user_id"]
        cart_content = session["cart"]
        address = request.form["shipping_address"]

        cart_id = db_manager.add_new_shopping_cart(user_id, cart_content)
        db_manager.add_new_completed_order(
            user_id, cart_id, address, session["grand_total"])

        for cart_product in cart_content:

            name = cart_product["name"]
            quantity = cart_product["quantity"]
            db_manager.decrease_product_amount(name, quantity)

        session["cart"] = []
        session.modified = True

        products = db_fetcher.get_all_products()
        return render_template("store.html", products=products, purchase_success=True)


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

    product_name = db_fetcher.get_product_name(product_id)
    result = db_manager.delete_product(product_id)

    if not result:
        return redirect("/logout")

    if len(session["cart"]) > 0:

        for index, product_in_cart in enumerate(session["cart"]):

            if product_in_cart["name"] == product_name:
                session["grand_total"] -= product_in_cart["total_price"]
                del session["cart"][index]

        session.modified = True

    return redirect("/store")


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():

    users = db_fetcher.get_all_users()
    completed_orders = db_fetcher.get_all_completed_orders()

    order_information = []

    for item in completed_orders:
        user_order_name = item[0]
        user_products = item[1]
        order_date_created = item[2]
        order_address = item[3]
        order_grand_total = item[4]

        order_dict = {"user_order_name": user_order_name,
                      "user_products": user_products,
                      "order_date_created": order_date_created,
                      "order_address": order_address,
                      "order_grand_total": order_grand_total}

        order_information.append(order_dict)

    if request.method == "GET":

        if session.get("admin_status") != 1:
            return render_template("index.html", admin_message=True)

    if request.method == "POST":

        username = request.form["username"]

        if username == session["username"]:
            return render_template("admin.html", delete_session_user=True, users=users, order_information=order_information)

        result = db_manager.delete_user(username)
        users = db_fetcher.get_all_users()

        if users is None:
            return render_template("index.html", user_message=True)

        if not result:
            return render_template("admin.html", user_delete_error=True, users=users, order_information=order_information)

    return render_template("admin.html", user_delete_success=True, users=users, order_information=order_information)


if __name__ == "__main__":
    app.run(debug=True)
