from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
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
        fieldnames = ['username', 'password', 'booked_rooms']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

def load_transactions():
    with open('transactions.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_transactions(transactions):
    with open('transactions.csv', mode='w', newline='') as file:
        fieldnames = ['user_id', 'room_id', 'check_in', 'check_out', 'amount']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

users = load_users()
transactions = load_transactions()
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if any(user['username'] == form.username.data for user in users):
            return "Username already exists", 400
        new_user = {
            'username': form.username.data,
            'password': form.password.data,
            'booked_rooms': ''
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
            return "Invalid credentials", 400
    return render_template('login.html', form=form)

@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    room = next((room for room in rooms if int(room['id']) == room_id), None)
    if not room:
        return "Room not found", 404
    if request.method == 'POST':
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        amount = int(room['price']) * (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days
        transactions.append({'user_id': session['user'], 'room_id': room['id'], 'check_in': check_in, 'check_out': check_out, 'amount': amount})
        save_transactions(transactions)
        room['availability'] = False
        save_rooms(rooms)
        return render_template('payment.html', room=room, amount=amount)
    return render_template('booking_form.html', room=room)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)