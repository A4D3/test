from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm( FlaskForm ):
    name = StringField('Name:', validators=[InputRequired(), Length(min=1, max=15)])
    surname = StringField('Surname:', validators=[InputRequired(), Length(min=1, max=15)])
    birth = StringField('Birth:', validators=[InputRequired(), Length(min=10, max=10)])
    username = StringField('Username:', validators=[InputRequired(), Length(min=5,max=20)])
    password = PasswordField('Password:', validators=[InputRequired() ,Length(min=1, max=20)])
    passwordVerification = PasswordField('Password:', validators=[InputRequired(), Length(min=1, max=20)])
    submit = SubmitField('Send')

class MyLoginForm( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5,max=20)])
    password = PasswordField('Password:', validators=[Length(min=1, max=20)])
    submit = SubmitField('Send')

class TaskForm( FlaskForm ):
    name = StringField('Name:', validators=[InputRequired(), Length(min=1, max=15)])
    description = StringField('Description:')
    deadline = StringField('Deadline:', validators=[InputRequired(), Length(min=10, max=10)])
    submit = SubmitField('Send')
