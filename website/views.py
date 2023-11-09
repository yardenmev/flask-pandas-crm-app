from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
import uuid
import os
import pandas as pd
from sqlalchemy import asc
from .auth import *

PLATFORM_CSV = "data_files/platforms_data.csv"
SERVICE_CSV = "data_files/services_data.csv"
CREDIT_CSV = 'data_files/credits_data.csv'
AGENTE_CSV = 'data_files/platform_users_data.csv'
TODO_CSV = 'data_files/todo_data.csv'
USERS_CSV = 'data_files/users_data.csv'
views = Blueprint("views", __name__)


def sort_task_by_user(user_id):
    tasks = []  # Initialize tasks as an empty list

    if os.path.isfile(TODO_CSV):
        tasks_data = pd.read_csv(TODO_CSV)
        tasks = tasks_data.to_dict('records')  # Convert the DataFrame to a list of dictionaries
    
    user_tasks = [task for task in tasks if task['user_id'] == user_id]
    # Sort the tasks by date_created in descending order
    user_tasks = sorted(user_tasks, key=lambda x: x['date_created'], reverse=True)
    return user_tasks

def get_platform_names():
    global platform_names  
    platforms_data = pd.read_csv(PLATFORM_CSV)
    platform_names = platforms_data.iloc[:, 0].tolist()
    return platform_names

@views.route("/")
@views.route("/home")
@login_required
def home():
    platform_names = get_platform_names()

    services_data = pd.read_csv(SERVICE_CSV)
    services_data = services_data.fillna("-")
    services = services_data.to_dict(orient="records")

    # tasks_data = pd.read_csv(TODO_CSV)
    # tasks = tasks_data.to_dict(orient="records")
    tasks = sort_task_by_user(current_user.id)

    agents_data = pd.read_csv(AGENTE_CSV)
    agents_data = agents_data.fillna("-")
    agents = agents_data.to_dict(orient="records")

    return render_template("home.html", user=current_user, services=services, tasks=tasks, agents=agents, platform_names=platform_names)

@views.route("/show-all/<platform_name>")
@login_required
def show_all(platform_name):
    services_data = pd.read_csv(SERVICE_CSV)
    services_data = services_data.fillna("-")
    services = services_data[services_data['platform_name'] == platform_name].to_dict(orient="records")

    credits_data = pd.read_csv(CREDIT_CSV)
    credits_data = credits_data.fillna("-")
    credits = credits_data[credits_data['platform_name'] == platform_name].to_dict(orient="records")

    agents_data = pd.read_csv(AGENTE_CSV)
    agents_data = agents_data.fillna("-")
    agents = agents_data[agents_data['platform_name'] == platform_name].to_dict(orient="records")

    return render_template("show_all.html", user=current_user, platform_name=platform_name, services=services, credits=credits, agents=agents)

@views.route("/delete/<kind>/<id>", methods=['GET', 'POST'])
@login_required
def delete_data(kind, id):
    # Check the 'kind' parameter to determine which type of data to delete
    if kind == 'service':
        data_csv = SERVICE_CSV
    elif kind == 'credit':
        data_csv = CREDIT_CSV
    elif kind == 'agent':
        data_csv = AGENTE_CSV
    elif kind == 'task':
        data_csv = TODO_CSV

    existing_data = pd.read_csv(data_csv)

    # Find the row with the matching 'id'
    row_to_delete = existing_data[existing_data['id'] == id]

    if row_to_delete.empty:
        flash("Row with the given ID not found.", category='error')
    else:
        # Drop the row with the matching 'id'
        existing_data = existing_data[existing_data['id'] != id]

        # Save the updated DataFrame back to the CSV file
        existing_data.to_csv(data_csv, index=False)
        flash(f'{kind.capitalize()} deleted.', category='success')

    if kind == 'task':
        return redirect(url_for("views.add_task"))
    else:
        return redirect(url_for('views.home'))

@views.route("/update-task-status/<id>", methods=['POST'])
@login_required
def update_task_status(id):
    existing_data = pd.read_csv(TODO_CSV)

    # Toggle the 'on_progress' value
    existing_data.loc[existing_data['id'] == id, 'on_progress'] = \
    ~existing_data.loc[existing_data['id'] == id, 'on_progress']

    existing_data.loc[existing_data['id'] == id, 'date_done'] = datetime.utcnow()

    # Save the updated data back to the CSV file
    existing_data.to_csv(TODO_CSV, index=False)

    previous_page = request.referrer

    if previous_page and '/create_task' in previous_page:
        return redirect(url_for('views.add_task'))
    else:
        return redirect(url_for('views.home'))

