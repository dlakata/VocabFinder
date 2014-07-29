from flask import Flask
from flask import request
from flask import render_template
import getWords

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results.html')
def results():
    return render_template("results.html", zip="")

@app.route('/', methods=['POST'])
def getData():
    if request.method == 'POST':
        fBook = request.files['book']
        fVocab = request.files['vocab']
        print fVocab, fBook
        text = fBook.stream.read()
        words = fVocab.stream.read()
        book = getWords.Book(text, True)
        vocab = getWords.Vocab(words, True, fVocab.filename)
        intersection = getWords.intersect(vocab, book)
        print intersection
        words, defs = make_html(intersection)
        return render_template("results.html", zip=zip(words, defs))

def make_html(intersection):
    words = []
    defs = []
    intersection = intersection.split('\n')
    intersection.pop(0)
    for line in intersection:
        words.append(line.split()[0])
        defs.append(' '.join(line.split()[2:]))
    return words, defs     

if __name__ == '__main__':
    app.debug = True
    app.run()
