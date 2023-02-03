from db import db
from werkzeug.security import generate_password_hash
from app import app


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

        sql = "INSERT INTO products (name, description, price, amount) VALUES (:name, :description, :price, :amount)"

        db.session.execute(
            sql, {"name": name, "description": description, "price": price, "amount": amount})
        db.session.commit()
        return True
    except Exception as error:

        print(f"Error: {error}")
        db.session.rollback()
        return False


with app.app_context():
    # For testing purposes only
    pass
