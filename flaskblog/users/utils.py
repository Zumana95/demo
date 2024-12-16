import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import db, mail  # Import db and mail but not app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(form_picture):
    """Save the uploaded picture and return the filename."""
    if not allowed_file(form_picture.filename):
        raise ValueError("File type not allowed.")

    random_hex = secrets.token_hex(8)  # Generate a random filename
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  # Create a unique filename
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # Use current_app

    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (125, 125)  # Resize dimensions
    try:
        i = Image.open(form_picture)
        i.thumbnail(output_size)  # Resize the image
        i.save(picture_path)  # Save the image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

    return picture_fn  # Return the filename

def send_reset_email(user):
    """Send a password reset email to the user."""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='zumana1995@gmail.com',
                  recipients=[user.email])

    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''

    try:
        mail.send(msg)  # Attempt to send the email
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
