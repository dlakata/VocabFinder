from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.mail import Mail
from flask.ext.babel import Babel

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)
babel = Babel(app)
db = SQLAlchemy(app)

import vocabfinder.views, vocabfinder.models