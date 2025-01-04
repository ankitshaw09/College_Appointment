# College Appointment Management System

## Overview
The College Appointment Management System is a Django-based application designed to streamline appointment scheduling between students and professors. This project includes APIs for booking, canceling, and viewing appointments, ensuring efficient communication and management of time slots.

---

## Features

- **Student Functionality:**
  - Book appointments with professors.
  - Check pending or completed appointments.

- **Professor Functionality:**
  - View all appointments.
  - Cancel appointments when necessary.

- **Admin Functionality:**
  - Manage users, appointments, and time slots.

---

## Requirements

- **Python:** 3.10+
- **Django:** 5.1.3
- **Django REST Framework:** 3.x
- **Database:** SQLite (default), can be switched to PostgreSQL/MySQL

---

## Installation

### Clone the Repository
```bash
$ git clone https://github.com/your-repo/college-appointment.git
$ cd college-appointment
```

### Set Up Virtual Environment
```bash
$ python -m venv venv
$ source venv/bin/activate   # For Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
$ pip install -r requirements.txt
```

### Apply Migrations
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create Superuser
```bash
$ python manage.py createsuperuser
```

### Run the Server
```bash
$ python manage.py runserver
```

---

## API Endpoints

### **Authentication**
##  Professors 
- **register:** `apis/professor/register/`[POST]
```bash
{
    "college_id":
    "name": 
    "department": 
    "email": 
    "user_type": 
    "password1": 
    "password2": 
}
``` 

- **Login:** `/apis/professor/login/` [POST]
``` bash
{
    "college_id": 
    "password": 
}
```
- **Logout:** `/api/auth/logout/`   * soon

- **Create Time Slot:** `apis/professor/timeslot/create/` [POST]
- **Cancel Appointment:** `/api/professor/cancel_appointment/` (POST)
- **View Appointments:** `/api/professor/view_appointments/` (GET)

### **Student Endpoints**

- **register:** `apis/student/register/`[POST]
```bash
{
    "college_id":
    "name": 
    "department": 
    "email": 
    "user_type": 
    "password1": 
    "password2": 
}
``` 

- **Login:** `/apis/student/login/` [POST]
``` bash
{
    "college_id": 
    "password": 
}
```
- **Logout:** `/api/auth/logout/`   * soon

- **Book Appointment:** `/api/student/book_appointment/` (POST)
- **Check Appointments:** `/api/student/check_appointments/` (GET)
- **Cancel Appointment:** `/api/professor/cancel_appointment/` (POST)

### **Admin Endpoints**
- Manage users, time slots, and appointments via the Django Admin Panel.

---


## Usage

### Booking an Appointment (Student)
Send a POST request to `/api/student/book_appointment/` with the following payload:
```json
{
  "time_slot_id": "T001"
}
```

### Canceling an Appointment (Professor)
Send a POST request to `/api/professor/cancel_appointment/` with the following payload:
```json
{
  "appointment_id": "A001"
}
```

### Checking Appointments (Student)
Send a GET request to `/api/student/check_appointments/`.

#### Example Response for No Appointments:
```json
{
  "message": "You have no pending appointments."
}

```
{![alt text](<Screenshot 2025-01-04 105736.png>) ![alt text](<Screenshot 2025-01-04 105714.png>) ![alt text](<Screenshot 2025-01-04 105637.png>) ![alt text](<Screenshot 2025-01-04 105623.png>) ![alt text](<Screenshot 2025-01-04 105607.png>) ![alt text](<Screenshot 2025-01-04 105326.png>) ![alt text](<Screenshot 2025-01-04 105304.png>) ![alt text](<Screenshot 2025-01-04 105245.png>) ![alt text](<Screenshot 2025-01-04 105103.png>)}
---

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

---

 
