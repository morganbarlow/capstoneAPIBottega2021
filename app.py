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
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
many_user_schema = UserSchema(many=True)


class Month(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    start_day = db.Column(db.Integer, nullable=False)
    days_in_month = db.Column(db.Integer, nullable=False)
    days_in_previous_month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False),
    hour = db.Column(db.Integer, nullable=False),
    minute = db.Column(db.Integer, nullable=False)

    def __init__(self,name,start_day,days_in_month,days_in_previous_month,year,hour,minute):
        self.name = name
        self.start_day = start_day
        self.days_in_month = days_in_month
        self.days_in_previous_month = days_in_previous_month
        self.year = year
        self.hour = hour
        self.minute = minute


class MonthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'start_day', 'days_in_month', 'days_in_previous_month', 'year', 'hour', 'minute')

month_schema = MonthSchema ()
multiple_month_schema = MonthSchema(many=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    month_id =db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable= False)
    minute = db.Column(db.Integer, nullable=False)

    def __init__(self,text,date,month_id):
        self.text = text
        self.date = date
        self.month_id = month_id
        self.hour = hour
        self.minute = minute

class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ('id','text','date', 'month_id', 'hour', 'minute')

appointment_schema = AppointmentSchema()
multiple_appointment_schema = AppointmentSchema(many=True)


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


@app.route("/month/add", methods=["POST"])
def add_month():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    name = post_data.get("name")
    start_day = post_data.get("start_day")
    days_in_month = post_data.get("days_in_month")
    days_in_previous_month = post_data.get("days_in_previous_month")
    year = post_data.get("year")
    hour = post_data.get("hour")
    minute = post_data.get("minute")

    record = Month(name,start_day,days_in_month,days_in_previous_month, year, hour, minute)
    db.session.add(record)
    db.session.commit()

    return jsonify("Month added")

@app.route("/month/add/multiple", methods=["POST"])
def add_multiple_months():
    if request.content_type != "application/json":
        return("Error: Data isn't JSON")

    post_data = request.get_json()
    data = post_data.get('data')
    for month in data:
        record = Month(month["name"], month["start_day"], month["days_in_month"], month["days_in_previous_month"], month["year"], month["hour"], month["minute"])
        db.session.add(record)

    db.session.commit()

    return jsonify("All months have been added")


@app.route("/month/get", methods=["GET"])
def get_all_months():
    all_months = db.session.query(Month).all()
    return jsonify(multiple_month_schema.dump(all_months))


@app.route("/month/get/<month_name>/<month_year>", methods=["GET"])
def get_one_month(month_name, month_year):
    month = bd.session.query(Month).filter(Month.name == month_name).filter(Month.year == month_year).first()
    return jsonify(month_schema.dump(month))


@app.route("/appointment/add", methods=["POST"])
def add_appointment():
    if request.content_type != "application/json":
        return("Error: Data isn't JSON")

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


@app.route("/appointment/get", methods=["GET"])
def get_all_appointments():
    all_appointments = db.session.query(Appointment).all()
    return jsonify(multiple_appointment_schema.dump(all_appointments))

@app.route("/appointment/get/<month_id>/<date>", methods=["GET"])
def get_one_appointment(month_id, date):
    appointment = db.session.query(Appointment).filter(Appointment.month_id == month_id).filter(Appointment.date == date).first()
    return jsonify(appointment_schema.dump(appointment))

@app.route("/appointment/update/<id>", methods=["PUT"])
def update_appointment(id):
    appointment_update = db.session.query(Appointment).filter(Appointment.id == id).first()
    if appointment_update is None:
        return jsonify(f'Error: No appointment with id-{id} to update')
    
    put_data = request.get_json()
    new_text = put_data.get("text")

    if new_text == "":
        return jsonify("Error: Text can't be blank")

    Appointment.text = new_text
    db.session.commit()

    return jsonify("Appointment updated")
    

@app.route("/appointment/delete/<id>", methods=["DELETE"])
def delete_appointment(id):
    appointment_delete = db.session.query(Appointment).filter(Appointment.id == id).first()
    db.session.delete(appointment)
    db.session.commit()

    return jsonify("Appointment has been deleted.")


if __name__ == "__main__":
    app.run(debug=True)