def edit_row(data_file, id, template_name, success_message, row_data_fields):
    platform_names = get_platform_names()
    row_data = []
    existing_data = pd.read_csv(data_file)
    row_to_edit = existing_data[existing_data['id'] == id]
    if row_to_edit.empty:
        flash("Row with the given ID not found.", category='error')
        return redirect(url_for('views.home'))

    else:
        row_data = row_to_edit.iloc[0]
        row_data = row_data.fillna("")

        if request.method == 'POST':
            has_error = False  # Track if any errors occur
            for field in row_data_fields:
                row_data[field] = request.form.get(field)
                if field == "task" and len(row_data[field]) == 0:
                    flash("Task field can't be empty!", category='error')
                    has_error = True

            if not has_error:
                existing_data.iloc[row_to_edit.index[0]] = row_data
                existing_data.to_csv(data_file, index=False)
                flash(success_message, category='success')
                return redirect(url_for('views.home'))


    return render_template(template_name, user=current_user, row_data=row_data, id=id, platform_names=platform_names)

@views.route("/edit-credit/<id>", methods=['GET', 'POST'])
@login_required
def edit_credit(id):
    return edit_row(
        CREDIT_CSV,
        id ,
        'edit_credit.html',
        'Credit edited!',
        [
            'platform_name',
            'owner',
            'balance',
            'cvv',
            'address',
            'card_holder',
            'card_type',
            'card_website',
            'website_username',
            'website_password',
            'email',
            'email_password',
            'date_exp',
            'card_number',
            'document_reference',
            'notes'
        ]
    )

@views.route("/edit-platform-user/<id>", methods=['GET', 'POST'])
@login_required
def edit_platform_user(id):
    return edit_row(
        AGENTE_CSV,
        id,
        'edit_platform_user.html',
        'platform user edited!',
        [
            "name",
            "birth_date",
            "phone",
            "address",
            "facebook_username",
            "facebook_password",
            "linkedIn_username",
            "linkedIn_password",
            "payoneer_username",
            "payoneer_password",
            "paypal_username",
            "paypal_password",
            "instagram_username",
            "instagram_password",
            "tiktok_username",
            "tiktok_password",
            "email1",
            "email_password1",
            "email2",
            "email_password2",
            "wp_username",
            "wp_password",
            "wp_site",
            "document_reference",
            'hosting_website',
            'hosting_username',
            'hosting_password',
            "notes",
            "platform_name",
            "country",
            "owner",
            "date_created"

        ]
    )

@views.route("/edit-service/<id>", methods=['GET', 'POST'])
@login_required
def edit_service(id):
    return edit_row(
        SERVICE_CSV,
        id,
        'edit_service.html',
        'Service edited!',
        [
            'platform_name',
            'used_by',
            'service_type',
            'website',
            'web_username',
            'web_password',
            'email',
            'email_password',
            'ip',
            'ip_username',
            'ip_password',
            'date_exp',
            'doc_reff',
            'phone',
            'country',
            'etc'
        ]
    )

@views.route("/edit-task/<id>", methods=['GET', 'POST'])
@login_required
def edit_task(id):
    return edit_row(
        TODO_CSV,
        id,
        'edit_task.html',
        'Task edited!',
        [
            'task',
        ]
    )

def create_row(data_file, template_name, url_redirect, success_message, row_data_fields, additional_fields, user_id=1):
    platform_names = get_platform_names()
    user_info = get_user_info_by_id(user_id)

    row_data = {}

    if request.method == 'POST':
        has_error = False
        row_data = {}
        for field in row_data_fields:
            row_data[field] = request.form.get(field)

            if field == "task" and len(row_data[field]) == 0:
                flash("Task field can't be empty!", category='error')
                has_error = True
            elif field == "platform_name" and len(row_data[field]) == 0:
                flash("Platform name field can't be empty!", category='error')
                has_error = True
        if "create-platform" in request.form:
            if row_data["platform_name"] in platform_names:
                flash('The platform already exists.', category='error')
                has_error = True

        if not has_error:
            try:
                existing_data = pd.read_csv(data_file)
            except FileNotFoundError:
                existing_data = pd.DataFrame(columns=row_data.keys())

            new_row = pd.Series(row_data)
            new_row['id'] = str(uuid.uuid4())
            new_row['date_created'] = date.today()

            # Add additional fields if defined in the additional_fields dictionary
            for field, value in additional_fields.items():
                new_row[field] = value

            existing_data = existing_data.append(new_row, ignore_index=True)
            existing_data.to_csv(data_file, index=False)
            flash(success_message, category='success')
            return redirect(url_redirect)
    return render_template(template_name, user=current_user, row_data=row_data, platform_names=platform_names, user_name=user_info['username'])

@views.route("/create-service", methods=['GET', 'POST'])
@login_required
def create_service():
    return create_row(
        SERVICE_CSV,
        'create_service.html',
        "url_for(views.home)",
        'Service created!',
        [
        'platform_name',
        'used_by',
        'service_type',
        'website',
        'web_username',
        'web_password',
        'email',
        'email_password',
        'ip',
        'ip_username',
        'ip_password',
        'date_exp',
        'doc_reff',
        'phone',
        'country',
        'etc',
        'date_created',
        'id'
        ],
        { }
    )

