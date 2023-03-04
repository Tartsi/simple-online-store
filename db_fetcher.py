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

    sql = """
    SELECT p.id, p.name, p.description, p.price, p.amount, ROUND(AVG(r.rating), 1) as rating
    FROM products p
    LEFT JOIN reviews r ON p.id = r.product_id
    WHERE p.amount > 0
    GROUP BY p.id
    ORDER BY p.id
    """

    query_result = db.session.execute(sql).fetchall()

    if query_result is None:
        return None

    return query_result


def get_all_users():

    sql = """
    SELECT id, username FROM users;
    """

    query_result = db.session.execute(sql).fetchall()

    if len(query_result) == 0:
        return None

    return query_result


def get_product_name(id):

    sql = """
    SELECT name FROM products WHERE id = :id
    """

    query_result = db.session.execute(sql, {"id": id}).fetchone()

    if query_result is None:
        return None

    return query_result[0]


def get_product_amount(id):

    sql = """
    SELECT amount FROM products WHERE id = :id
    """

    query_result = db.session.execute(sql, {"id": id}).fetchone()

    if query_result is None:
        return None

    return query_result[0]


def get_product_price(id):

    sql = """
    SELECT price FROM products WHERE id = :id
    """

    query_result = db.session.execute(sql, {"id": id}).fetchone()

    if query_result is None:
        return None

    return query_result[0]


def search_products(name):

    name = name.title()

    sql = """
    SELECT p.id, p.name, p.description, p.price, p.amount, ROUND(AVG(r.rating), 1) as rating
    FROM products p
    LEFT JOIN reviews r on p.id = r.product_id
    WHERE p.amount > 0 AND p.name LIKE '%' || :name || '%'
    GROUP BY p.id
    ORDER BY p.id
    """

    query_result = db.session.execute(sql, {"name": name}).fetchall()

    if len(query_result) == 0:
        return None

    return query_result


def get_shopping_cart_content(id):

    sql = """
    SELECT added_products FROM shopping_cart WHERE id = :id
    """

    query_result = db.session.execute(sql, {"id": id}).fetchone()

    if len(query_result) == 0:
        return None

    return query_result[0]


def get_reviews(product_id):

    sql = """SELECT r.id, r.rating, r.description, to_char(r.date_created, 'DD-MM-YYYY') AS date_created,
    u.username, p.name,
    (SELECT ROUND(AVG(rating), 2) FROM reviews WHERE product_id = :product_id) AS avg_rating
    FROM reviews r 
    LEFT JOIN users u ON r.user_id = u.id
    JOIN products p ON r.product_id = p.id
    WHERE r.product_id = :product_id"""

    query_result = db.session.execute(
        sql, {"product_id": product_id}).fetchall()

    if len(query_result) == 0:
        return None

    return query_result


def check_review_adding(user_id, product_id) -> bool:
    """Check if user has 
    already added a review 
    for a specific product
    """

    sql = """
    SELECT EXISTS (
        SELECT 1
        FROM reviews
        WHERE user_id = :user_id
        AND product_id = :product_id
    )
    """

    query_result = db.session.execute(
        sql, {"user_id": user_id, "product_id": product_id})

    return query_result.fetchone()[0]


with app.app_context():
    # For testing purposes only
    pass
