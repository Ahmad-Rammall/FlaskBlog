from flaskBlog import db , login_manager 
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask import current_app

@login_manager.user_loader #to let the extension knows that this is the function to get a user by id
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) , unique=True , nullable=False)
    email = db.Column(db.String(100) , unique=True , nullable=False)
    image_file = db.Column(db.String(20) , nullable=False , default='default.png')
    password = db.Column(db.String(60) , nullable=False)
    posts = db.relationship('Post' , backref='author' , lazy=True)#lazy=true means that sql will load data in one go

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.image_file}')"

    def getResetToken(self , expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'] , expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verifyResetToken(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

        
class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(50) , nullable=False)
    date_posted = db.Column(db.DateTime , nullable = False , default = datetime.utcnow)
    content = db.Column(db.Text , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False)#user table

    def __repr__(self):
        return f"Post('{self.title}' , '{self.date_posted}')"

# with current_app.root_path.app_context():
#     db.create_all()