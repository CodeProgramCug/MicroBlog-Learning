from app import app
from app import db, login_manager
from flask import render_template, flash, redirect, session, url_for, g, request
from models.forms import LoginForm, BlogEditor
from models.models import User, BlogPost
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId

@login_manager.user_loader
def load_user(user_id):
#	return User.query.get(int(id))
	# print user_id
	return User.objects(id=user_id).first()

@app.before_request
def before_request():
	g.user = current_user
	

@app.route('/')
@app.route('/index')
def index():
	user = g.user
	# user = { 'nickname': 'Miguel' } # fake user
	posts = []
	for post in BlogPost.objects:
		print "lalala"
		posts.append( post.to_json() )
	# print posts
	return render_template("index.html",
    			title = 'Home',
				posts = posts)


# Login Handler for the website
@app.route('/login', methods = ['GET', 'POST'])
def login():
	#if g.user is not None and g.user.is_authenticated:
	#	return redirect('/index')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.objects(username=form.username.data, password=form.password.data).first()
		if user:
			session['remember_me'] = form.remember_me.data
			login_user(user)
			return redirect( url_for('index'))
		else:
			flash("lalalal")
	return render_template('login.html' , 
							title = 'Sign In',
							form = form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect( url_for('index') )

@app.route('/test')
@login_required
def test():
	return "yes, you are allowed"

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = BlogEditor()
	postid = request.args.get('postid')
	if postid:
		post = BlogPost.objects.get(id=postid)
	else:
		post = []
	# if post:
		# form.text = post.body
	if form.validate_on_submit():
		if post:
			post.update(title = form.title.data, \
						body=form.text.data, \
						timestamp = datetime.now(), \
				 		tags = form.tags.data)
		else:
			BlogPost(\
		         title = form.title.data ,\
				 body = form.text.data, \
				 timestamp = datetime.now(), \
				 tags = form.tags.data).save()

		post = BlogPost.objects.get(title = form.title.data).to_json()
		user = g.user
		return render_template("blog.html", post=post, user = user)
		
	return render_template("edit.html", form=form, post=post)

@app.route('/blog')
def blog_by_id():
	postid = request.args.get('postid')
	post = BlogPost.objects.get(id=postid).to_json()
	user = g.user
	return render_template("blog.html",post=post, user=user)

@app.route('/delete')
def delete():
	postid = request.args.get('postid')
	post = BlogPost.objects.get(id=postid)
	if post:
		post.delete()
		flash("successfully delete")
	else:
		flash()
	return redirect(url_for("index"))


