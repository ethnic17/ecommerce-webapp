"""now it's job is to only run, so we will rename it to run.py"""
# from winepro import app #it will import from the init file means whenever we import something from package, it is imported from the init filw
from winepro import create_app, db # now we can create our apps
app = create_app()
if(__name__=="__main__"):
    with app.app_context():
        db.create_all()
    app.run()









# #importing the forms that we have created
# from flask import Flask, render_template, flash, redirect, url_for
# from forms import RegistrationForm, LoginForm 
# from flask_sqlalchemy import SQLAlchemy
# # we moved the models in the seperated file and now we are importing
# #if we try to run it will give error because
# """
# when the line from models import User thing is run, the whole models.py will run
# so when it goes to models.py, it gets to from templates import db and thinks it haven't found db
# variable till now, then it goes again to templates.py.
# But before this, we know python scripts are run as __main__ thing, so when it goes again to templates.py
# it reads all then it again encounters models import User, but it thinks that it have already seen models
# but didn't find any user or item thing (as they are below the import statement), so we get the rror
# that User can't be imported.
# So if we do from __main__ import db inside the models.py, we will get the error that the db variable can't be imported or found.

# so to solve the problem,  we will now create different files and use everything as the package
# """
# # from models import User, Item

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'ac62e12f376a25854f404c11394ca8b0'
# #the below line creates a instance folder and stores the database in that folder only
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #the 3 dash means the relative path to the database is our file only and so a new file named db will be created in the folder or dir

# db = SQLAlchemy(app) #this is the instance for database
# from models import User, Item


# class User(db.Model):
#     #primary keys are automatically generated
#     id = db.Column(db.Integer, primary_key=True) #primary key means the id is unique and will differentiate the users
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     #one user can have many Items, so we create a relationship between user and items, which is one to many relationship
#     #by below, we can access user.items and then item.author and lazy means data is loaded only when accessed
#     items = db.relationship('Item', backref='author', lazy=True)
#     # posts = db.relationship('Post', backref='author', lazy=True)

#     #the repr is the method which contains the string which will be printed when we try to print the object of this class
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     brand = db.Column(db.String(50), nullable=False)
#     brandpic = db.Column(db.String(20), nullable=True, default='brand.jpg')
#     rate = db.Column(db.Integer, nullable=False)
#     # added_by = db.Column(db.String, nullable=False)
#     #we used small u because the table is created as user and item, not case sensitive, so we want to get user ids when we work with items that why we write it
#     #foreign key is a column that refers to the primary key of the another table
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Item('{self.id}', '{self.brand}', '{self.rate}')"



#instead of writing html code here for different webpages, we can use templates, which will be created in the same folder
#we use render_template functoin from flask
# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html') #we have posts that are to be uploaded here, the posts variable will help to acccess posts
#     #if title is provided then it will print flask blog - title else it will print flask blog

# @app.route("/store")
# def store():
#     return render_template('store.html', title="store")
# #the above two decorators means that / and /home are same

# @app.route("/about")
# def about():
#     return render_template('about.html', title="about")
# #if you see the about and home template, lot of the code is
# """duplicated, so we can use template inheritance to sort it out
# we will create a layout template which will have the code
# which is common to both home and layout and use it."""

# # if i submit details in register, we would get method not allowed because we haven't passed any methods in the register 
# # after putting it, as we had action="", it would get us to that page again
# @app.route("/")
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     #now we have to create actual object (instance) of the form that we would pass
#     form = RegistrationForm()

#     #there is no validation whether the form is created or no, so for this we use flash from flask
#     if form.validate_on_submit():
#         #validate on submit check if the form was submitted via POST and it have passed all DataRequired(), Email(), Lenght() things
#         flash(f'Account created for {form.username.data}!', 'success')
#         #form.username is the object while .data give access to the actual value submitted by the user
        
#         return redirect(url_for('home'))
    
#     #as the registration is successful, we will redirect the user to the home page
#     #import redirect from flask only

#     return render_template('register.html', title='Register', form=form) #the right form is the name by which we will acess the instance form in the html template file

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     #now we have to create actual object (instance) of the form that we would pass
#     form = LoginForm()

#     if form.validate_on_submit():
#         # now we will check if the data entered is correct or not, so we will now validate things, since we don't have database now, we will put dummy details as correct
#         if form.username.data == "rudransh" and form.password.data == "rudransh":
#             flash("Login Successful", 'success')
#             return redirect(url_for('home'))
#         else:
#             flash("Login Unsuccessfull, please check your credentials", 'danger')
#     return render_template('login.html', title='login', form=form) #the right form is the name by which we will acess the instance form in the html template file










