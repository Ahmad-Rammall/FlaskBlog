import os

class Config:
    #secret key for protection + create database instance inside bash_profile
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


    # MAIL_USERNAME = 'rammalahmad20@gmail.com'
    # MAIL_PASSWORD = 'opogmeywsbjvzumf'