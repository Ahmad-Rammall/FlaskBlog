from flask import Blueprint, render_template
from flaskBlog.models import Post

main = Blueprint('main' , __name__)

@main.route("/")
def hello_world():
    posts = Post.query.all()
    return render_template('home.html' , posts=posts)

@main.route("/about")
def hello_world_about():
    return render_template('about.html')