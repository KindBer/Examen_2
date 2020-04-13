from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from examapp.models import User, Role, Group

#neccesary
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	selected_question = SelectField('Secret Question', choices=[('1','What is your favorite car?'),
		('2','What was the name of your first pet?'),('3','Where is the place of your birth?'),], default='1')
	secret_word = StringField('Answer', validators=[DataRequired(), Length(min=2,max=10)])
	submit = SubmitField('Sign Up')
	#validate user
	def validate_username(self, username):
		#call user
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken, choose a different one!')
	def validate_email(self, email):
		#call user
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken, choose a different one!')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators= [FileAllowed(['jpg','png'])])
	secret_word = StringField('Secret Word', validators=[DataRequired(), Length(min=2,max=10)])
	submit = SubmitField('Update')
	#validate user
	def validate_username(self, username):
		#call user
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken, choose a different one!')
	def validate_email(self, email):
		#call user
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken, choose a different one!')

		
class RegistrationForm_AdminAccess(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	selected_question = SelectField('Secret Question', choices=[('1','What is your favorite car?'),
		('2','What was the name of your first pet?'),('3','Where is the place of your birth?'),], default='1')
	secret_word = StringField('Answer', validators=[DataRequired(), Length(min=2,max=10)])
	group= QuerySelectField(query_factory=lambda:Group.query.all(),get_label="groupname")
	role = QuerySelectField(query_factory=lambda:Role.query.all(),get_label="rolename")
	submit = SubmitField('Create New')
	#validate user
	def validate_username(self, username):
		#call user
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken, choose a different one!')
	def validate_email(self, email):
		#call user
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken, choose a different one!')

class Group_Form(FlaskForm):
	group = StringField('Groupname', validators=[DataRequired(), Length(min=2,max=20)])
	submit = SubmitField('Create New')

class UpdateUserForm_AdminAccess(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	group= QuerySelectField(query_factory=lambda:Group.query.all(),get_label="groupname")
	role = QuerySelectField(query_factory=lambda:Role.query.all(),get_label="rolename")
	submit = SubmitField('Update User')
	#validate user
	def validate_username(self, username):
		#call user
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken, choose a different one!')
	def validate_email(self, email):
		#call user
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken, choose a different one!')

class Update_Group_Form(FlaskForm):
	group = StringField('Groupname', validators=[DataRequired(), Length(min=2,max=20)])
	picture = FileField('Update Profile Picture', validators= [FileAllowed(['jpg','png'])])
	submit = SubmitField('Update Team')







#no need
class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')