"""Handles requests to app"""
from vocabfinder import app, db, datastore
from flask.ext.security import current_user, \
    login_user, logout_user, login_required, RegisterForm, LoginForm
from flask import request, session, render_template, jsonify, \
    flash, redirect, url_for, g
from models import User, Role, VocabSet
from vocabfinder.process_words import TextAnalyzer, valid_words, difficulty_text
from datetime import datetime
from functools import wraps
from urlparse import urlparse
from urllib import urlopen
import json

api_key = "&api_key=" + app.config['WORDNIK_API_KEY']
base_url = "http://api.wordnik.com/v4/word.json/"

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id = request.args.get('id', 0, type=int)
        vocab_set = VocabSet.query.get(id)
        if not vocab_set:
            flash("Sorry, that vocab set couldn't be found")
            return redirect(url_for('index'))
        if g.user.is_anonymous() or g.user.id != vocab_set.user_id:
            flash("Sorry, only the vocab set's owner can do that")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    """Sets global current_user"""
    g.user = current_user

@app.route('/')
def index():
    """Shows index"""
    return render_template("index.html")

@app.route('/about')
def about():
    """Shows about page"""
    return render_template("about.html")

@app.route('/account')
@login_required
def account():
    """Shows user's account"""
    return render_template("security/account.html")

@app.route('/change_visibility')
@owner_required
def change_visibility():
    """Toggles a vocab set's visibility"""
    id = request.args.get('id', 0, type=int)
    vocab_set = VocabSet.query.get(id)
    vocab_set.public = not vocab_set.public
    datastore.commit()
    return ""

@app.route('/change_difficulty')
@owner_required
def change_difficulty():
    """Changes a vocab set's difficulty"""
    id = request.args.get('id', 0, type=int)
    difficulty = request.args.get('difficulty', 'hardest', type=str)
    vocab_set = VocabSet.query.get(id)
    vocab_set.difficulty = difficulty
    datastore.commit()
    return ""

@app.route('/change_num_words')
@owner_required
def change_num_words():
    """Changes a vocab set's word count"""
    id = request.args.get('id', 0, type=int)
    num_words = request.args.get('num_words', 100, type=int)
    vocab_set = VocabSet.query.get(id)
    vocab_set.num_words = num_words
    datastore.commit()
    return ""

@app.route('/delete_vocab_set')
@owner_required
def delete_vocab_set():
    """Deletes a vocab set"""
    id = request.args.get('id', 0, type=int)
    vocab_set = VocabSet.query.get(id)
    datastore.delete(vocab_set)
    datastore.commit()
    return ""

@app.route('/get_definitions')
def get_definitions():
    """Returns the word's definitions"""
    word = request.args.get('word', '', type=str)
    url = urlopen(base_url + word + "/definitions?limit=200&sourceDictionaries=all&useCanonical=false&includeTags=false" + api_key)
    return url.read()

@app.route('/get_etymology')
def get_etymology():
    """Returns the word's etymology"""
    word = request.args.get('word', '', type=str)
    url = urlopen(base_url + word + "/etymologies?useCanonical=true" + api_key)
    return url.read()

@app.route('/get_pronunciation')
def get_pronunciation():
    """Returns the word's pronunciation"""
    word = request.args.get('word', '', type=str)
    url = urlopen(base_url + word + "/audio?useCanonical=false&limit=50" + api_key)
    return url.read()

@app.route('/saved_set/<int:id>')
def saved_set(id):
    """Displays a saved vocab set"""
    vocab_set = VocabSet.query.get(id)
    if not vocab_set:
        flash("Sorry, that vocab set couldn't be found")
        return redirect(url_for('index'))
    if (g.user.is_anonymous() or g.user.id != vocab_set.user_id) and not vocab_set.public:
        flash("Sorry, the owner hasn't made that vocab set publicly available")
        return redirect(url_for('index'))
    return render_vocab_set(vocab_set)

@app.route('/saved_set/<int:id>/text')
def saved_set_text(id):
    """Displays a saved vocab set"""
    vocab_set = VocabSet.query.get(id)
    if not vocab_set:
        flash("Sorry, that vocab set couldn't be found")
        return redirect(url_for('index'))
    if (g.user.is_anonymous() or g.user.id != vocab_set.user_id) and not vocab_set.public:
        flash("Sorry, the owner hasn't made that vocab set publicly available")
        return redirect(url_for('index'))
    source = vocab_set.source
    if "http" in source:
        return redirect(source)
    return vocab_set.text

@app.route('/results')
def results_no_data():
    """Shows blank results page"""
    return render_template("results.html")

@app.route('/results', methods=['POST'])
def results():
    """Processes source and returns definitions"""
    book_input = request.files['book']
    website_input = request.form['website']
    text_input = request.form['text']
    difficulty = request.form['difficulty']
    num_input = request.form['word_num']
    if num_input and num_input.isdigit():
        num_words = int(num_input)
    else:
        num_words = 100
    valid = valid_words[difficulty]
    difficulty_level = difficulty_text[difficulty]
    if book_input:
        source = book_input.filename
        if '.' in source and source.rsplit('.', 1)[1] in 'txt':
            book = book_input.stream.read()
            text = TextAnalyzer.clean_text(book)
            words = TextAnalyzer.find_words(text, valid)
        else:
            flash("Please upload a .txt file")
            return redirect(url_for('index'))
    elif website_input:
        if not validate_url(website_input):
            flash("Please enter a valid, http-prefixed URL.")
            return redirect(url_for('index'))
        source = website_input
        text = TextAnalyzer.clean_website_text(source)
        words = TextAnalyzer.find_words(text, valid)
    elif text_input:
        source = "user input"
        text = text_input
        words = TextAnalyzer.find_words(text_input, valid)
    else:
        flash("You need to provide some input.")
        return redirect(url_for('index'))
    words = words[:num_words]
    defs = [TextAnalyzer.define(word) for word in words]
    word_data = zip(words, defs)
    vocab_set = VocabSet()
    vocab_set.source = source
    vocab_set.text = text
    vocab_set.difficulty = difficulty
    vocab_set.num_words = num_words
    vocab_set.user = g.user
    if g.user.is_authenticated():
        datastore.put(vocab_set)
        datastore.commit()
    return render_vocab_set(vocab_set)

def render_vocab_set(vocab_set):
    difficulty = vocab_set.difficulty
    num_words = vocab_set.num_words
    valid = valid_words[difficulty]
    difficulty_level = difficulty_text[difficulty]
    words = TextAnalyzer.find_words(vocab_set.text, valid)[:num_words]
    defs = [TextAnalyzer.define(word) for word in words]
    word_data = zip(words, defs)
    return render_template("results.html",
            num_words=num_words,
            difficulty=difficulty_level,
            source=vocab_set.source,
            words=word_data)

@app.errorhandler(404)
def page_not_found(_):
    """Custom 404 error page"""
    return render_template('404.html'), 404

@app.errorhandler(Exception)
@app.errorhandler(500)
def internal_error(_):
    """Custom 500 error page"""
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/saved_lists')
@login_required
def saved_lists():
    """User customization"""
    return render_template('saved_lists.html')

def validate_url(url):
    """Confirm that url is valid"""
    parse = urlparse(url)
    return parse.scheme and len(parse.netloc.split('.')) != 1

