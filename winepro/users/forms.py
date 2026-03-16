from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed 
from winepro.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
            validators = [DataRequired(), Email()])
    
    password = PasswordField('Password',
            validators = [DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
            validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    #we create our own validation check

    """ so, what happens is when we put the request on the website, a form = RegistrationForm() object is created.
    then it comes in this file and takes all the inputs, then the flask looks for custom validators, in form validate_<fieldname>
    if there, then it validates it, otherwise it just runs validate_on_submit and do the checks
    """
    
    def validate_username(self, username): #as we want to check username, we will need username, so we import it
        user = User.query.filter_by(username=username.data).first() #username.data is soemthing that is coming from the form and is same as the parameter of this function

        if user: #if user exists then it won't be null else null
            raise ValidationError('Username exists.') #this ValidationError is just like check
        

    def validate_email(self, email): #as we want to check username, we will need username, so we import it
        user = User.query.filter_by(email=email.data).first() #username.data is soemthing that is coming from the form and is same as the parameter of this function

        if user: #if user exists then it won't be null else null
            raise ValidationError('Email exists.')    


class LoginForm(FlaskForm):
    username = StringField('Username', 
            validators=[DataRequired(), Length(min=2, max=30)])
    
    password = PasswordField('Password',
            validators = [DataRequired()])

    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class UpdateAccount(FlaskForm):
    username = StringField('Username', 
            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
            validators = [DataRequired(), Email()])
    
    picture = FileField('Update Profile Pic', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Change')
    
    def validate_username(self, username): #now, if the entered username is different from the existing, then only we want to perform check
        #so we need the current user username and email so we will import current_user from flask_login

        if username.data!=current_user.username:
                user = User.query.filter_by(username=username.data).first() #username.data is soemthing that is coming from the form and is same as the parameter of this function

                if user: #if user exists then it won't be null else null
                        raise ValidationError('Username exists.') #this ValidationError is just like check
        

    def validate_email(self, email): #as we want to check username, we will need username, so we import it
        user = User.query.filter_by(email=email.dataa).first() #username.data is soemthing that is coming from the form and is same as the parameter of this function
        if email.data!=current_user.email:
                if user: #if user exists then it won't be null else null
                        raise ValidationError('Email exists.')
                
#for adding the items, we need a form
class AddItemForm(FlaskForm):
    brandname = StringField('Name', 
            validators=[DataRequired(), Length(min=2, max=20)])
    
    price = IntegerField('Price',
            validators = [DataRequired()])

    pic = FileField('Add Image', validators=[FileAllowed(['jpg', 'jpng', 'png'])])    
    submit = SubmitField('Add')

class EditItemForm(FlaskForm):
    brandname = StringField('Name', 
            validators=[Length(min=2, max=20)])
    
    price = IntegerField('Price')

    pic = FileField('Change Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])    
    submit = SubmitField('Update')