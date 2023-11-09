from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import db 
from flask_login import  UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd

auth = Blueprint('auth', __name__)
USERS_CSV = 'data_files/users_data.csv'

class User(UserMixin):
    def __init__(self, id, username, group, role):
        self.id = id
        self.username = username
        self.group = group
        self.role = role

def write_users_to_csv(users_data):
    users_data.to_csv(USERS_CSV, index=False)


def read_users_from_csv():
    try:
        users_data = pd.read_csv(USERS_CSV)
        # print("Users Data before 'id' conversion:")
        # print(users_data)
        users_data['id'] = users_data['id'].astype(int)
        return users_data
    except FileNotFoundError:
        # print('this os exept')
        return pd.DataFrame(columns=['id', 'username', 'password', 'group', 'role',])


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) == 0 or len(password) == 0:
            flash('Please enter username and password, try again.', category='error')
        else:
            users_data = read_users_from_csv()
            # print(users_data)
            user = users_data[users_data['username'] == username]
            # print(user['id'].values[0])
            # print(user['password'].values[0])
            if not user.empty and user['password'].values[0] == password:
                user_id = user['id'].values[0]
                username = user['username'].values[0]
                user_group = user['group'].values[0]
                user_role = user['role'].values[0]

                # print(user_id)
                login_user(User(int(user_id), username, user_group, user_role), remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username or password, try again.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        username = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        users_data = read_users_from_csv()
        if not users_data[users_data['username'] == username].empty:
            flash('Email already exists.', category='error')
        elif len(username) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user_id = len(users_data) + 1
            new_user_data = {'id': new_user_id, 'username': username, 'email': email, 'password': generate_password_hash(password1, method='sha256')}
            users_data = users_data.append(new_user_data, ignore_index=True)
            write_users_to_csv(users_data)
            flash('Account created!', category='success')
            login_user(User(new_user_id, username), remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)







# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             if check_password_hash(user.password, password):
#                 flash('Logged in successfully!', category='success')
#                 login_user(user, remember=True)
#                 return redirect(url_for('views.home'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

#     return render_template("login.html", user=current_user)


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=first_name, password=generate_password_hash(
#                 password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('views.home'))

#     return render_template("sign_up.html", user=current_user)











###################
# # CSV file to store user data (username, hashed password)
# USERS_CSV = 'users.csv'

# # Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Hash the password before storing it
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#         user_data = pd.DataFrame({'username': [username], 'password': [hashed_password]})

#         try:
#             existing_data = pd.read_csv(USERS_CSV)
#         except FileNotFoundError:
#             # If the file doesn't exist, create a new DataFrame
#             existing_data = pd.DataFrame(columns=['username', 'password'])

#         # Concatenate the new data with the existing data
#         new_data = pd.concat([existing_data, user_data], ignore_index=True)
#         # Save the updated data to the CSV file
#         new_data.to_csv(USERS_CSV, index=False)

#         flash('Registration successful!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         try:
#             users_data = pd.read_csv(USERS_CSV)
#         except FileNotFoundError:
#             flash('Login failed. No users found.', 'error')
#             return redirect(url_for('login'))

#         user_row = users_data[users_data['username'] == username]
#         if not user_row.empty:
#             hashed_password = user_row['password'].values[0]

#             if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
#                 session['user'] = username
#                 flash('Login successful!', 'success')
#                 return redirect(url_for('protected'))

#         flash('Login failed. Check your credentials.', 'error')
#     return render_template('login.html')

# # Protected route
# @app.route('/protected')
# def protected():
#     if 'user' in session:
#         return 'This is a protected route. You are logged in as ' + session['user']
#     return 'You need to log in to access this page.'

# # Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('login'))
