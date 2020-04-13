from datetime import datetime
from examapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Role Table (1-user,2-lead,3-admin)
class Role(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     rolename = db.Column(db.String(20), unique=True, nullable=False)
     users = db.relationship('User', backref='user_types', lazy=True)

     def __repr__(self):
        return f"Role('{self.rolename}')"


#Group Table
class Group(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     groupname = db.Column(db.String(20), unique=True, nullable=False)
     image_file = db.Column(db.String(20), nullable=False, default='default_group.jpg')
     users = db.relationship('User', backref='team', lazy=True)

     def __repr__(self):
        return f"Group('{self.groupname}','{self.image_file}')"

#User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #personal information
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    secret_word = db.Column(db.String(10), nullable=False)
    #foreign keys
    #linked to Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False,  default=1)
    #linked to Group
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False, default=1)
    #linked to Post
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.secret_word}', '{self.role_id}', '{self.group_id}' )"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"