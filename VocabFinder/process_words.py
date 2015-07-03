""" Finds words common to vocabulary list and text """
import sys, urllib2, unicodedata, codecs
from datetime import datetime
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from cookielib import CookieJar

class TextAnalyzer(object):

    def __init__(self):
        nltk.data.path.append('nltk_data')
        self.prep_dictionary()
        self.lemmatize = prep_wordnet()
        self.english_words = set(self.dictionary.keys())
        self.trans_table = get_trans_table()

    def find_words(self, text, validWords):
        clean_text = codecs.decode(text, 'unicode_escape').translate(self.trans_table)
        words = { word.strip().lower() for word in clean_text.split(' ') if len(word) > 3 }
        lemmatized_words = map(self.lemmatize, words)
        found = validWords & set(lemmatized_words)
        return sorted(found, key=lambda word: self.frequencies.get(word, 10000000))

    def find_website_words(self, url, validWords):
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = urllib2.Request(url)
        response = opener.open(request)
        html = response.read()
        response.close()
        text = BeautifulSoup(html).get_text()
        return self.find_words(text.encode('utf-8'), validWords)

    def print_words(self, found, number):
        for i in xrange(number):
            word = found[i]
            print word, self.dictionary[word]

    def prep_dictionary(self):
        self.dictionary = dict()
        self.frequencies = dict()
        with open('words_freqs_defs.txt', 'r') as english_dict:
            data = english_dict.readlines()
        for line in data:
            word, freq, dfn = line.decode('utf-8').split('\t')
            self.dictionary[word] = dfn
            self.frequencies[word] = int(freq)
        with open('sat_words.txt', 'r') as sat_dict:
            self.sat_words = { word.replace('\n', '').decode('utf-8') for word in sat_dict.readlines() }
        with open('gre_words.txt', 'r') as gre_dict:
            self.gre_words = { word.replace('\n', '').decode('utf-8') for word in gre_dict.readlines() }

def prep_wordnet():
    lemma = WordNetLemmatizer()
    wordnet.synsets(lemma.lemmatize('hello'))
    return lemma.lemmatize

def get_trans_table():
    letters = [i for i in xrange(sys.maxunicode) if not unicodedata.category(unichr(i)).startswith('L')]
    return dict.fromkeys(letters, u' ')

def main():
    """ Main function """
    with open(sys.argv[1], 'r') as book_file:
        book = book_file.read()
    analyzer = TextAnalyzer()
    a = datetime.now()
    found = analyzer.find_words(book, analyzer.english_words)
    print datetime.now() - a

if __name__ == "__main__":
    main()
