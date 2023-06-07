from flask_wtf import FlaskForm
#we write python classes instead of html forms

from wtforms import StringField , PasswordField , SubmitField , BooleanField , ValidationError 
from wtforms.validators import DataRequired , Length , Email , EqualTo
from flaskBlog.models import User
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed

class RegistractionForm(FlaskForm):

    username = StringField('Username', 
                           validators=[DataRequired(),Length(min=2 , max=20)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password' , 
                             validators=[DataRequired()])
    
    comfirm_Pass = PasswordField('ComfirmPassword' , 
                                 validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('signUp')

    def validate_username(self , username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken! Please choose a different one')

    def validate_email(self , email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken! Please choose a different one')


class LoginForm(FlaskForm):
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password' , validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('LogIn')

class UpdateForm(FlaskForm):

    username = StringField('Username', 
                           validators=[DataRequired(),Length(min=2 , max=20)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Piture' , validators=[FileAllowed(['jpg' , 'png'])])

    submit = SubmitField('Update')

    def validate_username(self , username):
        user = User.query.filter_by(username=username.data).first()
        if username.data != current_user.username :
            if user :
                raise ValidationError('That username is taken! Please choose a different one')

    def validate_email(self , email):
            user = User.query.filter_by(email=email.data).first()
            if email.data != current_user.email:
                if user :
                    raise ValidationError('That email is taken! Please choose a different one')
                

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self , email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There Is No Account With This Email!')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password' , 
                             validators=[DataRequired()])
    comfirm_Pass = PasswordField('ComfirmPassword' , 
                                 validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')