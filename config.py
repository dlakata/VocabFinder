import os

DEBUG = True
SECRET_KEY = 'zhayYxXXUPuNh09ZDsNGLcDRIWywVUC6XCH1sZI2'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')

SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = True
SECURITY_PASSWORD_SALT = 'b64f49553d5c441652e95697a2c5949e'
SECURITY_PASSWORD_HASH = 'bcrypt'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = "Your password for VocabFinder has been changed"
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = "Your password for VocabFinder has been reset"
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = "Password reset instructions for VocabFinder"

WORDNIK_API_KEY = os.getenv('WORDNIK_API_KEY', '')