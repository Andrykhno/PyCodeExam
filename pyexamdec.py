from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Sample data
rooms = [
    {'id': 1, 'name': 'Sea View Apartment', 'location': 'Miami', 'price': 120, 'availability': True},
    {'id': 2, 'name': 'Mountain Cabin', 'location': 'Aspen', 'price': 150, 'availability': True},
    {'id': 3, 'name': 'City Center Hotel', 'location': 'New York', 'price': 200, 'availability': False},
]

booked_rooms = []  # List to store booked room IDs

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/staff')
def staff():
    # Placeholder for staff information
    return render_template('staff.html')
