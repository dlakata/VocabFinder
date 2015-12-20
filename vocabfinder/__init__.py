from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from flask.ext.migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)
babel = Babel(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from vocabfinder.models import User, Role

datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore)

import vocabfinder.views
