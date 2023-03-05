import json
from db import db
from werkzeug.security import generate_password_hash
from app import app
from db_fetcher import get_product_amount

"""
This module makes changes to the database
"""


def add_user(username, password, admin):

    try:

        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {
            "username": username, "password": generate_password_hash(password), "admin": admin})
        db.session.commit()
        return True
    except Exception as error:
        print(f"Error: {error}")
        db.session.rollback()
        return False


def add_new_product(name, description, price, amount):

    try:

        # adds consistency to items in database
        name = name.title()

        sql = """INSERT INTO products (name, description, price, amount)
        VALUES (:name, :description, :price, :amount)"""
        db.session.execute(
            sql, {"name": name, "description": description, "price": price, "amount": amount})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def add_new_review(user_id, product_id, rating, description):

    try:
        sql = """INSERT INTO reviews (user_id, product_id, rating, description)
        VALUES (:user_id, :product_id, :rating, :description)"""

        db.session.execute(sql,
                           {"user_id": user_id, "product_id": product_id,
                            "rating": rating, "description": description})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def add_new_shopping_cart(user_id, added_products):

    try:

        added_products = json.dumps(added_products)

        sql = """
        INSERT INTO shopping_cart (user_id, added_products)
        VALUES (:user_id, :added_products)
        RETURNING id
        """

        result = db.session.execute(
            sql, {"user_id": user_id, "added_products": added_products}).fetchone()[0]

        db.session.commit()
        return result
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def add_new_completed_order(user_id, cart_id, address, total_price):

    try:

        sql = """
        INSERT INTO completed_orders (user_id, cart_id, address, total_price)
        VALUES (:user_id, :cart_id, :address, :total_price)
        """

        db.session.execute(sql, {"user_id": user_id, "cart_id": cart_id,
                           "address": address, "total_price": total_price})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def increase_product_amount(name, amount):

    try:

        name = name.title()

        sql = "UPDATE products SET amount = amount + :amount WHERE name = :name"

        query_result = db.session.execute(
            sql, {"amount": amount, "name": name})

        if query_result.rowcount == 0:
            return False

        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def decrease_product_amount(name, amount):

    try:

        sql = """
        UPDATE products SET amount = amount - :amount WHERE name = :name
        RETURNING id
        """

        result = db.session.execute(
            sql, {"amount": amount, "name": name}).fetchone()[0]

        if get_product_amount(result) <= 0:
            delete_product(result)

        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def delete_product(id):

    try:

        sql = "DELETE FROM products WHERE id=:id"

        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


def delete_user(username):

    try:

        sql = "DELETE FROM users WHERE username=:username"

        db.session.execute(sql, {"username": username})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


with app.app_context():
    # For testing purposes only
    pass
