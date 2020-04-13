from examapp import db, bcrypt
from examapp.models import User, Group, Role
#recreate db
db.drop_all()
db.create_all()
#create the roles and 1 group for admins
#roles
role_1 = Role(rolename='Normal User')
role_2 = Role(rolename='Lead User')
role_3 = Role(rolename='Admin User')
db.session.add(role_1)
db.session.add(role_2)
db.session.add(role_3)
#group
group_1 = Group(groupname='New User Group')
group_2 = Group(groupname='Admin Group')
db.session.add(group_1)
db.session.add(group_2)
#create an admin user with hashed password
hashed_password = bcrypt.generate_password_hash('Password1').decode('utf-8')
secret_word = 'Toyota'
#create an admin user
user = User(username='Admin User', email='admin@admin.com', password=hashed_password, secret_word=secret_word, role_id=3, group_id=2)
db.session.add(user)
#applies the changes to the db
db.session.commit()
