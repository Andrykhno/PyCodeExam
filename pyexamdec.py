from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_users():
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_users(users):
    with open('users.csv', mode='w', newline='') as file:
        fieldnames = ['username', 'password', 'booked_rooms', 'first_name', 'last_name', 'phone_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

def load_rooms():
    with open('rooms.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return [
            {
                'id': room['id'],
                'name': room['name'],
                'location': room['location'],
                'price': int(room['price']),
                'availability': room['availability'] == 'True',
                'description': room['description'],
                'latitude': float(room['latitude']),
                'longitude': float(room['longitude']),
            }
            for room in reader
        ]

def save_rooms(rooms):
    with open('rooms.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'location', 'price', 'availability', 'description', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rooms)

users = load_users()
rooms = load_rooms()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
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

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/account', methods=['GET', 'POST'])
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
    booked_rooms = [room for room in rooms if str(room['id']) in current_user.get('booked_rooms', '').split(',')]
    return render_template('account.html', user=current_user, booked_rooms=booked_rooms, editing=editing)

@app.route('/cancel_booking/<int:room_id>', methods=['POST'])
def cancel_booking(room_id):
    if 'user' not in session:
        return render_template('error.html', message="You need to log in to cancel a booking.")
    
    current_user = next((user for user in users if user['username'] == session['user']), None)
    booked_rooms = current_user.get('booked_rooms', '').split(',')
    if str(room_id) in booked_rooms:
        booked_rooms.remove(str(room_id))
        current_user['booked_rooms'] = ','.join(booked_rooms)
        save_users(users)
        for room in rooms:
            if str(room['id']) == str(room_id):
                room['availability'] = True
                save_rooms(rooms)
                break
    
    return redirect(url_for('account'))

@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    if 'user' not in session:
        return render_template('error.html', message="You need to log in to book a room.")
    
    room = next((room for room in rooms if int(room['id']) == room_id), None)
    if not room:
        return "Room not found", 404

    if request.method == 'POST':
        check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%d')
        check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%d')
        total_days = (check_out - check_in).days
        amount = round((total_days * room['price']))
        
        current_user = next((user for user in usкers if user['username'] == session['user']), None)
        if current_user:
            current_user['booked_rooms'] = ','.join(current_user.get('booked_rooms', '').split(',') + [str(room_id)])
            save_users(users)
        room['availability'] = False
        save_rooms(rooms)
        return render_template('payment.html', room=room, amount=amount)
    
    amenities = ["Hot water", "Free Wi-Fi", "Heating", "Air Conditioning"]
    nearby_places = ["Metro Station - 200m", "Supermarket - 500m", "Park - 1km"]
    photos = [f"/static/images/room{room['id']}_1.jpg", f"/static/images/room{room['id']}_2.jpg"]

    return render_template(
        'room_details.html',
        room=room,
        amenities=amenities,
        nearby_places=nearby_places,
        photos=photos
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/map')
def map_view():
    return render_template('map.html', rooms=rooms)

if __name__ == '__main__':
    app.run(debug=True)