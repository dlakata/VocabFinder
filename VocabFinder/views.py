"""Handles requests to app"""
from VocabFinder import app, db
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user, \
    login_user, logout_user, login_required, RegisterForm, LoginForm
from flask import request, session, render_template, jsonify, \
    flash, redirect, url_for, g
from models import User, Role, VocabSet
from VocabFinder.process_words import TextAnalyzer
from datetime import datetime
from functools import wraps
from urlparse import urlparse

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

analyzer = TextAnalyzer()
valid_words = {
    'sat': analyzer.sat_words,
    'gre': analyzer.gre_words,
    'hardest': analyzer.english_words
}
difficulty_text = {
    'sat' : 'SAT words',
    'gre' : 'GRE words',
    'hardest' : 'of the hardest English words'
}

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id = request.args.get('id', 0, type=int)
        vocab_set = VocabSet.query.get(id)
        if vocab_set is None:
            flash("Sorry, that vocab set couldn't be found")
            return redirect(url_for('index'))
        if g.user.is_anonymous() or g.user.id != vocab_set.user_id:
            flash("Sorry, only the vocab set's owner can do that")
            return redirect(url_for('login', next=request.url))
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

@app.route('/login')
def login(*args, **kwargs):
    """Wrapper for Flask-Security's login route"""
    flask.ext.login(*args, **kwargs)

@app.route('/about')
def about():
    """Shows about page"""
    return render_template("about.html")

@app.route('/change_visibility')
@owner_required
def change_visibility():
    """Toggles a vocab set's visibility"""
    id = request.args.get('id', 0, type=int)
    vocab_set = VocabSet.query.get(id)
    vocab_set.public = not vocab_set.public
    db.session.commit()
    return ""

@app.route('/change_difficulty')
@owner_required
def change_difficulty():
    """Changes a vocab set's difficulty"""
    id = request.args.get('id', 0, type=int)
    difficulty = request.args.get('difficulty', 'hardest', type=str)
    vocab_set = VocabSet.query.get(id)
    vocab_set.difficulty = difficulty
    db.session.commit()
    return ""

@app.route('/change_num_words')
@owner_required
def change_num_words():
    """Changes a vocab set's word count"""
    id = request.args.get('id', 0, type=int)
    num_words = request.args.get('num_words', 100, type=int)
    vocab_set = VocabSet.query.get(id)
    vocab_set.num_words = num_words
    db.session.commit()
    return ""

@app.route('/delete_vocab_set')
@owner_required
def delete_vocab_set():
    """Deletes a vocab set"""
    id = request.args.get('id', 0, type=int)
    vocab_set = VocabSet.query.get(id)
    db.session.delete(vocab_set)
    db.session.commit()
    return ""

@app.route('/get_context')
def get_context():
    """Returns the word's context"""
    sentence = analyzer.get_sentence(request.args.get('word', '', type=str))
    return jsonify(result=sentence)

@app.route('/saved_set/<int:id>')
def saved_set(id):
    """Displays a saved vocab set"""
    vocab_set = VocabSet.query.get(id)
    if vocab_set is None:
        flash("Sorry, that vocab set couldn't be found")
        return redirect(url_for('login', next=request.url))
    if (g.user.is_anonymous() or g.user.id != vocab_set.user_id) and not vocab_set.public:
        flash("Sorry, the owner hasn't made that vocab set publicly available")
        return redirect(url_for('login', next=request.url))
    difficulty = vocab_set.difficulty
    num_words = vocab_set.num_words
    valid = valid_words[difficulty]
    difficulty_level = difficulty_text[difficulty]
    words = analyzer.find_words(vocab_set.text.encode('utf-8'), valid)
    defs = [analyzer.dictionary[word] for word in words[:num_words] if word in analyzer.dictionary]
    definitions = zip(words, defs)
    return render_template("results.html",
            vocab_set=vocab_set,
            num_words=num_words,
            difficulty=difficulty_level,
            source=vocab_set.source,
            definitions=definitions)

@app.route('/saved_set/<int:id>/text')
def saved_set_text(id):
    """Displays a saved vocab set"""
    vocab_set = VocabSet.query.get(id)
    if vocab_set is None:
        flash("Sorry, that vocab set couldn't be found")
        return redirect(url_for('login', next=request.url))
    if (g.user.is_anonymous() or g.user.id != vocab_set.user_id) and not vocab_set.public:
        flash("Sorry, the owner hasn't made that vocab set publicly available")
        return redirect(url_for('login', next=request.url))
    source = vocab_set.source
    if "http" in source:
        return redirect(source)
    text = vocab_set.text.encode('utf-8')
    return text

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
            words = analyzer.find_words(book, valid)
        else:
            flash("Please upload a .txt file")
            return redirect(url_for('index'))
    elif website_input:
        if not validate_url(website_input):
            flash("Please enter a valid, http-prefixed URL.")
            return redirect(url_for('index'))
        source = website_input
        words = analyzer.find_website_words(website_input, valid)
    elif text_input:
        source = "user input"
        words = analyzer.find_words(text_input.encode('utf-8'), valid)
    else:
        flash("You need to provide some input.")
        return redirect(url_for('index'))
    defs = [analyzer.dictionary[word] for word in words[:num_words] if word in analyzer.dictionary]
    definitions = zip(words, defs)
    if g.user.is_authenticated():
        vocab_set = VocabSet(source=source)
        vocab_set.text = analyzer.text
        vocab_set.difficulty = difficulty
        vocab_set.num_words = num_words
        vocab_set.public = False
        vocab_set.timestamp = datetime.now()
        vocab_set.user = g.user
        db.session.add(vocab_set)
        db.session.commit()
    return render_template("results.html",
            num_words=num_words,
            difficulty=difficulty_level,
            source=source,
            definitions=definitions)

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
    parse = urlparse(url)
    if not parse.scheme:
        return False
    if len(parse.netloc.split('.')) == 1:
        return False
    return True
