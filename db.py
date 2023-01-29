from flask_sqlalchemy import SQLAlchemy
from app import app
from os import getenv
from dotenv import load_dotenv
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
