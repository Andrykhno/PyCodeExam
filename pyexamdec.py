from flask import Flask, render_template, redirect, url_for
import csv

app = Flask(__name__)

def load_rooms():
    with open('rooms.csv', mode='r') as file:
        reader = csv.DictReader(file)
        rooms = []
        for row in reader:
            row['availability'] = row['availability'] == 'True'
            rooms.append(row)
        return rooms

def save_rooms(rooms):
    with open('rooms.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'location', 'price', 'availability', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for room in rooms:
            room['availability'] = 'True' if room['availability'] else 'False'
            writer.writerow(room)

rooms = load_rooms()
booked_rooms = []

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/book/<int:room_id>')
def book_room(room_id):
    room = next((room for room in rooms if int(room['id']) == room_id), None)
    if room:
        if room['availability']:  # Проверяем булевое значение
            room['availability'] = False  # Меняем на False (занято)
            booked_rooms.append(int(room['id']))  # Добавляем в список забронированных
            save_rooms(rooms)  # Сохраняем изменения в CSV
            return render_template('booking_confirmation.html', room=room)
        else:
            return "Room is already booked", 400
    else:
        return "Room not found", 404

@app.route('/account')
def account():
    selected_rooms = [room for room in rooms if int(room['id']) in booked_rooms]
    return render_template('account.html', rooms=selected_rooms)

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/in_process')
def in_process():
    return render_template('in_process.html')

@app.route('/logo')
def logo_redirect():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)