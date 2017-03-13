from flask_wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
# from app import db

class LoginForm(Form):
	username = TextField('uername', validators=[DataRequired()], render_kw={"placeholder": "Username"})
	password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember_me = BooleanField('remember_me', default=False)

class BlogEditor(Form):
	title = StringField("title", validators=[DataRequired()])
	text = TextAreaField("text", validators=[DataRequired()])
	tags = StringField("tags", validators=[DataRequired()])
	draft = BooleanField("draft", default=False)
	submit = SubmitField("submit")