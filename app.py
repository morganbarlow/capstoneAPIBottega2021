from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS
import os

app = Flask(__name__)

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS(app)

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    def __init__ (self, username, password):
        self.username = username
        self.password = password

class UserSchema (ma.Schema):
    class Meta:
        feilds = ("id", "username", "password")

user_schema = UserSchema()
many_user_schema = UserSchema(many=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable= False)
    date = db.Column(db.Integer, nullable=False)
    month_id = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)

    def __init__ (self, text, date, month_id, hour, minute):
        self.text = text
        self.date = date
        self.month_id = month_id
        self.hour = hour
        self.minute = minute

class AppointmentSchema(ma.Schema):
    class Meta: 
        feilds = ("id", "text", "date", "month_id", "hour", "minute")


appointment_schema = AppointmentSchema()
many_appointment_schema = AppointmentSchema(many=True)

@app.route("/user/add", methods = ["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("An error occured, your data must be sent as JSON")

        post_user = request.get_json()
        username = post_user.get("username")
        password = post_user.get("password")

        record = User(username, password)
        db.session.add(record)
        db.session.commit()

        return jsonify("Congrats! User added.")

@app.route("/user/get", methods = ["GET"])
def get_user_all():
    user = db.session.query(User).all()
    return jsonify(many_user_schema.dump(all))

@app.route("/user/get/<id>", methods = ["GET"])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dumb(user))

@app.route("/user/get/<username>", methods = ["GET"])
def get_user_by_username(month):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dumb(user))

@app.route("/multiple/user/add", methods = ["POST"])
def add_multiple_add():
    if request.content_type != "application/json":
        return jsonify("An error occured, your data must be sent as JSON")

        post_user = request.get_json()
        user = post_user.get('user')
        for user in user: 
            record = User(user["username"], user["password"]) 
