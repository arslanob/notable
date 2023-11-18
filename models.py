"""SQLAlchemy for models"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Doctor(db.Model):
    """An individual doctor."""

    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True,)

    name = db.Column(db.String(50), nullable=False,)
    
    last_name = db.Column(db.String(50), nullable=False,)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)

    
    appointments = db.relationship('Appointment', backref="doctor", cascade="all, delete-orphan", order_by='Appointment.start_time')

    def __repr__(self):
        return f"<Doctor #{self.id}: {self.name}>"

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "last_name":self.last_name,
                "created_at": self.created_at.isoformat(),
                "appointments": [appointment.serialize() for appointment in self.appointments]

            }


class Appointment(db.Model):
    """An individual appointment."""

    __tablename__ = 'appointments'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(db.String(50), nullable=False,)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    
    start_time = db.Column(
        db.DateTime,
        nullable=False
    )

    description = db.Column(db.String(200))

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "description":self.description,
        }


