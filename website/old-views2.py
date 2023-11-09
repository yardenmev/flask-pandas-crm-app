from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Service, Platform, Credit, agent
from .notes import notes
from datetime import datetime, date
from . import db
import uuid
import os
import pandas as pd
from sqlalchemy import asc

PLATFORM_CSV = "data_files/platforms_data.csv"
SERVICE_CSV = "data_files/services_data.csv"
CREDIT_CSV = 'data_files/credits_data.csv'
AGENTE_CSV = 'data_files/platform_users_data.csv'
TODO_CSV = 'data_files/todo_data.csv'

views = Blueprint("views", __name__)
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

    tasks_data = pd.read_csv(TODO_CSV)
    tasks = tasks_data.to_dict(orient="records")

    agents_data = pd.read_csv(AGENTE_CSV)
    agents_data = agents_data.fillna("-")
    agents = agents_data.to_dict(orient="records")

    return render_template("home2.html", user=current_user, services=services, tasks=tasks, agents=agents, platform_names=platform_names)

@views.route("/show-all/<platform_name>")
@login_required
def show_all(platform_name):
    services_data = pd.read_csv(SERVICE_CSV)
    services_data = services_data.fillna("-")
    # Filter the services data by platform_name
    services = services_data[services_data['platform_name'] == platform_name].to_dict(orient="records")

    credits_data = pd.read_csv(CREDIT_CSV)
    credits_data = credits_data.fillna("-")
    # Filter the credits data by platform_name
    credits = credits_data[credits_data['platform_name'] == platform_name].to_dict(orient="records")

    agents_data = pd.read_csv(AGENTE_CSV)
    agents_data = agents_data.fillna("-")
    # Filter the agents data by platform_name
    agents = agents_data[agents_data['platform_name'] == platform_name].to_dict(orient="records")

    return render_template("show_all.html", user=current_user, platform_name=platform_name, services=services, credits=credits, agents=agents)


@views.route("/create-service", methods=['GET', 'POST'])
@login_required
def create_service():
    platform_names = get_platform_names()
    if request.method == 'POST':
        platform_name = request.form.get('platform_name')
        used_by = request.form.get('used_by')
        service_type = request.form.get('service_type')
        website = request.form.get('website')
        web_username = request.form.get('web_username')
        web_password = request.form.get('web_password')
        email = request.form.get('email')
        email_password = request.form.get('email_password')
        ip = request.form.get('ip')
        ip_username = request.form.get('ip_username')
        ip_password = request.form.get('ip_password')
        date_exp = request.form.get('date_exp')
        doc_reff = request.form.get('doc_reff')
        phone = request.form.get('phone')
        country = request.form.get('country')
        etc = request.form.get('etc')
        date_created = date.today()
        id = str(uuid.uuid4())


        new_service = pd.DataFrame({
            'platform_name': [platform_name],
            'used_by': [used_by],
            'service_type': [service_type],
            'website': [website],
            'web_username': [web_username],
            'web_password': [web_password],
            'email': [email],
            'email_password': [email_password],
            'ip': [ip],
            'ip_username': [ip_username],
            'ip_password': [ip_password],
            'date_exp': [date_exp],
            'doc_reff': [doc_reff],
            'phone': [phone],
            'country': [country],
            'etc': [etc],
            'date_created': [date_created],
            'id': [id]
        })

        try:
            existing_data = pd.read_csv(SERVICE_CSV)
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame
            existing_data = pd.DataFrame(columns=new_service.columns)

        # Concatenate the new data with the existing data
        new_data = pd.concat([existing_data, new_service], ignore_index=True)
        # Save the updated data to the Excel file
        new_data.to_csv(SERVICE_CSV, index=False)
        flash('Service created!', category='success')
        return redirect(url_for('views.home'))

    return render_template('create_service.html', user=current_user, platform_names=platform_names)

