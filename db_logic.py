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
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return False


with app.app_context():
    # For testing purposes only
    pass
