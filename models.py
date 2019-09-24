from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

# To let the flask_login about the user we need to pass UserMixin to the class User
# By adding UserMixin, the flask_login adds additional properties to the class User
# This doesn't effect the User class.
class User(UserMixin, db.Model):
    """ User database Model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)