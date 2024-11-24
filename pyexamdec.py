from flask import Flask, render_template, redirect, url_for
import pandas as pd
import requests

app = Flask(__name__)

def get_coordinates(location):
    api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key=YOUR_API_KEY"
    response = requests.get(api_url)
    data = response.json()
    if data['results']:
        return data['results'][0]['geometry']['location']
    return None

def load_rooms():
    df = pd.read_csv('rooms.csv')
    return df.to_dict(orient='records')

rooms = load_rooms()

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

def save_rooms():
    df = pd.DataFrame(rooms)
    df.to_csv('rooms.csv', index=False)

booked_rooms = []

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/book/<int:room_id>')
def book_room(room_id):
    room = next((room for room in rooms if room['id'] == room_id), None)
    if room:
        if room['availability']:
            room['availability'] = False
            save_rooms()  # Обновляем CSV после изменения данных
            return render_template('booking_confirmation.html', room=room)
        else:
            return "Room is already booked", 400
    else:
        return "Room not found", 404

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/in_process')
def in_process():
    return render_template('in_process.html')

@app.route('/account')
def account():
    selected_rooms = [room for room in rooms if room['id'] in booked_rooms]
    return render_template('account.html', rooms=selected_rooms)

@app.route('/book/<int:room_id>')
def book_room(room_id):
    room = next((room for room in rooms if room['id'] == room_id), None)
    if room:
        return render_template('booking_confirmation.html', room=room)
    else:
        return "Room not found", 404

@app.route('/logo')
def logo_redirect():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)