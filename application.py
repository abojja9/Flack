import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from time import localtime, strftime

from form_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize flask-socketio
socketio = SocketIO(app)

# Creating Flack rooms
ROOMS = ["lunch", "movies", "games", "news"]

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

        # Flash messages
        flash('Registered Successfully. Please Login!', 'success')
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
    # if not current_user.is_authenticated:
    #     flash('Please Login!', 'danger')
    #     return redirect(url_for('login'))

    # Remember current user so that we can display him
    return render_template('chat.html', username=current_user.username,
    rooms=ROOMS)

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash('Logged out Successfully!', 'success')
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):
    print (data)

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + ' has joined the ' + data['room'] + " room."}, room=data['room'])


@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + ' has left the ' + data['room'] + " room."}, room=data['room'])

 

if __name__ == "__main__":
    socketio.run(app, debug=True)


