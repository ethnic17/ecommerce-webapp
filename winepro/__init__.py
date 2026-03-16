"""
in the package templates, we will import everything except templates.py (templates is the package and templates.py is the app file)
"""

"""
in init file, we will initialize our application and bring different components

so all the imports and part were we are creating the app
"""
# from flask import Flask, render_template, flash, redirect, url_for #some are only used in routes, so we will move them there
from flask import Flask 
import os 
# from forms import RegistrationForm, LoginForm #only used in routes 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from winepro.config import Config

#we will need a mail server, mail port, user and password to send a mail

#for login systems
from flask_login import LoginManager

#we also have to import the routes here as when we run the file, it should find the routes
#we won't use the import statement here as the import route will go to routes.py and then it will find the import app whidh will cause circular import loop

bcrypt = Bcrypt()
lm = LoginManager()
#if a user tries to access a page where the decorator is @login_required, he will be redirected to a page mentioned in login_view
lm.login_view = 'users.login' #that view is the function name of our route
#also the text it uses is ugly, so we do the following thing
lm.login_message_category = 'info'
db = SQLAlchemy() #this is the instance for database
mail = Mail()

#now we have to add some functionality to databse models

#creating the function for the app run

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    lm.init_app(app)
    mail.init_app(app)

    from winepro.users.routes import users
    from winepro.items.routes import items
    from winepro.main.routes import main
    from winepro.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(items)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

#now we can't import app because we don't have app variable
