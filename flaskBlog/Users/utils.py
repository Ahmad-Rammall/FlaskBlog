from flask import current_app, url_for
from PIL import Image
from flask_mail import Message
import secrets,os
from flaskBlog import mail


def savePicture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name , f_ext = os.path.splitext(form_picture.filename) 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path , 'static/images' , picture_fn)
    output_size = (125 , 125)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)
    return picture_fn

def sendResetEmail(user):
    token = user.getResetToken()
    msg = Message('Password Reset Request' , sender='rammalahmad20@gmail.com' , recipients=[user.email])
    msg.body = f'''
        To reset your password , follow the following link :
        {url_for('users.resetToken' , token=token , _external=True)}
        If you did not make this request , simply ignore this email and no changes will be made
    '''
    mail.send(msg)
#_external = true --> to get an absolute URL rather than a relative URL


