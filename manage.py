"""Starts the app"""
from VocabFinder import app, db
from flask.ext.script import Server, Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail
import os

migrate = Migrate(app, db)
mail = Mail(app)
server = Server(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

manager = Manager(app)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
