from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, reqparse
from models import db, Doctor, Appointment
from datetime import datetime

class Appointments(Resource):
    #Get a single appointment
    def get(self, id):
        if id is None:
            return {'message': 'Appointment ID is required'}, 400

        appointment = Appointment.query.get(id)

        if appointment is None:
            return {'message': 'Appointment not found'}, 404

        return  (appointment.serialize()), 200
  
    #delete an appointment
    def delete(self, id):
        if id is None:
            return {'message': 'Appointment ID is required'}, 400
        
        appointment = Appointment.query.get(id)

        if appointment is None:
            return {'message': 'Appointment not found'}, 404
        
        db.session.delete(appointment)
        db.session.commit()

        return {'message': 'Appointment deleted successfully'}, 200

class AppointmentList(Resource):
    #Get All appointments
    def get(self):
        appointments = Appointment.query.all()
        return jsonify([appointment.serialize() for appointment in appointments])

    # Create a new appointment
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('doctor_id', type=int, required=True, help="Doctor ID cannot be blank!")
        parser.add_argument('start_time', required=True, help="Start time is required")
        parser.add_argument('description')
        args = parser.parse_args()
        
        # Check and parse start_time
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Start time is in an incorrect format. Please use YYYY-MM-DD HH:MM:SS'}, 400

        if start_time.minute not in [0, 15, 30, 45]:
            return {'message': 'Start time must be at a quarter-hour increment (00, 15, 30, 45 minutes past the hour)'}, 400

        #check if doctor exists
        doctor = Doctor.query.get(args['doctor_id'])
        if doctor is None:
            return {'message': 'Doctor not found'}, 404 
        
        #check if doctor is available
        if not is_doctor_available(args['doctor_id'], start_time):
            return {'message': 'Doctor is not available at this time.'}, 400

        #create an appointment
        new_appointment = Appointment(name=args['name'], doctor_id=args['doctor_id'], start_time=start_time, description=args['description'])
        db.session.add(new_appointment)
        db.session.commit()

        return {'message': 'New appointment added successfully', "new_appointment":new_appointment.serialize()}, 201

            

class Doctors(Resource):
    #Get a single doctor.
    def get(self, id):
        if id is None:
            return {'message': 'Doctor ID is required'}, 400
        
        doctor = Doctor.query.get(id)

        if doctor is None:
            return {'message': 'Doctor not found'}, 404

        return (doctor.serialize()), 200

    
    #Delete a doctor.
    def delete(self, id):
        if id is None:
            return {'message': 'Doctor ID is required'}, 400

        doctor = Doctor.query.get(id)

        if doctor is None:
            return {'message': 'Doctor not found'}, 404

        db.session.delete(doctor)
        db.session.commit()

        return {'message': 'Doctor deleted successfully', "Deleted_doctor":doctor.serialize()}, 200


class DoctorList(Resource):
    #Get All Doctors
    def get(self):
        doctors = Doctor.query.all()
        return jsonify([doctor.serialize() for doctor in doctors])

    # Create a new doctor
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('last_name', type=str, required=True, help="Last Name cannot be blank!")
        args = parser.parse_args()

        new_doctor = Doctor(name=args['name'], last_name=args['last_name'])

        db.session.add(new_doctor)
        db.session.commit()
        return {'message': 'Doctor added successfully', "new_doctor":new_doctor.serialize()}, 201




# Helper function to check doctor's availability
def is_doctor_available(doctor_id, start_time):
    #Maybe we can check if start time is within office hours of that doctor here?

    # Check for overlapping appointments
    overlapping_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.start_time == start_time,
    ).all()

    return len(overlapping_appointments) < 3