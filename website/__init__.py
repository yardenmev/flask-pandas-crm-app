from flask import Flask, render_template
from flask_login import login_required, current_user
# from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

# db = SQLAlchemy()
DB_NAME = "database.db"

def register_blueprints(app):
    from .views import views
    from .auth import auth
    # from .auth import read_users_from_csv

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # db.init_app(app)
    register_blueprints(app)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user=current_user), 404
    # from .models import User, Note, Service, Platform, Credit, agent
    from .auth import read_users_from_csv , User


    # with app.app_context():
        # db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # print(f"load_user called with ID: {id}")
        users_data = read_users_from_csv()
        # print(users_data)
        
        if not users_data.empty:  # Check if the DataFrame is not empty
            user = users_data.loc[(users_data['id'] == int(id)) & (users_data['id'].notna())]

            # print(f"User : {user}")
            
            if not user.empty:
                username = user['username'].values[0]
                user_group = user['group'].values[0]
                user_role = user['role'].values[0]

                # print(f"User found: {username}")
                return User(int(id), username, user_group, user_role)

        # print("User not found or DataFrame is empty.")
        return None   
    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