@views.route("/create-platform-user", methods=['GET', 'POST'])
@login_required
def create_platform_user():
    return create_row(
        AGENTE_CSV,
        'create_platform_user.html',
        "url_for(views.home)",
        'Platform added!',
        [  
        'id',
        'name',
        'phone',
        'birth_date',
        'address',
        'facebook_username',
        'facebook_password',
        'linkedIn_username',
        'linkedIn_password',
        'payoneer_username',
        'payoneer_password',
        'paypal_username',
        'paypal_password',
        'instagram_username',
        'instagram_password',
        'tiktok_username',
        'tiktok_password',
        'email1',
        'email_password1',
        'email2',
        'email_password2',
        'wp_username',
        'wp_password',
        'wp_site',
        'document_reference',
        'hosting_website' ,
        'hosting_username',
        'hosting_password',
        'notes',
        'platform_name',
        'country',
        'owner',
        'date_created',
        ],
        { }
    )

@views.route("/create-platform", methods=['GET', 'POST'])
@login_required
def create_platform():
        return create_row(
            PLATFORM_CSV,
            'create_platform.html',
            "url_for(views.home)",
            'Platform addedaaaaaaa!',
            ['platform_name'],
            { }
            
        )
    
@views.route('/create-credit', methods=['GET', 'POST'])
@login_required
def create_credit():
    return create_row(
    CREDIT_CSV,
    'create_credit.html',
    "url_for(views.home)",
    'credit added!',
    [
    'id',
    'platform_name',
    'owner',
    'balance',
    'cvv',
    'address',
    'card_holder',
    'card_type',
    'card_website',
    'website_username',
    'website_password',
    'email',
    'email_password',
    'date_exp',
    'card_number',
    'document_reference',
    'notes',
    'date_created'
    ],

    {   
    'user_id': current_user.id
    }   
)

def get_group_users_tasks():
    if current_user.role == 1:
        if os.path.isfile(TODO_CSV):
            tasks_data = pd.read_csv(TODO_CSV)

            # Create a dictionary to store DataFrames for each user in the group
            group_user_task_dfs = {}

            # Filter tasks based on group and exclude the current user
            group_tasks = tasks_data[(tasks_data['group'] == current_user.group) & (tasks_data['user_id'] != current_user.id)]

            # Group the tasks by user ID
            grouped = group_tasks.groupby('user_id')

            # Iterate through each user's tasks and store them in separate DataFrames
            for user_id, group in grouped:
                user_task_df = group.copy()
                group_user_task_dfs[user_id] = user_task_df

            return group_user_task_dfs

    return {}  # Return an empty dictionary if the role is not 1 or the file doesn't exist

def get_user_info_by_id(user_id):
    # Read the user data from the CSV file into a DataFrame
    user_data = pd.read_csv(USERS_CSV)

    # Filter the DataFrame to get the user with the specified ID
    user_info = user_data[user_data['id'] == user_id]

    # Check if the user with the given ID exists
    if not user_info.empty:
        # Extract the user's name from the DataFrame
        user_name = user_info['username'].values[0]
        return {'id': user_id, 'username': user_name}
    else:
        return None  # User not found
    
@views.route("/create-task/<int:user_id>", methods=['GET', 'POST'])
@login_required
def add_task_for_user(user_id):
    user_info = get_user_info_by_id(user_id)
    user_tasks = sort_task_by_user(user_id)
    print(user_info)
    if request.method == 'POST':
        return create_row(
            TODO_CSV,
            'create_task_for_user.html',
            request.referrer,
            'Task added!',
            ['task'],
            {
            'on_progress': True,
            'user_id': int(user_id),
            'username': user_info['username'],
            'group': current_user.group,
            },
            user_id=user_id
        )

    if current_user.role == 1:
        return render_template("create_task_for_user.html", user=current_user, user_name=user_info['username'],tasks=user_tasks )
    else:
        return render_template("create_task_for_user.html", user=current_user)

@views.route("/create_task", methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        return create_row(
            TODO_CSV,
            'create_task.html',
            request.referrer,
            'Task added!',
            ['task'],
            {
            'on_progress': True,
            'user_id': int(current_user.id),
            'username': current_user.username,
            'group': current_user.group,

            }
            
        )

    user_tasks = sort_task_by_user(current_user.id)
    if current_user.role == 1:
        group_users_tasks = get_group_users_tasks()
        # print(group_users_tasks)
        return render_template("create_task.html", user=current_user, tasks=user_tasks, group_users_tasks=group_users_tasks)
    else:
        return render_template("create_task.html", user=current_user, tasks=user_tasks)

