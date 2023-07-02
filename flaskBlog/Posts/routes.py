from flaskBlog.models import Post
from flask import  abort, render_template , flash , redirect, request , url_for , Blueprint
from flaskBlog.Posts.forms import PostForm 
from flaskBlog import db   
from flask_login import  current_user , login_required

posts = Blueprint('posts' , __name__) # 'posts' is the name

def getOwnPosts():
    if current_user.is_authenticated:
        return Post.query.filter_by(user_id = current_user.id)
    else:
        return ""

@posts.route("/post/new", methods=['GET' , 'POST'])
@login_required
def newPost():
    form = PostForm()
    own_posts = getOwnPosts()

    if form.validate_on_submit():
        post = Post(title=form.title.data , content = form.content.data , author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!' , 'success')
        return redirect('/')
    return render_template('createPost.html' , title='New Post' , form=form , own_posts=own_posts)

@posts.route("/post/<int:post_id>")
def post(post_id):
    #search for the post with the id, if it doesnt exist then return 404 error
    post = Post.query.get_or_404(post_id)
    own_posts = getOwnPosts()

    return render_template('post.html' , title = post.title , post=post , legend='New Post' , own_posts=own_posts) 

@posts.route("/post/<int:post_id>/update", methods=['GET' , 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.author != current_user):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post Has Been Updated!" , 'success')
        return redirect(url_for('posts.post' , post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createPost.html' , title='Update Post' , 
                            form=form , legend='Update Post')



@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect('/')