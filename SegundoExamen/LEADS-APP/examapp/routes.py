import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from examapp import app, db, bcrypt
from examapp.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RegistrationForm_AdminAccess, 
							UpdateUserForm_AdminAccess, Group_Form, Update_Group_Form)
from examapp.models import User, Post, Group, Role
from flask_login import login_user, current_user, logout_user, login_required   

#-------------------Starting App's Routes-------------------------
#HomePage
@app.route("/")
@app.route("/home")
def Home():
	return render_template('home.html')

#About Page
@app.route("/about")
def About():
	return render_template('about.html', title ='About')
#-------------------End of Starting App's Routes-------------------------

#-------------------Basic App's Routes-------------------------
@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('Home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		#encrypt the password
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, secret_word=form.secret_word.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Your Account has been  created succesfully!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('Home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			#if exists redirects Home
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('Home'))
		else:
			flash('Login Unsuccessful. Please check Email and Password',  'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('Home'))

def save_picture(form_picture):
	#build the route and ext of the img
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	#reduce size of profile picture
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.secret_word = form.secret_word.data
		db.session.commit()
		flash('Your account has been updated','success')
		redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.secret_word.data = current_user.secret_word
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)
#-------------------END of Basic App's Routes-------------------------

#-------------------USER CRUD Routes- Admin Access------------------------------
#Show All Users
@app.route("/users")
@login_required
def Users():
	if current_user.role_id == 3:
		users = User.query.all()
	if current_user.role_id == 2:
		users = User.query.filter_by(group_id=current_user.group_id).all()	
	return render_template('users.html', title ='Users', users=users)

#Show All Teams
@app.route("/teams")
@login_required
def Groups():
	if current_user.role_id == 3:
		groups = Group.query.all()
	if current_user.role_id == 2:
		groups = Group.query.all()
	return render_template('teams.html', title ='Groups', groups=groups)

#Show All Leads
@app.route("/roles")
@login_required
def Roles():
	if current_user.role_id == 3:
		roles = Role.query.all()
	if current_user.role_id == 2:	
		roles = Role.query.all()	
	return render_template('roles.html', title ='Roles', roles=roles)

#Creates a new user
@app.route("/users/new", methods=['GET','POST'])
@login_required
def register_loggedin():
	form = RegistrationForm_AdminAccess()
	if form.validate_on_submit():
		#encrypt the password
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, secret_word=form.secret_word.data,role_id=(request.form['role']), group_id=(request.form['group']))
		db.session.add(user)
		db.session.commit()
		flash(f'The account has been created succesfully!', 'success')
		return redirect(url_for('Home'))
	return render_template('create_user.html', legend='New User', form=form)

#Creates a new team
@app.route("/teams/new", methods=['GET','POST'])
@login_required
def group_loggedin():
	form = Group_Form()
	if form.validate_on_submit():
		group = Group(groupname=form.group.data)
		db.session.add(group)
		db.session.commit()
		flash(f'The team has been created succesfully!', 'success')
		return redirect(url_for('Home'))
	return render_template('create_team.html', legend='New Team', form=form)

#open directly an user
@app.route("/users/<int:user_id>") #expects and int as id
@login_required
def get_user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user.html', title=user.username, user=user)

#open directly an team
@app.route("/teams/<int:group_id>") #expects and int as id
@login_required
def get_group(group_id):
	group = Group.query.get_or_404(group_id)
	return render_template('team.html', title=group.groupname, group=group)

	
#update an user
@app.route("/users/<int:user_id>/update", methods = ['GET','POST']) #expects and int as id
@login_required
def update_user(user_id):
	user = User.query.get_or_404(user_id)
	if current_user.role_id != 3:
		abort(403) #return a error if user is not the current user
	form = UpdateUserForm_AdminAccess()
	if form.validate_on_submit(): #update an existing post to the db
		user.username = form.username.data
		user.email = form.email.data
		user.role_id = request.form['role']
		user.group_id = request.form['group']
		db.session.commit()
		flash('The user has been updated!', 'success')
		return redirect(url_for('Users', user_id=user.id))
	elif request.method == 'GET': #populate the textboxes
		form.username.data = user.username
		form.email.data = user.email
	return render_template('update_user.html', title='Update User', form=form, legend='Update User')

#update an team
@app.route("/teams/<int:group_id>/update", methods = ['GET','POST']) #expects and int as id
@login_required
def update_group(group_id):
	group = Group.query.get_or_404(group_id)
	if current_user.role_id != 3:
		abort(403) #return a error if user is not the current user
	form = Update_Group_Form()
	if form.validate_on_submit(): #update an existing post to the db
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			group.image_file = picture_file
			#current_user.image_file = picture_file
		group.groupname = form.group.data
		db.session.commit()
		flash('The team has been updated!', 'success')
		return redirect(url_for('Groups', group_id=group.id))
	elif request.method == 'GET': #populate the textboxes
		form.group.data = group.groupname
	image_file = url_for('static', filename='profile_pics/' + group.image_file)
	#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('update_team.html', title='Update Team', form=form, legend='Update Team')

#delete an user
@app.route("/users/<int:user_id>/delete", methods = ['POST']) #expects and int as id
@login_required
def delete_user(user_id):
	user = User.query.get_or_404(user_id)
	if current_user.role_id != 3:
		abort(403) #return a error if user is not the current user
	db.session.delete(user)
	db.session.commit()
	flash('The user has been deleted!', 'success')
	return redirect(url_for('Users'))	

#delete an team
@app.route("/teams/<int:group_id>/delete", methods = ['POST']) #expects and int as id
@login_required
def delete_group(group_id):
	group = Group.query.get_or_404(group_id)
	if current_user.role_id != 3:
		abort(403) #return a error if user is not the current user
	db.session.delete(group)
	db.session.commit()
	flash('The team has been deleted!', 'success')
	return redirect(url_for('Groups'))	


##----------------------end of USER CRUD------------------------------------







#no need / modificate
#new insert
@app.route("/post/new", methods = ['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit(): #add the post to the db
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit() #--------
		flash('Your post have been created!','success')
		return redirect(url_for('Home'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')

#open directly an id
@app.route("/post/<int:post_id>") #expects and int as id
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

#update an id
@app.route("/post/<int:post_id>/update", methods = ['GET','POST']) #expects and int as id
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403) #return a error if user is not the current user
	form = PostForm()
	if form.validate_on_submit(): #update an existing post to the db
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET': #populate the textboxes
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#delete an id
@app.route("/post/<int:post_id>/delete", methods = ['POST']) #expects and int as id
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403) #return a error if user is not the current user
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('Home'))