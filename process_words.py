""" Finds words common to vocabulary list and text """
import sys, urllib2, unicodedata
from datetime import datetime
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

class TextAnalyzer(object):

    def __init__(self):
        self.lemmatize = prep_wordnet()
        self.dictionary = create_dictionary()
        self.valid_words = set(self.dictionary.keys())
        self.trans_table = dict.fromkeys((i for i in xrange(sys.maxunicode) if not unicodedata.category(unichr(i)).startswith('L')), u' ')

    def find_words(self, text):
        clean_text = text.decode('utf-8').translate(self.trans_table)
        words = { word.strip().lower() for word in clean_text.split(' ') }
        lemmatized_words = map(self.lemmatize, words)
        found = self.valid_words & set(lemmatized_words)
        return sorted(found, key=lambda word: self.dictionary[word][0])

    def find_website_words(self, website):
        response = urllib2.urlopen(website)
        html = response.read()
        response.close()
        text = BeautifulSoup(html).get_text()
        return self.find_words(text.encode('utf-8'))

    def print_words(self, found, number):
        for i in xrange(number):
            word = found[i]
            print word, self.dictionary[word][1]

def prep_wordnet():
    lemma = WordNetLemmatizer()
    wordnet.synsets(lemma.lemmatize('hello'))
    return lemma.lemmatize

def create_dictionary():
    dictionary = dict()
    new_file = open('words_freqs_defs.txt', 'r')
    data = new_file.readlines()
    new_file.close()
    for line in data:
        word, freq, dfn = line.decode('utf-8').split('\t')
        dictionary[word] = int(freq), dfn
    return dictionary

def main():
    """ Main function """
    book_file = open(sys.argv[1], 'r')
    book = book_file.read()
    book_file.close()
    analyzer = TextAnalyzer()
    a = datetime.now()
    found = analyzer.find_words(book)
    print datetime.now() - a

if __name__ == "__main__":
    main()
