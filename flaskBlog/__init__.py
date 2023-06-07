from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskBlog.config import Config

#sql instance
db = SQLAlchemy()

#initialse hashing
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login' #login is the function name of our login route
login_manager.login_message_category = 'info' #info is bootstrap class

mail = Mail()

def createApp(config_class=Config):
    #creating an instance of Flask class. __name__ is the name of the module.
    app = Flask(__name__)

    #to use configurations
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from flaskBlog.Users.routes import users
    from flaskBlog.Posts.routes import posts
    from flaskBlog.Main.routes import main
    from flaskBlog.Errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app 