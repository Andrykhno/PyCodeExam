from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)

def get_coordinates(location):
    api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key=YOUR_API_KEY"
    response = requests.get(api_url)
    data = response.json()
    if data['results']:
        return data['results'][0]['geometry']['location']
    return None

# Sample data
rooms = [
    {'id': 1, 'name': 'Sea View Apartment', 'location': 'Lodnon, NW5 3AN', 'price': 120, 'availability': True},
    {'id': 2, 'name': 'Mountain Cabin', 'location': 'Aspen', 'price': 150, 'availability': True},
    {'id': 3, 'name': 'City Center Hotel', 'location': 'New York', 'price': 200, 'availability': False},
    {'id': 4, 'name': 'Sea View Apartment', 'location': 'Lodnon, NW5 3AN', 'price': 120, 'availability': True},
    {'id': 5, 'name': 'Mountain Cabin', 'location': 'Aspen', 'price': 150, 'availability': True},
    {'id': 6, 'name': 'City Center Hotel', 'location': 'New York', 'price': 200, 'availability': False},
    {'id': 7, 'name': 'Sea View Apartment', 'location': 'Lodnon, NW5 3AN', 'price': 120, 'availability': True},
    {'id': 8, 'name': 'Mountain Cabin', 'location': 'Aspen', 'price': 150, 'availability': True},
    {'id': 9, 'name': 'City Center Hotel', 'location': 'New York', 'price': 200, 'availability': False},
    {'id': 10, 'name': 'Sea View Apartment', 'location': 'Lodnon, NW5 3AN', 'price': 120, 'availability': True},
    {'id': 11, 'name': 'Mountain Cabin', 'location': 'Aspen', 'price': 150, 'availability': True},
    {'id': 12, 'name': 'City Center Hotel', 'location': 'New York', 'price': 200, 'availability': False},
]

booked_rooms = []  # List to store booked room IDs

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/staff')
def staff():
    # Placeholder for staff information
    return render_template('staff.html')

@app.route('/in_process')
def in_process():
    # Placeholder for future content
    return render_template('in_process.html')

@app.route('/account')
def account():
    # Display rooms that the user has selected or paid for
    selected_rooms = [room for room in rooms if room['id'] in booked_rooms]
    return render_template('account.html', rooms=selected_rooms)

@app.route('/book/<int:room_id>')
def book_room(room_id):
    if room_id not in booked_rooms:
        booked_rooms.append(room_id)
    return redirect(url_for('account'))

@app.route('/book/<int:room_id>')
def book_room(room_id):
    room = next((room for room in rooms if room['id'] == room_id), None)
    if room:
        # Логика бронирования (например, добавить в список booked_rooms)
        return render_template('booking_confirmation.html', room=room)
    else:
        return "Room not found", 404

@app.route('/logo')
def logo_redirect():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)