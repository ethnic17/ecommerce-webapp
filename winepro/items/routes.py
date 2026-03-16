from flask import Blueprint
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

items = Blueprint('items', __name__)

@items.route("/add",  methods=['POST', 'GET'])
@login_required
def add():
    form = AddItemForm()

    if form.validate_on_submit():
        pic_file = 'default.jpg'

        if form.pic.data:
            pic_file = savepic1(form.pic.data)
        # image_file = url_for('static', filename=f"images/{item.image_file}")

        item = Item(user_id = current_user.id, brand=form.brandname.data, brandpic=pic_file, rate=form.price.data)

        db.session.add(item)
        db.session.commit()

        flash("Item added successfully!", "success")
        return redirect(url_for('main.store'))

    return render_template('additem.html', title='account', form=form)


@items.route('/edit/<item_id>', methods=['GET', 'POST'])
@login_required

def edit(item_id):
    form = EditItemForm()
    

    if form.validate_on_submit():
        item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
        # if not item:
        #     flash('Cant Update item not added by you', 'danger')
        #     return redirect(url_for('store'))

        if form.pic.data:
            file = savepic1(form.pic.data)
            item.brandpic = file

        item.brand = form.brandname.data
        item.rate = form.price.data
        image_file = url_for('static', filename=f"brandimages/{item.brandpic}")
        db.session.commit()
        flash('Item updated', 'success')
        return redirect(url_for('main.home'))
    
    # elif request.method=='GET':
    #     form.brandname.data = item.username
    #     form.price.data = item.rate
    

    return render_template('edit.html', title='edit item', form=form)

#now suppose you want to see the item specially, so <> will contain the id

@items.route("/home/<int:item_id>")
@items.route("/store/<item_id>")

@login_required
def getitem(item_id):
    # item = Item.query.get(item_id)
    item = Item.query.get_or_404(item_id)
    #the above will give 404 error if the template doesn't exits

    return render_template('item.html', title=item.brand, item=item)

@items.route("/delete/<int:item_id>", methods=['POST'])
@login_required
def deleteitem(item_id):
    # item = Item.query.get(item_id)
    item = Item.query.get_or_404(item_id)
    

    if current_user.id==item.user_id:
        db.session.delete(item)
        db.session.commit()
        item = Item.query.all()
        flash("Item deleted successfully", 'danger')
        return redirect(url_for('main.home'))
    #the above will give 404 error if the template doesn't exits

    return render_template('item.html', title=item.brand, item=item)



#for forget password thing, we will generate a secure time sensitive token
#we use itsdangerous module which is downloaded with flask
# Only someone who knows the secret key can create valid tokens.
#When we send the request for password reset, we have a token assigned, which is the 
"""combination of signature and many things, so if i load that thing after
the max age, then it tries to calculate the signature again but finds out that the time
have expired, so it then doesn't allow us"""

"""
>>> token = s.dumps({'user_id': 5}).decode('utf-8') it is uesd because if a user post a request for foret password then server must respond for which user? token solves the problem
>>> print(token) 
eyJ1c2VyX2lkIjo1fQ.abFXLg.hM0D6UG76hoeTvUjm_yRhMC8adM
>>> data=s.loads(token, max_age=50) #here the verification takes place when a request come to server after the user clicks the link
#then the server loads the user

this is usefull because we will have a url like reset/id, so if someone tampers the token like id=1 to 2 then the signature breaks and request is not entertained

>>> print(data)
{'user_id': 5}
"""