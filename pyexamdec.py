from flask import Flask, render_template, redirect, url_for, request, session, flash  # Imports modules for creating a web application and handling routes, templates, sessions, and user input.
from flask_wtf import FlaskForm  # Importing FlaskForm to create secure forms with CSRF protection.
from wtforms import StringField, PasswordField, SubmitField  # Imports fields for user input such as text fields and password fields.
from wtforms.validators import DataRequired, EqualTo  # Provides validators to ensure fields are not empty and passwords match.
import csv  # Used for reading and writing data to CSV files for persistence.
from datetime import datetime  # Enables manipulation and formatting of date and time objects.

app = Flask(__name__)  # Initializes a Flask application instance for routing and handling requests.
app.secret_key = 'supersecretkey'  # Sets a secret key to enable secure sessions and CSRF protection.

def load_users():  # Reads user data from a CSV file and returns it as a list of dictionaries.
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_users(users):  # Writes updated user data to the 'users.csv' file, ensuring all users are saved.
    try:
        existing_users = load_users()
    except FileNotFoundError:
        existing_users = []
    existing_users_dict = {user['username']: user for user in existing_users}
    for user in users:
        existing_users_dict[user['username']] = user
    all_fields = set()
    for user in existing_users_dict.values():
        all_fields.update(user.keys())
    all_fields = list(all_fields)
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(existing_users_dict.values())

def load_rooms():  # Reads room data from a CSV file, converts fields to appropriate types, and returns a list of room dictionaries.
    with open('rooms.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return [
            {
                'id': int(row['id']),
                'name': row['name'],
                'location': row['location'],
                'price': int(row['price']),
                'availability': row['availability'] == 'True',
                'description': row.get('description', 'No description available'),
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude'])
            }
            for row in reader
        ]

def save_rooms(rooms):  # Writes room data to the 'rooms.csv' file, including all necessary fields for room information.
    fieldnames = ['id', 'name', 'location', 'price', 'availability', 'description', 'latitude', 'longitude']
    with open('rooms.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{key: room[key] for key in fieldnames} for room in rooms])

users = load_users()  # Loads all users from the 'users.csv' file into a global variable.
rooms = load_rooms()  # Loads all rooms from the 'rooms.csv' file into a global variable.

class RegistrationForm(FlaskForm):  # Defines a registration form with fields for username, password, and password confirmation.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):  # Defines a login form with fields for username and password.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')  # Displays the homepage where users can filter, sort, and view available rooms.
def index():
    filters = request.args
    filtered_rooms = rooms
    if 'location' in filters and filters['location']:
        filtered_rooms = [room for room in rooms if filters['location'].lower() in room['location'].lower()]
    if 'price' in filters and filters['price']:
        try:
            price = int(filters['price'])
            filtered_rooms = [room for room in filtered_rooms if room['price'] <= price]
        except ValueError:
            pass
    if 'sort' in filters and filters['sort'] == 'alphabetical':
        filtered_rooms = sorted(filtered_rooms, key=lambda x: x['name'])
    elif 'sort' in filters and filters['sort'] == 'price':
        filtered_rooms = sorted(filtered_rooms, key=lambda x: x['price'])
    return render_template('index.html', rooms=filtered_rooms)

@app.route('/register', methods=['GET', 'POST'])  # Handles user registration, validates inputs, and saves new users to the database.
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if any(user['username'] == form.username.data for user in users):
            return "Username already exists", 400
        new_user = {
            'username': form.username.data,
            'password': form.password.data,
            'booked_rooms': '',
            'first_name': '',
            'last_name': '',
            'phone_number': ''
        }
        users.append(new_user)
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])  # Manages user login, authenticates credentials, and starts a session.
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users if user['username'] == form.username.data and user['password'] == form.password.data), None)
        if user:
            session['user'] = user['username']
            return redirect(url_for('index'))
        else:
            return render_template('error.html', message="Invalid username or password.")
    return render_template('login.html', form=form)

