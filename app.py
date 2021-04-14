from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

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

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    record = User(username, password)
    db.session.add(record)
    db.session.commit()

    return jsonify("Congrats! User added.")


@app.route("/user/get", methods = ["GET"])
def get_user_all():
    all_users = db.session.query(User).all()
    return jsonify(many_user_schema.dump(all_users))

@app.route("/user/get/<id>", methods = ["GET"])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/get/<username>", methods = ["GET"])
def get_user_by_username(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))

@app.route("/multiple/user/add", methods = ["POST"])
def add_multiple_add():
    if request.content_type != "application/json":
        return jsonify("An error occured, your data must be sent as JSON")

    post_data = request.get_json()
    user = post_data.get('user')
    for user in user: 
        record = User(user["username"], user["password"])

@app.route("/user/delete/<id>", methods = ["DELETE"])
def delete_user(id):
    user_delete = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify ("User has been deleted")

@app.route("/appointment/add", methods = ["POST"])
def add_appointment():
    if request.content_type != "application/json":
        return("Error: Data must be sent as JSON")

    post_data = request.get_json() 
    text = post_data.get("text")
    date = post_data.get("date")
    month_id = post_data.get("month_id")
    hour = post_data.get("hour")
    minute = post_data.get("minute")

    record = Appointment(text, date, month_id, hour, minute)
    db.session.add(record)
    db.session.commit()

    return jsonify("Appointment has been added")

@app.route("/appointment/get", methods = ["GET"])
def get_appointment_all():
    all_appointments = db.session.query(Appointment).all()
    return jsonify(many_appointment_schema.dump(all_appointments))

@app.route("/appointment/get/<id>", methods = ["GET"])
def get_appointment_by_id(id):
    appointment = db.session.query(Appointment).filter(Appoinment.id == id).first()
    return jsonify(appointment_schema.dump(appointment))

@app.route("/appointment/update/<id>", methods = ["PUT"])
def update_appointment(id):
    appointment_update = db.session.query(Appointment).filter(Appointment.id == id).first()
    if appointment_update is None:
        return jsonify(f'ERROR: No appointment with ID:${id} exists.')

    put_data = request.get_json()
    new_text = put_data.get("text")
    new_date = put_data.get("date")
    new_month_id = put_data.get("month_id")
    new_hour = put_data.get("hour")
    new_minute = put_data.get("minute")

    if new_text == "" :
        return ("Text cannot be blank")
    if new_date == "" :
        return ("Date cannot be blank")
    if new_month_id == "" :
        return ("Month cannot be blank")
    if new_hour == "" :
        return ("Hour cannot be blank")
    if new_minute == "" :
        return ("Minute cannot be blank")

    Appointment.text = new_text
    Appointment.date = new_date
    Appointment.month_id = new_month_id
    Appointment.hour = new_hour
    Appointment.minute = new_minute
    db.session.commit()

    return jsonify("Appointment has been updated")

@app.route("/appointment/delete/<id>", methods = ["DELETE"])
def delete_appointment_by_id(id):
    appointment_delete = db.session.query(Appointment).filter(Appointment.id == id).first()
    db.session.delete(appointment)
    db.session.commit
    return jsonify("Appointment has been deleted")


if __name__ == "__main__":
    app.run(debug=True)