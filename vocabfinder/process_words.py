"""Finds the frequencies of all the words in a given text"""
import sys, urllib2, unicodedata, codecs, nltk.data, re
from datetime import datetime
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup, Doctype
from cookielib import CookieJar

def get_trans_table():
    """Returns a translation table mapping all non-letters to a space"""
    not_letter = lambda i: not unicodedata.category(unichr(i)).startswith('L')
    letters = [i for i in xrange(sys.maxunicode) if not_letter(i)]
    return dict.fromkeys(letters, u' ')

def visible_html_entities(element):
    """Filters html tags that aren't part of the website's text"""
    non_text = ['style', 'script', 'head', 'title']
    return element.parent.name not in non_text and not isinstance(element, Doctype)

class WordData(object):
    """An object that holds a dictionary, frequency lists, and vocabulary lists"""

    def __init__(self):
        self.prep_dictionary()
        self.english_words = set(self.dictionary.keys())
        self.trans_table = get_trans_table()

    def prep_dictionary(self):
        """Loads the dictionary and word lists into a dictionary"""
        self.dictionary = dict()
        self.frequencies = dict()
        with open('word_lists/words_freqs_defs.txt', 'r') as english_dict:
            data = english_dict.readlines()
        for line in data:
            word, freq, dfn = line.decode('unicode-escape').split('\t')
            self.dictionary[word] = dfn
            self.frequencies[word] = int(freq)
        self.words = set(self.dictionary.keys())
        with open('word_lists/sat_words.txt', 'r') as sat_dict:
            sat_lines = sat_dict.readlines()
            self.sat_words = {word.replace('\n', '').decode('unicode-escape') for word in sat_lines}
        with open('word_lists/gre_words.txt', 'r') as gre_dict:
            gre_lines = gre_dict.readlines()
            self.gre_words = {word.replace('\n', '').decode('unicode-escape') for word in gre_lines}

class TextAnalyzer(object):
    """An object that analyzes a list of valid words and their frequencies"""

    @staticmethod
    def find_words(text, valid_words):
        """Cleans given text and compares the lemmatized text to a list of valid words"""
        clean_text = text.translate(word_data.trans_table)
        words = {word.strip().lower() for word in clean_text.split(' ') if len(word) > 3}
        lemmatized_words = map(lemma.lemmatize, words)
        found = valid_words & set(lemmatized_words) & word_data.words
        return sorted(found, key=lambda word: word_data.frequencies.get(word, sys.maxsize))

    @staticmethod
    def clean_website_text(url):
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
        text = ''.join(filter(visible_html_entities, soup.findAll(text=True)))
        return TextAnalyzer.clean_text(text.encode('unicode-escape'))

    @staticmethod
    def clean_text(text):
        """Handles unicode escaping"""
        return codecs.decode(text, 'unicode_escape')

    @staticmethod
    def define(word):
        """Getter method to retrieve the word's definition"""
        return word_data.dictionary[word]

nltk.data.path.append('nltk_data')
lemma = WordNetLemmatizer()
wordnet.synsets(lemma.lemmatize('hello'))  # first lemmatizer query takes 3 seconds

word_data = WordData()

valid_words = {
    'sat': word_data.sat_words,
    'gre': word_data.gre_words,
    'hardest': word_data.english_words
}

difficulty_text = {
    'sat' : 'SAT words',
    'gre' : 'GRE words',
    'hardest' : 'of the hardest English words'
}
