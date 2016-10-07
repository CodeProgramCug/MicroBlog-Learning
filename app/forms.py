from flask_wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField
from wtforms.validators import DataRequired
# from app import db

class LoginForm(Form):
	username = TextField('uername', validators=[DataRequired()], render_kw={"placeholder": "Username"})
	password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember_me = BooleanField('remember_me', default=False)