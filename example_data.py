from models import Doctor, Appointment
from datetime import datetime, time

# Function to add example data when database is started. If there are no data, it adds 2 example datapoints.assert
def add_example_data(db):

    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    if not doctors and not appointments:
        print('NO DOCTOR AND APPOINTMENT IN THE SYSTEM SO ADDING EXAMPLE DATA -2 doctors,  2 appointments')

        # Create example doctors
        doctor1 = Doctor(name="Dr. Omer", last_name="Arslan")
        doctor2 = Doctor(name="Dr. Mike", last_name="Turner" )

        db.session.add(doctor1)
        db.session.add(doctor2)
        db.session.commit() 

        # Create example appointments
        appointment1 = Appointment(
            doctor_id=doctor1.id,
            name = "Sarah Connor",
            start_time=datetime(2023, 11, 18, 10, 0),
            description="Regular Checkup"
        )

        appointment2 = Appointment(
            doctor_id=doctor2.id,
            name = "Marry Jane",
            start_time=datetime(2023, 11, 18, 14, 0),
            description="Consultation"
        )

        db.session.add(appointment1)
        db.session.add(appointment2)

        # Commit the changes to the database
        db.session.commit()
