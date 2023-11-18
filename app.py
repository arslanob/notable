# Import flask
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from datetime import datetime
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import Config
from models import db, Doctor, Appointment
from resources import Appointments, AppointmentList,  Doctors, DoctorList
from example_data import add_example_data


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()
    add_example_data(db)  # Pass the db object


if __name__ == "__main__":
    app.run()


#Homepage for summary
@app.route('/', methods=["GET"])
def homepage():
    return render_template("homepage.html")


# Add resources and their routes
api.add_resource(AppointmentList, '/appointments')
api.add_resource(Appointments, '/appointments/<int:id>')
api.add_resource(DoctorList, '/doctors')
api.add_resource(Doctors, '/doctors/<int:id>')





