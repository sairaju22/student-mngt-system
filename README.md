Student Management System

This repository contains a Flask-based web application for managing student data. It provides functionality for user registration, login, CRUD operations for students, and dynamic routing examples. The application uses MySQL as its database.

* Features

User Authentication:

User registration with hashed passwords for security.

User login with session management.

Logout functionality.

Student Management:

Add new students.

View the list of registered students.

Edit student details.

Delete student records with confirmation.

Dynamic Routing:

Examples of dynamic URL handling with string, integer, float, path, and UUID types.

About Us Page:

A static page providing information about the application.

Prerequisites

Python 3.x

Flask

MySQL

Required Python libraries (see Installation)

=>Installation

Clone the Repository:

git clone https://github.com/sairaju22/student-management-system.git
cd student-management-system

Set Up the Virtual Environment:

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Set Up the Database:

Create the database and tables using the provided SQL script in the SQL folder.

Update the database configuration in db_config within app.py if needed:

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'student'
}

Run the Application:

python app.py

Access the Application:
Open your browser and navigate to:

http://127.0.0.1:5000/

Folder Structure

student-management-system/
├── app.py               # Main application file
├── templates/           # HTML templates
│   ├── homepage.html
│   ├── login.html
│   ├── register.html
│   ├── student_register.html
│   ├── student_list.html
│   ├── student_update.html
│   ├── delete_confirmation.html
│   └── aboutus.html
├── static/              # Static files (CSS, JS, images)
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── sql/                 # SQL scripts for database setup
    └── create_tables.sql

Routes Overview

Method

Route

Description

GET/POST

/login

User login page.

GET/POST

/register

User registration page.

GET

/

Dashboard (requires login).

GET/POST

/std_reg

Register a new student.

GET

/student_list

View the list of students.

GET/POST

/edit/<int:id>

Edit student details by ID.

GET/POST

/delete/<int:id>

Delete a student by ID with confirmation.

GET

/aboutus

Static "About Us" page.

GET

/logout

Logout and clear the session.

Security Features

Passwords are securely hashed using werkzeug.security.

Session management ensures access control for protected routes.
