import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # system variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # system variables
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('FLASK_MAIL_USERNAME') # system variables
    MAIL_PASSWORD = os.environ.get('FLASK_MAIL_PASSWORD') # system variables
