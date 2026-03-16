from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed 
from winepro.models import User

class RequestResetForm(FlaskForm):
    email = StringField('Email',
            validators = [DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email): #as we want to check username, we will need username, so we import it
        user = User.query.filter_by(email=email.data).first() #username.data is soemthing that is coming from the form and is same as the parameter of this function
        if user is None: #if user exists then it won't be null else null
                raise ValidationError('Email doesnt exists.')


#now a form where they put password and put confirm password
class ResetPasswordForm(FlaskForm):
    
    password = PasswordField('Password',
            validators = [DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
            validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')