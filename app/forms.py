from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[Length(max=100)])
    biography = TextAreaField('Biography')
    profile_photo = FileField('Profile Photo',validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NewPostForm(FlaskForm):
    caption = StringField('Caption', validators=[DataRequired(), Length(max=200)])
    photo = FileField('Photo', validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Create Post')