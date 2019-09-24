import os

from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from form_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://rcrlddecvxotif:fe0adb891142e2d956e6f6209c2472c045f17ffb5e15aef4ee2c20ec525885dd@ec2-174-129-231-116.compute-1.amazonaws.com:5432/da364vd80pj157'
db = SQLAlchemy(app)

# Configure Flask Login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=["GET", "POST"])
def index():

    reg_form = RegistrationForm()

    # Update the DB if the registraion details are valid.
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash the password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Route for login"""

    login_form = LoginForm()

    # check if the login is valid
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    
    return render_template('login.html', form=login_form)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not current_user.is_authenticated:
        return "Plesase Login"
    return "Chat with me"


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return "User Logged out!"







if __name__ == "__main__":
    app.run(debug=True)


