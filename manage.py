"""Starts the app"""
from vocabfinder import app
from flask.ext.script import Server, Manager
from flask.ext.migrate import MigrateCommand
import os

server = Server(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

manager = Manager(app)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
