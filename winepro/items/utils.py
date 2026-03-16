import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from winepro import db, bcrypt, mail
from flask import current_app
from winepro.models import User, Item
from winepro.forms import RegistrationForm, LoginForm, UpdateAccount, AddItemForm, EditItemForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required 
from flask_mail import Message


def savepic1(form_pic):
    #we use this function to save the picture if submitted by the user
    #we don't want to keep the name of the file image so we will use the hex, so import secrets module
    random_hex = secrets.token_hex(8)
    #it should be save as jpg or png whatever the user puts, so we will use os module to grab the extension

    _, f_ext = os.path.splitext(form_pic.filename) #form_pic is the data from the filed that user submits so it will have a filename attribute obviously
    picture_fn = random_hex+f_ext

    picture_path = os.path.join(current_app.root_path, 'static/brandimages', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    # creates the full path where the image will be saved
    #app.root_path gives the main folder path of our flask project
    #we use os.path.join because in mac we use / intsead of \ so the os do it itself
    # form_pic.save(picture_path) #now we have saved the picture path, but the image is not updated till now
    i.save(picture_path)

    return picture_fn

