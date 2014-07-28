from flask import Flask
from flask import request
from flask import render_template
import getWords

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
        fBook = request.files['book']
        fVocab = request.files['vocab']
        text = fBook.stream.read()
        words = fVocab.stream.read()
        book = getWords.Book(text, True)
        vocab = getWords.Vocab(words, True, fVocab.filename)
        intersection = getWords.intersect(vocab, book)
        pretty = make_html(intersection)
        return render_template("results.html", results=pretty)

def make_html(intersection):
    return intersection.split('\n')

if __name__ == '__main__':
    app.debug = True
    app.run()
