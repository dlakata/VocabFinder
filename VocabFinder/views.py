from VocabFinder import app
from flask import Flask, request, render_template, redirect, url_for
from process_words import *
import os
    
analyzer = TextAnalyzer()
definitions = []
validWords = {'sat': analyzer.sat_words, 'gre': analyzer.gre_words, 'hardest': analyzer.english_words}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/', methods=['POST'])
def getInput():
    bookInput = request.files['book']
    websiteInput = request.form['website']
    textInput = request.form['text']
    difficulty = request.form['difficulty']
    numWords = int(request.form['word_num'])
    valid = validWords[difficulty]
    if bookInput:
        book = bookInput.stream.read()
        print len(book.split('\n'))
        words = analyzer.find_words(book, valid)[:numWords]
    elif websiteInput:
        words = analyzer.find_website_words(websiteInput, valid)[:numWords]
    elif textInput:
        words = analyzer.find_words(textInput.encode('utf-8'), valid)[:numWords]
    defs = [analyzer.dictionary[word] for word in words if word in analyzer.dictionary]
    del definitions[:]
    definitions.extend(zip(words, defs))
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template("results.html", definitions=definitions)