@app.route('/account', methods=['GET', 'POST'])  # Allows logged-in users to view and edit their account information and bookings.
def account():
    if 'user' not in session:
        return render_template('error.html', message="You need to log in to access your account.")
    current_user = next((user for user in users if user['username'] == session['user']), None)
    if not current_user:
        return render_template('error.html', message="Account not found.")
    if request.method == 'POST':
        current_user['first_name'] = request.form.get('first_name', current_user.get('first_name', ''))
        current_user['last_name'] = request.form.get('last_name', current_user.get('last_name', ''))
        current_user['phone_number'] = request.form.get('phone_number', current_user.get('phone_number', ''))
        save_users(users)
        return redirect(url_for('account'))
    editing = request.args.get('edit') == 'True'
    booked_rooms = []
    for room in rooms:
        if str(room['id']) in current_user.get('booked_rooms', '').split(','):
            check_in = current_user.get(f'check_in_{room["id"]}')
            check_out = current_user.get(f'check_out_{room["id"]}')
            if check_in and check_out:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
                days = (check_out_date - check_in_date).days
                total_price = days * room['price']
                room['total_price'] = total_price
                room['check_in'] = check_in
                room['check_out'] = check_out
            else:
                room['total_price'] = 0
            booked_rooms.append(room)
    return render_template('account.html', user=current_user, booked_rooms=booked_rooms, editing=editing)

@app.route('/cancel_booking/<int:room_id>', methods=['POST'])  # Allows logged-in users to cancel bookings and updates the availability of rooms.
def cancel_booking(room_id):
    if 'user' not in session:
        return render_template('error.html', message="You need to log in to cancel a booking.")
    current_user = next((user for user in users if user['username'] == session['user']), None)
    if not current_user:
        return render_template('error.html', message="Account not found.")
    booked_rooms = current_user.get('booked_rooms', '').split(',')
    if str(room_id) in booked_rooms:
        booked_rooms.remove(str(room_id))
        current_user['booked_rooms'] = ','.join(booked_rooms)
        current_user.pop(f'check_in_{room_id}', None)
        current_user.pop(f'check_out_{room_id}', None)
        save_users(users)
        for room in rooms:
            if int(room['id']) == room_id:
                room['availability'] = True
                break
        save_rooms(rooms)
    flash("Booking successfully canceled!", "success")
    return redirect(url_for('account'))

@app.route('/book/<int:room_id>', methods=['GET', 'POST']) # Handles room booking by validating dates and updating user and room records.
def book_room(room_id):
    if 'user' not in session:
        return render_template('error.html', message="You need to log in to book a room.")

    room = next((room for room in rooms if int(room['id']) == room_id), None)
    if not room:
        return "Room not found", 404

    if request.method == 'POST':
        try:
            check_in = request.form['check_in']
            check_out = request.form['check_out']

            if not check_in or not check_out:
                return render_template('room_details.html', room=room, error="Please provide both check-in and check-out dates.")

            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')

            if check_out_date <= check_in_date:
                return render_template('room_details.html', room=room, error="Check-out date must be after check-in date.")

            total_days = (check_out_date - check_in_date).days
            total_price = total_days * room['price']

            current_user = next((user for user in users if user['username'] == session['user']), None)
            if current_user:
                booked_rooms = current_user.get('booked_rooms', '').split(',')
                if str(room_id) not in booked_rooms:
                    booked_rooms.append(str(room_id))
                current_user['booked_rooms'] = ','.join(booked_rooms)
                current_user[f'check_in_{room_id}'] = check_in
                current_user[f'check_out_{room_id}'] = check_out
                save_users(users)

            room['availability'] = False
            save_rooms(rooms)

            flash(f"Booking confirmed! Total Price: £{total_price}", "success")
            return redirect(url_for('index'))

        except ValueError:
            return render_template('room_details.html', room=room, error="Invalid date format. Use YYYY-MM-DD.")
        except Exception as e:
            return render_template('error.html', message=f"An unexpected error occurred: {e}")

    map_data = {
        "latitude": room.get('latitude'),
        "longitude": room.get('longitude'),
        "show_map": room.get('latitude') is not None and room.get('longitude') is not None
    }

    return render_template('room_details.html', room=room, map_data=map_data)

# @app.route('/logout') defines the logout functionality, which removes the current user from the session and redirects them to the homepage.
@app.route('/logout')
def logout():
    session.pop('user', None)  # Removes the 'user' key from the session, effectively logging the user out.
    return redirect(url_for('index'))  # Redirects the user to the homepage.

# @app.route('/map') serves the map view, displaying all rooms with location data on an interactive map.
@app.route('/map')
def map_view():
    return render_template('map.html', rooms=rooms)  # Renders the map.html template with the list of rooms.

# The entry point of the Flask application, which runs the app in debug mode for development purposes.
if __name__ == '__main__':
    app.run(debug=True)  # Starts the Flask development server with debug mode enabled.