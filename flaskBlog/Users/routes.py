from flask import Blueprint
from flaskBlog.Users.utils import savePicture, sendResetEmail
from flaskBlog.models import Post, User
from flask import render_template , flash , redirect, request , url_for
from flaskBlog.Users.forms import RegistractionForm , LoginForm , UpdateForm , RequestResetForm , ResetPasswordForm
from flaskBlog import bcrypt , db   
from flask_login import login_user , current_user , logout_user , login_required

users = Blueprint('users' , __name__)

@users.route("/register" , methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistractionForm()
    if form.validate_on_submit():
        hashed_p = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username = form.username.data , email = form.email.data , password = hashed_p)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!' , 'success') #success is a bootstrap class
        return redirect('/login')
    return render_template('register.html' , title='Register' , form=form)

@users.route("/login", methods=['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user)
            #next_page = request.args.get('next')
            flash(f'Logged In for {form.email.data}!' , 'success') 
            return redirect('/')
        else:
            flash(f'Log In Is Unsuccessful. Please check email and password!' , 'danger') 

    return render_template('login.html' , title='Login' , form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash(f'Logedd out  Successfully!' , 'success') 

    return redirect('/')

@users.route("/account", methods=['GET' , 'POST'])
@login_required
def account():
    form = UpdateForm()
    own_posts = Post.query.filter_by(user_id = current_user.id)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = savePicture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated !' , 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static' , filename = 'images/' + current_user.image_file)
    return render_template('account.html' , title='Account' , image_file = image_file , form=form,
                           own_posts=own_posts)


@users.route("/reset_password", methods=['GET' , 'POST'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect('/')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        sendResetEmail(user)
        flash('Email Has Been Sent To Reset The Password!' , 'info')
        return redirect(url_for('users.login'))
    return render_template('resetRequest.html' , title='Reset Password' , 
                            form=form )

@users.route("/reset_password/<token>", methods=['GET' , 'POST'])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect('/')
    user = User.verifyResetToken(token)
    if user is None:
        flash('Invalid Or Expired Token!' , 'warning')
        return redirect({url_for('users.resetRequest')})
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_p = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user.password = hashed_p
        db.session.commit()
        flash('Your Password Has Been Updated' , 'success') #success is a bootstrap class
        return redirect(url_for('users.login'))
    return render_template('resetToken.html' , title='Reset Password' , 
                            form=form )