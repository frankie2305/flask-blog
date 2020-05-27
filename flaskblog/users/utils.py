import secrets, os
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_thumbnail(form_thumbnail):
    # create path to save image
    random_hex = secrets.token_hex(8)
    base, ext = os.path.splitext(form_thumbnail.filename)
    thumbnail_fn = random_hex + ext
    thumbnail_path = os.path.join(current_app.root_path, 'static/thumbnails', thumbnail_fn)

    # resize image
    output_size = (125, 125)
    image = Image.open(form_thumbnail)
    image.thumbnail(output_size)

    # save image to the path created
    image.save(thumbnail_path)
    return thumbnail_fn

def send_password_reset_email(user):
    token = user.get_reset_token()
    message = Message(subject='Password reset request', recipients=[user.email], sender='justamailbot@gmail.com')
    message.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email.
    '''
    mail.send(message)
