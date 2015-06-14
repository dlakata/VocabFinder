from flask import Flask, request, render_template
from process_words import *

app = Flask(__name__)
lemma = prep_wordnet()
dictionary = create_dictionary()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/', methods=['POST'])
def getData():
    if request.method == 'POST':
        book = request.files['book'].stream.read()
        words = process_book(lemma, dictionary, book)[:100]
        defs = [dictionary[word][1] for word in words]
        return render_template("results.html", zip=zip(words, defs))

if __name__ == '__main__':
    app.debug = True
    app.run()
