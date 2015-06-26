from flask import Flask, request, render_template
from process_words import *

app = Flask(__name__)
analyzer = TextAnalyzer()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/', methods=['POST'])
def getData():
    if request.method == 'POST':
        bookInput = request.files['book']
        websiteInput = request.form['website']
        if bookInput:
            book = bookInput.stream.read()
            words = analyzer.find_words(book)[:100]
        else:
            words = analyzer.find_website_words(websiteInput)[:100]
        defs = [analyzer.dictionary[word][1] for word in words]
        return render_template("results.html", zip=zip(words, defs))

if __name__ == '__main__':
    app.debug = True
    app.run()