"""Handles requests to app"""
from VocabFinder import app, db
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user, \
    login_user, logout_user, login_required, RegisterForm, LoginForm
from flask import request, session, render_template, jsonify, \
    flash, redirect, url_for, g
from models import User, Role
from VocabFinder.process_words import TextAnalyzer

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

analyzer = TextAnalyzer()
valid_words = {
    'sat': analyzer.sat_words,
    'gre': analyzer.gre_words,
    'hardest': analyzer.english_words
}

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

@app.route('/get_context')
def get_context():
    """Returns the word's context"""
    sentence = analyzer.get_sentence(request.args.get('word', '', type=str))
    return jsonify(result=sentence)

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
    num_words = int(request.form['word_num'])
    valid = valid_words[difficulty]
    if difficulty == 'sat':
        difficulty_level = 'SAT words'
    elif difficulty == 'gre':
        difficulty_level = 'GRE words'
    elif difficulty == 'hardest':
        difficulty_level = 'of the hardest English words'
    if book_input:
        source = book_input.filename
        book = book_input.stream.read()
        words = analyzer.find_words(book, valid)
    elif website_input:
        source = website_input
        words = analyzer.find_website_words(website_input, valid)
    elif text_input:
        source = "the given text"
        words = analyzer.find_words(text_input.encode('utf-8'), valid)
    defs = [analyzer.dictionary[word] for word in words[:num_words] if word in analyzer.dictionary]
    return render_template("results.html",
            num_words=num_words,
            difficulty=difficulty_level,
            source=source,
            definitions=zip(words, defs))

@app.errorhandler(404)
def page_not_found(_):
    """Custom 404 error page"""
    return render_template('404.html'), 404

@app.route('/settings')
@login_required
def settings():
    """User customization"""
    return render_template('settings.html')
