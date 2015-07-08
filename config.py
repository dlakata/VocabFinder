import os

DEBUG = True
SECRET_KEY = 'zhayYxXXUPuNh09ZDsNGLcDRIWywVUC6XCH1sZI2'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = False
SECURITY_PASSWORD_SALT = 'b64f49553d5c441652e95697a2c5949e'
SECURITY_PASSWORD_HASH = 'bcrypt'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'davidlakata@gmail.com'
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')