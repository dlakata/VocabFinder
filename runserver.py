"""Starts the app"""
from VocabFinder import app
import os

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