@views.route("/create-platform-user", methods=['GET', 'POST'])
@login_required
def create_platform_user():
    platform_names = get_platform_names()

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        phone = request.form.get('phone')
        address = request.form.get('address')
        facebook_username = request.form.get('facebook_username')
        facebook_password = request.form.get('facebook_password')
        linkedIn_username = request.form.get('linkedIn_username')
        linkedIn_password = request.form.get('linkedIn_password')
        payoneer_username = request.form.get('payoneer_username')
        payoneer_password = request.form.get('payoneer_password')
        paypal_username = request.form.get('paypal_username')
        paypal_password = request.form.get('paypal_password')
        instagram_username = request.form.get('instagram_username')
        instagram_password = request.form.get('instagram_password')
        tiktok_username = request.form.get('tiktok_username')
        tiktok_password = request.form.get('tiktok_password')
        email1 = request.form.get('email1')
        email_password1 = request.form.get('email_password1')
        email2 = request.form.get('email2')
        email_password2 = request.form.get('email_password2')
        wp_username = request.form.get('wp_username')
        wp_password = request.form.get('wp_password')
        wp_site = request.form.get('wp_site')
        hosting_website = request.form.get('hosting_website')
        hosting_username = request.form.get('hosting_username')
        hosting_password = request.form.get('hosting_password')
        document_reference = request.form.get('document_reference')
        notes = request.form.get('notes')
        platform_name = request.form.get('platform_name')
        country = request.form.get('country')
        owner = request.form.get('owner')
        date_created = date.today()
        id = str(uuid.uuid4())

        # Create a new row as a dictionary
        new_agent = pd.DataFrame({
            'id': [id],
            'name': [name],
            'birth_date': [birth_date],
            'phone': [phone],
            'address': [address],
            'facebook_username': [facebook_username],
            'facebook_password': [facebook_password],
            'linkedIn_username': [linkedIn_username],
            'linkedIn_password': [linkedIn_password],
            'payoneer_username': [payoneer_username],
            'payoneer_password': [payoneer_password],
            'paypal_username': [paypal_username],
            'paypal_password': [paypal_password],
            'instagram_username': [instagram_username],
            'instagram_password': [instagram_password],
            'tiktok_username': [tiktok_username],
            'tiktok_password': [tiktok_password],
            'email1': [email1],
            'email_password1': [email_password1],
            'email2': [email2],
            'email_password2': [email_password2],
            'wp_username': [wp_username],
            'wp_password': [wp_password],
            'wp_site': [wp_site],
            'document_reference': [document_reference],
            'hosting_website': [hosting_website],
            'hosting_username': [hosting_username],
            'hosting_password': [hosting_password],
            'notes': [notes],
            'platform_name': [platform_name],
            'country': [country],
            'owner': [owner],
            'date_created': [date_created],
        })

        try:
            existing_data = pd.read_csv(AGENTE_CSV)
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=new_agent.columns)

        new_data = pd.concat([existing_data, new_agent], ignore_index=True)
        new_data.to_csv(AGENTE_CSV, index=False)
        flash('Agent created!', category='success')
        return redirect(url_for('views.create_platform_user'))

    return render_template('create_platform_user.html', user=current_user, platform_names=platform_names)

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

    if previous_page and '/todo' in previous_page:
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

@views.route("/edit-note/<id>", methods=['GET', 'POST'])
@login_required
def edit_note(id):
    return edit_row(
        TODO_CSV,
        id,
        'edit_note.html',
        'Note edited!',
        [
            'task',
        ]
    )



def create_row(data_file, template_name, url_redirect, success_message, row_data_fields, additional_fields):
    platform_names = get_platform_names()
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
            return redirect(url_for(url_redirect))

    return render_template(template_name, user=current_user, row_data=row_data, platform_names=platform_names)

@views.route("/create-platform", methods=['GET', 'POST'])
@login_required
def create_platform():
    # Check if the CSV file exists, and create it if it doesn't
    if not os.path.isfile(PLATFORM_CSV):
        # Create an empty DataFrame with the appropriate columns
        initial_data = pd.DataFrame(columns=['platform_name', 'date_created'])
        # Save it as the CSV file
        initial_data.to_csv(PLATFORM_CSV, index=False)

    platform_names = get_platform_names()

    if request.method == 'POST':
        platform_name = request.form.get('platform_name')
        date_created = date.today()

        if len(platform_name) < 1:
            flash('Platform name cannot be null!', category='error')
        elif platform_name in platform_names:
            flash('The platform already exists.', category='error')
        else:
            new_platform = pd.DataFrame({
                'platform_name': [platform_name],
                'date_created': [date_created],
            })

            try:
                existing_data = pd.read_csv(PLATFORM_CSV)

                if 'platform_name' in existing_data.columns:
                    # Check for duplicate platform names
                    if platform_name in existing_data['platform_name'].values:
                        flash('The platform already exists.', category='error')
                        return render_template('create_platform.html', user=current_user)
            except FileNotFoundError:
                existing_data = pd.DataFrame(columns=new_platform.columns)

            new_data = pd.concat([existing_data, new_platform], ignore_index=True)
            new_data.to_csv(PLATFORM_CSV, index=False)
            flash('Platform created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_platform.html', user=current_user)

@views.route('/create-credit', methods=['GET', 'POST'])
@login_required
def create_credit():
    return create_row(
    CREDIT_CSV,
    'create_credit.html',
    'views.home',
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


@views.route("/todo", methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        return create_row(
            TODO_CSV,
            'note.html',
            'views.add_task',
            'Task added!',
            ['task'],
            {'on_progress': True,
             'user_id': current_user.id
            }
            
        )

    tasks = []  # Initialize tasks as an empty list

    if os.path.isfile(TODO_CSV):
        tasks_data = pd.read_csv(TODO_CSV)
        tasks = tasks_data.to_dict('records')  # Convert the DataFrame to a list of dictionaries
    
    user_tasks = [task for task in tasks if task['user_id'] == current_user.id]

    # Sort the tasks by date_created in descending order
    user_tasks = sorted(user_tasks, key=lambda x: x['date_created'], reverse=False)

    return render_template("note.html", user=current_user, tasks=user_tasks)
    