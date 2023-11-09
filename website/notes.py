from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Service, Platform, Credit, agent
from datetime import datetime
from . import db
from sqlalchemy import asc
import pandas as pd
import os
import uuid


notes = Blueprint("notes", __name__)

TODO_CSV = 'data_files/todo_data.csv'



# 



# TODO_CSV = "data_files/todo.csv"
# @notes.route('/note', methods=['GET', 'POST'])
# @login_required
# def add_note():
#     notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.on_progress.desc(), Note.date_done.desc(), Note.date_created.desc()).all()
#     if request.method == 'POST': 
#         note = request.form.get('data')

#         if len(note) < 1:
#             flash('Note is too short!', category='error') 
#         else:
#             new_note = Note(data=note, user_id=current_user.id)  
#             db.session.add(new_note) 
#             db.session.commit()
#             flash('Note added!', category='success')

#         return redirect(url_for("notes.add_note"))

#     return render_template("note.html", user=current_user, notes=notes)

@notes.route("/delete-task/<id>", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    note = Note.query.filter_by(id=id).first()

    if not note:
        flash("note does not exist.", category='error')
    elif current_user.id != note.user_id:
        flash('You do not have permission to delete this service.', category='error')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('note deleted.', category='success')

    return redirect(url_for('notes.add_note'))


# @notes.route("/edit-note/<id>", methods=['GET', 'POST'])
# @login_required
# def edit_note(id):
#     note = Note.query.filter_by(id=id).first()
#     if request.method == 'POST':
#         note.data = request.form.get('data')

#         try:
#             db.session.commit()
#             flash('note edited!', category='success')
#             return redirect(url_for('notes.add_note'))

#         except:
#             return "there is a problem"
#     else:

#         return render_template('edit_note.html', user=current_user, note=note)
    
# @notes.route("/update-task-status/<int:row_number>", methods=['POST'])
# @login_required
# def update_task_status(row_number):
#     existing_data = pd.read_csv(TODO_CSV)

#     if 0 <= row_number < len(existing_data):
#         # Toggle the 'on_progress' value
#         existing_data.at[row_number, 'on_progress'] = not existing_data.at[row_number, 'on_progress']
#         existing_data.at[row_number, 'date_done'] = datetime.utcnow()

#         # Save the updated data back to the CSV file
#         existing_data.to_csv(TODO_CSV, index=False)

#     return redirect(url_for('notes.add_task'))


# def create_row(data_file, template_name, success_message, row_data_fields):
#     platform_names = get_platform_names()
#     row_data = {}
    
#     if request.method == 'POST':
#         has_error = False
#         row_data = {}  
#         for field in row_data_fields:
#                 row_data[field] = request.form.get(field)
#                 if field == "task" and len(row_data[field]) == 0:
#                     flash("Task field can't be empty!", category='error')
#                     has_error = True
#                 elif field == "platform_name" and len(row_data[field]) == 0:
#                     flash("Platform name  field can't be empty!", category='error')
#                     has_error = True
        
#         if not has_error:
#             try:
#                 existing_data = pd.read_csv(data_file)
#             except FileNotFoundError:
#                 existing_data = pd.DataFrame(columns=row_data.keys())

#             new_row = pd.Series(row_data)
#             new_row['id'] = str(uuid.uuid4())
#             new_row['date_created'] = date.today()

#             existing_data = existing_data.append(new_row, ignore_index=True)
#             existing_data.to_csv(data_file, index=False)
#             flash(success_message, category='success')
#             return redirect(url_for('views.home'))

#     return render_template(template_name, user=current_user, row_data=row_data, platform_names=platform_names)











# @views.route('/todo', methods=['GET', 'POST'])
# @login_required
# def add_task():
#     if request.method == 'POST':
#         task = request.form.get('task')

#         if len(task) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             # Create a new task as a dictionary
#             new_task = {
#                 'task': task,
#                 'user_id': current_user.id,
#                 'on_progress': True,
#                 'date_done': None,
#                 'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'id': str(uuid.uuid4())

#             }

#             if not os.path.isfile(TODO_CSV):
#                 # If the file doesn't exist, create it with a header
#                 initial_data = pd.DataFrame(columns=['task', 'user_id', 'on_progress', 'date_created'])
#                 initial_data.to_csv(TODO_CSV, index=False)

#             # Read existing data from the CSV file
#             existing_data = pd.read_csv(TODO_CSV)

#             # Append the new task to the existing tasks
#             new_task = existing_data.append(new_task, ignore_index=True)

#             # Save the updated data to the CSV file
#             new_task.to_csv(TODO_CSV, index=False)
#             flash('Note added!', category='success')

#         return redirect(url_for("views.add_task"))

#     # Initialize tasks as an empty list
#     tasks = []

#     # Read existing notes from the CSV file
#     if os.path.isfile(TODO_CSV):
#         tasks_data = pd.read_csv(TODO_CSV)
#         tasks = tasks_data.to_dict('records')  # Convert the DataFrame to a list of dictionaries

#     # Filter notes for the current user
#     user_tasks = [task for task in tasks if task['user_id'] == current_user.id]

#     # Sort the notes by date_created in descending order
#     user_tasks = sorted(user_tasks, key=lambda x: x['date_created'], reverse=True)

#     return render_template("note.html", user=current_user, tasks=user_tasks)



# @views.route('/create-credit', methods=['GET', 'POST'])
# @login_required
# def create_credit():
#     platform_names = get_platform_names()

#     if request.method == 'POST':

#         # Get form data
#         platform_name = request.form.get('platform_name')
#         owner = request.form.get('owner')
#         balance = request.form.get('balance')
#         cvv = request.form.get('cvv')
#         address = request.form.get('address')
#         card_holder = request.form.get('card_holder')
#         card_type = request.form.get('card_type')
#         card_website = request.form.get('card_website')
#         web_username = request.form.get('web_username')
#         web_password = request.form.get('web_password')
#         email = request.form.get('email')
#         email_password = request.form.get('email_password')
#         date_exp = request.form.get('date_exp')
#         card_number = request.form.get('card_number')
#         document_reference = request.form.get('document_reference')
#         notes = request.form.get('notes')
#         date_created = date.today()
#         id = str(uuid.uuid4())

#         # Create a new row as a dictionary
#         new_credit = pd.DataFrame({
#             'id': [id],
#             'platform_name': [platform_name],
#             'owner': [owner],
#             'balance': [balance],
#             'cvv': [cvv],
#             'address': [address],
#             'card_holder': [card_holder],
#             'card_type': [card_type],
#             'card_website': [card_website],
#             'website_username': [web_username],
#             'website_password': [web_password],
#             'email': [email],
#             'email_password': [email_password],
#             'date_exp': [date_exp],
#             'card_number': [card_number],
#             'document_reference': [document_reference],
#             'notes': [notes],
#             'date_created': [date_created],
#         })

#         try:
#             existing_data = pd.read_csv(CREDIT_CSV)
#             # Get the number of rows
#             num_rows = len(existing_data)
#             print(f'Total rows in {CREDIT_CSV}: {num_rows}')
#         except FileNotFoundError:
#             print(f'{CREDIT_CSV} does not exist or is empty.')

#         # Read the existing CSV file, if it exists
#         try:
#             existing_data = pd.read_csv(CREDIT_CSV)
#         except FileNotFoundError:
#             # If the file doesn't exist, create a new DataFrame
#             existing_data = pd.DataFrame(columns=new_credit.columns)

#         # Concatenate the new data with the existing data
#         new_data = pd.concat([existing_data, new_credit], ignore_index=True)
#         # Save the updated data to the Excel file
#         new_data.to_csv(CREDIT_CSV, index=False)
#         flash('Credit card added!', category='success')
#         # Redirect back to the form after submission
#         return redirect(url_for('views.create_credit'))

#     # Display the form initially
#     return render_template('create_credit.html', user=current_user, platform_names=platform_names)
