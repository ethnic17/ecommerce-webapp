from flask import Blueprint
"""
here we will have routes and everything they need ( if they use dummy data then that also)
"""
import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from winepro import db, bcrypt, mail
from winepro.models import User, Item
from winepro.users.forms import RegistrationForm, LoginForm, UpdateAccount, AddItemForm, EditItemForm
from winepro.items.forms import  ResetPasswordForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required 
from flask_mail import Message

main = Blueprint('main', __name__)


@main.route("/home")
def home():
    items = Item.query.filter_by(user_id=current_user.id)
    return render_template('home.html', items = items) #we have posts that are to be uploaded here, the posts variable will help to acccess posts

@main.route("/store")
@login_required
def store():
    items = Item.query.all()
    return render_template('store.html', title="store", items = items)
#the above two decorators means that / and /home are same

@main.route("/about")
def about():
    return render_template('about.html', title="about")
#if you see the about and home template, lot of the code is
"""duplicated, so we can use template inheritance to sort it out
we will create a layout template which will have the code
which is common to both home and layout and use it."""

# if i submit details in register, we would get method not allowed because we haven't passed any methods in the register 
# after putting it, as we had action="", it would get us to that page again

