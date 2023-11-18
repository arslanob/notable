## Getting Started

To get this application running, make sure you do the following in the Terminal: 
PS:You need to create a postgresql database named 'notable'

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb notable`
5. `flask run`


Welcome to our appointment management system backend. Below are the available API routes:

Get Routes ✓
GET /appointments: List all appointments.
GET /appointments/:id: Fetch details of a specific appointment.
GET /doctors: Display all doctors.
GET /doctors/:id: Get details about a specific doctor and their appointments.

Post Routes ✓
POST /doctors/: Add new doctors to the system. body={"name":"Dr. Emily", last_name="Sanders" }
POST /appointments/: Create new appointments. body={name="Jane Doe", "description":"General Checkup", "start_time":"2023-10-02 9:00:00", "doctor_id":"1"}

Delete Routes ✓
DELETE /doctors/:id: Remove a doctor from the system.
DELETE /appointments/:id: Cancel or remove appointments.