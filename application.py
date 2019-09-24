import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from form_fields import *

app = Flask(__name__)
app.secret_key = 'replace later'
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Great Success!"
    return render_template('index.html', form=reg_form)
