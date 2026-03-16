from flask import Blueprint

users = Blueprint('users', __name__)

"""
here we will have routes and everything they need ( if they use dummy data then that also)
"""
import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from winepro import db, bcrypt, mail
from flask import current_app
from winepro.models import User, Item
from winepro.users.forms import RegistrationForm, LoginForm, UpdateAccount, AddItemForm, EditItemForm
from winepro.items.forms import  ResetPasswordForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required 
from flask_mail import Message

#users is the name of the blueprint
#we made a instance

#now we will make the routes specifically for this users blueprint and then register with the app later
#we will use users.route instead of app.route

@users.route("/")
@users.route("/register", methods=['GET', 'POST'])

def register():
    #if user is logged in, he shouldn't see the login button, so we import current_user from flask_login
    #or even if he click on login or registration, nothing should happen
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    #now we have to create actual object (instance) of the form that we would pass
    form = RegistrationForm()

    #there is no validation whether the form is created or no, so for this we use flash from flask
    if form.validate_on_submit():
        #validate on submit check if the form was submitted via POST and it have passed all DataRequired(), Email(), Lenght() things

        """now we have to create hashed password to save it on the database """
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        """to create a user in the database"""
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created! Now you can login', 'success')
        # flash(f'Account created for {form.username.data}!', 'success')
        #form.username is the object while .data give access to the actual value submitted by the user
        
        # return redirect(url_for('home'))
        return redirect(url_for('users.login'))
    
    #as the registration is successful, we will redirect the user to the home page
    #import redirect from flask only

    return render_template('register.html', title='Register', form=form) #the right form is the name by which we will access the instance form in the html template file

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #now we have to create actual object (instance) of the form that we would pass
    form = LoginForm()

    if form.validate_on_submit():
        # now we will check if the data entered is correct or not, so we will now validate things, since we don't have database now, we will put dummy details as correct
        # if form.username.data == "rudransh" and form.password.data == "rudransh":
        #     flash("Login Successful", 'success')
        #     return redirect(url_for('home'))

        #now real authentication. first we will check if user exists and then we will check if same email address exists and return the first user
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #now we will log the user in, so import login_user from flask_login
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #see, args is a dictionary type object, and if we had tried to acces it like args['next] and the key didn't exist then it would have given us the rror
            #so we use get method which just returns null if the value doesn't exist
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash("Login Unsuccessfull, please check your credentials", 'danger')
    return render_template('login.html', title='login', form=form) #the right fo

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

#we may want some page which should only be visible if you are loggedi n

#to make this account page non accessible for no login user, we can use login required decorator 

@users.route("/account", methods=['GET', 'POST'])
@login_required #we also need to tell where the login route is located
#so the thing is if you had tried to go to account page, then it would have told to login
#and in the above, you can see something like ?next thing which is a query and indicates which page the user was trying to go to
#so we can use that to redirect to that page if the query exists, which will be after the user had logged in
#for that first import request from flask

#when you update the image, it takes the whole screen so for this, we use pillow to resize the image
def account():
    form = UpdateAccount()
    #to pass image to template, we have to share the image folder
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = savepic(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('account updated', 'success')
        return redirect(url_for('users.account')) 
        """we use redirect intead of render template because of post get redirect pattern, like that when it says data will be resubmitted etc, 
        IF WE HAD USED RENDER_TEMPLATE, after we have submitted the fomr, it will look fine but if we refresh it, it asks do you want to resubmit because
        the last request was a post request, and if user clicks yes, it will get into duplicate entries.
        
        if we use redirect, the server automatically makes a new request of GET/account and the account page is loaded via GET, so if user refresh, the request GET will work"""

    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"images/{current_user.image_file}") #user.image_file me image file User model ka hai
    
    return render_template('account.html', title='account', image_file=image_file, form=form)

#now we will create a page where the user will be able to add the items

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_p():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    """flow is when we click forget password, we are logged out before that only, so as we enter the email, the server then get all the info
    of the user so then it creates the token using the user_id and then sends a link to the email"""
    
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #now i would want to send the user the email to reset the password
        send_reset_email(user)

        # token = user.get_rtoken()
        flash("Email sent", "success")
        redirect(url_for('users.login'))
    return render_template('reset_req.html', title='Reset Password', form=form)

    #we want the user to be logged out here to reset the password

#now the route where the user resets the password, so here we will need the verified token
#to make sure the user is same, we need to see if the token we gave him with the email is still active, the url sent with the email will contain the token

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_actpas(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    #now first we will verify the user
    user = User.ver_rtoken(token)

    #now if i don't get a user it means the token is invalid or expired

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed
        db.session.commit()

        flash(f'Password Reseted! Now you can login', 'success')
        return redirect(url_for('main.login'))
    
    return render_template("reset_pas.html", title="Reset Passowrd", form=form)

