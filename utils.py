from db import db
from app import app
from werkzeug.security import check_password_hash


def login(username, password):

    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    query_result = db.session.execute(sql, {"username": username})

    user = query_result.fetchone()

    if user == None:
        return False

    if check_password_hash(user[1], password) == False:
        return False

    return (user[0], username, user[2])


with app.app_context():
    # For testing purposes only
    pass
