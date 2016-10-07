from app import app
from app import db, lm, oid
from flask import render_template, flash, redirect, session, url_for, g
from .forms import LoginForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	g.user = current_user
	

@app.route('/')
@app.route('/index')
def index():
	user = g.user;
	# user = { 'nickname': 'Miguel' } # fake user
	posts = [
       	    {
			    'author' : { 'nickname' : 'John'},
				'body'   : 'Beautiful day in Newyork'
			},
			{
			    'author' : { 'nickname' : 'Susan'},
				'body'   : 'The Avengers movie was so cool!'
			}
			]
	return render_template("index.html",
    			title = 'Home',
			    user = user,
				posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect('/index')
	form = LoginForm()
	if form.validate_on_submit():
		# flash('"Login requested for OpenId = "' + form.openid.data + str(form.remember_me.data))
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['username', 'password'])
	return render_template('login.html' , 
							title = 'Sign In',
							form = form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect( url_for('index') )


@oid.after_login
def after_login(resp):
	if resp.username is None or resp.username == "":
		flash('Invalid Login, Please try again.')
		return redirect( url_for('login') )
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		flash('Invalid Login, Please try again.')
		return redirect( url_for('login') )
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me);
	return redirect(request.args.get('next') or url_for('index'))
