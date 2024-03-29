from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5  import DateField, TimeField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from classroom.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max = 20)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered! Contact admin(Nafi, Robin) for password recovery.')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class PostForm(FlaskForm):
    course = StringField('Course Code', validators=[DataRequired()])
    date = DateField('Date of Class Test', format='%Y-%m-%d')
    time = StringField('Time')
    syllabus = StringField('Syllabus', validators=[DataRequired()])
    submit = SubmitField('Post CT')