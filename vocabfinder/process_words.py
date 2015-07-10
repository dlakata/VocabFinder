"""Finds the frequencies of all the words in a given text"""
import sys, urllib2, unicodedata, codecs, nltk.data, re
from datetime import datetime
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup, Doctype
from cookielib import CookieJar

class TextAnalyzer(object):
    """An object that holds a list of valid words and their frequencies"""

    def __init__(self):
        nltk.data.path.append('nltk_data')
        self.prep_dictionary()
        self.lemmatize = prep_wordnet()
        self.english_words = set(self.dictionary.keys())
        self.trans_table = get_trans_table()

    def find_words(self, text, valid_words):
        """Cleans given text and compares the lemmatized text to a list of valid words"""
        self.text = codecs.decode(text, 'unicode_escape')
        clean_text = self.text.translate(self.trans_table)
        words = {word.strip().lower() for word in clean_text.split(' ') if len(word) > 3}
        lemmatized_words = map(self.lemmatize, words)
        found = valid_words & set(lemmatized_words)
        return sorted(found, key=lambda word: self.frequencies.get(word, 10000000))

    def find_website_words(self, url, valid_words):
        """Wrapper for find_words to get a website's text"""
        cookie_jar = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        request = urllib2.Request(url)
        response = opener.open(request)
        html = response.read()
        response.close()
        soup = BeautifulSoup(re.sub(r'<!--.*-->', '', str(html)))
        for element in soup.select('[style~="display:none"]'):
            element.extract()
        text = ''.join(filter(self.visible_html_entities, soup.findAll(text=True)))
        return self.find_words(text.encode('utf-8'), valid_words)

    def visible_html_entities(self, element):
        """Filters html tags that aren't part of the website's text"""
        if element.parent.name in ['style', 'script', 'head', 'title']:
            return False
        elif isinstance(element, Doctype):
            return False
        return True

    def get_sentence(self, word):
        """Returns the sentence in which the word occurred"""
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(self.text)
        for sentence in sentences:
            if word.lower().strip() in sentence.lower():
                return sentence
        return "Sorry, no context was found!"

    def print_words(self, found, number):
        """Prints each found word with its definition"""
        for i in xrange(number):
            word = found[i]
            print word, self.dictionary[word]

    def prep_dictionary(self):
        """Loads the dictionary and word lists into a dictionary"""
        self.dictionary = dict()
        self.frequencies = dict()
        with open('word_lists/words_freqs_defs.txt', 'r') as english_dict:
            data = english_dict.readlines()
        for line in data:
            word, freq, dfn = line.decode('utf-8').split('\t')
            self.dictionary[word] = dfn
            self.frequencies[word] = int(freq)
        with open('word_lists/sat_words.txt', 'r') as sat_dict:
            sat_lines = sat_dict.readlines()
            self.sat_words = {word.replace('\n', '').decode('utf-8') for word in sat_lines}
        with open('word_lists/gre_words.txt', 'r') as gre_dict:
            gre_lines = gre_dict.readlines()
            self.gre_words = {word.replace('\n', '').decode('utf-8') for word in gre_lines}

def prep_wordnet():
    """Initializes WordNet, since the first query takes ~3 seconds"""
    lemma = WordNetLemmatizer()
    wordnet.synsets(lemma.lemmatize('hello'))
    return lemma.lemmatize

def get_trans_table():
    """Returns a translation table mapping all non-letters to a space"""
    not_letter = lambda i: not unicodedata.category(unichr(i)).startswith('L')
    letters = [i for i in xrange(sys.maxunicode) if not_letter(i)]
    return dict.fromkeys(letters, u' ')

def main():
    """ Main function """
    with open(sys.argv[1], 'r') as book_file:
        book = book_file.read()
    analyzer = TextAnalyzer()
    start = datetime.now()
    analyzer.find_words(book, analyzer.english_words)
    print datetime.now() - start

if __name__ == "__main__":
    main()
