from flask import Flask
from flask import request
from flask import render_template
import getWords

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/', methods=['POST'])
def getData():
    if request.method == 'POST':
        fBook = request.files['book']
        fVocab = request.files['vocab']
        if not fVocab:
            words = 'wordLists/freq_all.num'
            vocab = getWords.Vocab(words, False)
        else:
            words = fVocab.stream.read()
            vocab = getWords.Vocab(words, True, fVocab.filename)
        text = fBook.stream.read()
        book = getWords.Book(text, True)
        intersection, context = getWords.intersect(vocab, book)
        context = context.split('\n')
        context.pop(0)
        words, defs = make_html(intersection)
        return render_template("results.html", zip=zip(words, defs, context, range(len(words))))

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
