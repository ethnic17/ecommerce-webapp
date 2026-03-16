# from __main__ import db
from winepro import db, lm #app because we will need the secret key
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as ser

#this is the function to get the user by id
@lm.user_loader #so that the function knows this is the only function
def load_user(user_id):
    return User.query.get(int(user_id))
#now we have to get the userloader so to reload the user in the current session

# class User(db.Model):
#the extension expects our User Model to have some special methods and attributes such as
#isauthenticated, isactive, isanonymous and getid, get id is added and rest can be added by UserMixin
class User(db.Model, UserMixin): #db.Model is for the creating of a table in the database, just like the blueprint
    #primary keys are automatically generated
    id = db.Column(db.Integer, primary_key=True) #primary key means the id is unique and will differentiate the users
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #one user can have many Items, so we create a relationship between user and items, which is one to many relationship
    #by below, we can access user.items and then item.author and lazy means data is loaded only when accessed
    items = db.relationship('Item', backref='author', lazy=True)
    # posts = db.relationship('Post', backref='author', lazy=True)

    #we will create a method to get reset token
    def get_rtoken(self, expire=60):
        s = ser(current_app.config['SECRET_KEY'])
        # token = s.dumps({'user_id': self.id}).decode('utf-8')
        token = s.dumps({'user_id': self.id}) #.decode not necessary because newer version of itsdangerous dumps() already returns a string not bytes so don't decode

        return token
    
    @staticmethod
    def ver_rtoken(token):
        s = ser(current_app.config['SECRET_KEY'])

        try:
            # user_id = s.loads(token)['user_id']
            #we must apply the expiration here
            user_id = s.loads(token, max_age=120)['user_id']
        except:
            return None
        
        return User.query.get(user_id)
        
    #the repr is the method which contains the string which will be printed when we try to print the object of this class
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.password}, '{self.image_file}')"
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    brandpic = db.Column(db.String(20), nullable=True, default='default.jpg')
    rate = db.Column(db.Integer, nullable=False)

    #we used small u because the table is created as user and item, not case sensitive, so we want to get user ids when we work with items that why we write it
    #foreign key is a column that refers to the primary key of the another table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.id}', '{self.brand}', '{self.rate}')"