from db import db
from app import app
from werkzeug.security import check_password_hash

"""
This module fetches information from database
"""


def login(username, password):

    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    query_result = db.session.execute(sql, {"username": username})

    user = query_result.fetchone()

    if user is None:
        return False

    if check_password_hash(user[1], password) is False:
        return False

    return (user[0], username, user[2])


def get_all_products():

    sql = "SELECT id, name, description, price, amount FROM products"
    query_result = db.session.execute(sql).fetchall()

    if len(query_result) == 0:
        return None

    return query_result


def search_products(name):

    sql = "SELECT id, name, description, price, amount FROM products WHERE name LIKE '%' || :name || '%'"

    query_result = db.session.execute(sql, {"name": name}).fetchall()

    if len(query_result) == 0:
        return None

    return query_result


with app.app_context():
    # For testing purposes only
    pass
