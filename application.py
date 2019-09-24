import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from form_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://rcrlddecvxotif:fe0adb891142e2d956e6f6209c2472c045f17ffb5e15aef4ee2c20ec525885dd@ec2-174-129-231-116.compute-1.amazonaws.com:5432/da364vd80pj157'
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data


        # Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted to DB"

    return render_template('index.html', form=reg_form)
