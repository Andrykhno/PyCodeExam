# APP NAME
AndRent

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/Andrykhno/PyCodeExam

## Identification
- Andrii Prykhno
- P455514
- KICL IY499 Introduction to Programming

## Declaration of Own Work
I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

## Introduction
This code represents a simple implementation of the xx using the xx library. The game consists of xxyy

# APP NAME
AndRent

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/Andrykhno/PyCodeExam

## Identification
- **Name**: Andrii Prykhno
- **Student ID**: P455514
- **Course**: KICL IY499 Introduction to Programming

## Declaration of Own Work
I confirm that this assignment is my own work. Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

---

## Introduction
This project is a web-based room booking application built using the Flask framework. It allows users to register, log in, browse rooms, book accommodations, manage bookings, and interact with a map of room locations. The system ensures secure user sessions, persistent data storage in CSV files, and intuitive error handling for smooth user experiences.

---

## Installation
Follow these steps to set up and run the application:

1. Ensure you have Python installed on your system.
2. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/Andrykhno/PyCodeExam.git
   cd PyCodeExam
3.	Install the required dependencies from the requirements.txt file:
   ``bash
   pip install -r requirements.txt 
4.	Run the application using the command:
   python pyexamdec.py

## How to Play
Basic Usage

	•	Register: Create an account using your username and password.
	•	Log In: Access your account with your credentials.
	•	Browse Rooms: View all available rooms on the homepage.
	•	Filter and Sort: Filter rooms by location or price and sort by name or price.
	•	Book a Room: Select a room, specify check-in and check-out dates, and confirm the booking.
	•	Manage Account: View or cancel your bookings and update your personal information.

## Features
User Authentication
	•	Users can register and log in securely.
	•	Passwords are managed through secure input fields.

Room Browsing
	•	View a list of available rooms with details like name, location, price, and availability.
	•	Apply filters and sorting options to customize the search experience.

Room Booking
	•	Book a room by selecting a room and entering the desired dates.
	•	Automatic price calculation based on the duration of the stay.

Account Management
	•	View booked rooms, including check-in and check-out dates.
	•	Update personal information or cancel bookings.

Interactive Map
	•	Visualize room locations on an interactive map.

Error Handling
	•	Custom error messages for invalid actions (e.g., booking conflicts, invalid login attempts).

## Libraries Used
The following libraries are used in this project:

- **Flask**: A lightweight web framework used for creating the web application, managing routes, handling user sessions, and rendering templates.
- **Flask-WTF**: A Flask extension for creating secure forms with built-in CSRF protection.
- **WTForms**: A library used for defining form fields such as text inputs, password fields, and submit buttons, along with input validation.
- **csv**: A Python module for reading and writing user and room data to CSV files for persistent storage.
- **datetime**: A standard Python library for handling and formatting dates and times, such as managing check-in and check-out dates.

## Project Structure
The project is organized into the following directories and files:

### Root Directory
- **pyexamdec.py**: The main Python script that serves as the entry point for the application.
- **README.md**: Documentation for the project, including setup instructions and feature descriptions.
- **users.csv**: Stores user account information, including credentials and bookings.
- **rooms.csv**: Contains data about available rooms, including location, price, and availability.
- **transactions.csv**: Logs transaction details related to room bookings and payments.
- **auto_commit.sh**: A shell script for automating version control operations (e.g., commits).
- **tempCodeRunnerFile.sh**: A temporary file used during code execution for debugging purposes.
- **venv/**: A virtual environment directory containing installed dependencies for the project.

### `templates/` Directory
Contains HTML templates for rendering different pages of the web application:
- **base.html**: The base layout used as a foundation for all other templates.
- **index.html**: The homepage displaying available rooms with filtering and sorting options.
- **account.html**: Displays the user's account information and their booked rooms.
- **account_details.html**: Detailed view of user account settings and information.
- **account_edit.html**: A page for editing user account details.
- **register.html**: Registration form for creating a new user account.
- **login.html**: Login form for existing users.
- **room_details.html**: Displays detailed information about a specific room.
- **booking_form.html**: A form for selecting check-in and check-out dates for booking a room.
- **map.html**: An interactive map showing the locations of all available rooms.
- **staff.html**: A template for staff-related functions (e.g., administrative operations).
- **in_process.html**: A placeholder template for processing user actions or requests.
- **error.html**: A generic error page displayed for invalid actions or missing resources.
- **payment.html**: Handles payment-related actions and displays payment confirmation.

### `static/` Directory
Holds static files used in the application:
- **style.css**: The main CSS file for styling the web application.
- **images/**: A directory for storing images used throughout the website.