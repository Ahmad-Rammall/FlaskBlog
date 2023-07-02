from flask import Blueprint, render_template
from flask_login import current_user
from flaskBlog.models import Post 


main = Blueprint('main' , __name__)

@main.route("/")
def hello_world():
    posts = Post.query.all()
    if current_user.is_authenticated:
        own_posts = Post.query.filter_by(user_id = current_user.id)
    else:
        own_posts = {}
    return render_template('home.html' , posts=posts , own_posts=own_posts)

@main.route("/about")
def hello_world_about():
    if current_user.is_authenticated:
        own_posts = Post.query.filter_by(user_id = current_user.id)
    else:
        own_posts = {}    
    return render_template('about.html' , own_posts=own_posts)