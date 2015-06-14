""" Finds words common to vocabulary list and text """
import string, sys, re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

def prep_wordnet():
    lemma = WordNetLemmatizer()
    wordnet.synsets(lemma.lemmatize('hello'))
    return lemma

def create_dictionary():
    dictionary = dict()
    new_file = open('words_freqs_defs.txt', 'r')
    data = new_file.readlines()
    new_file.close()
    for line in data:
        word, freq, dfn = line.decode('utf-8').split('\t')
        dictionary[word] = int(freq), dfn
    return dictionary

def find_words(lemma, text_words, dictionary):
    found = set()
    for word in text_words:
        lookup = lemma.lemmatize(word)
        if lookup in dictionary:
            found.add(lookup)
    return sorted(found, key=lambda word: dictionary[word][0])

def process_book(lemma, dictionary, text):
    digits = re.compile('\d')
    text = text.translate(string.maketrans("",""), string.punctuation).decode('utf-8')
    text_words = set([word.strip().lower() for word in text.split(' ') if not bool(digits.search(word))])
    return find_words(lemma, text_words, dictionary)

def print_words(found, dictionary, number):
    for i in xrange(number):
        word = found[i]
        print word, dictionary[word][1]

def main():
    """ Main function """
    book_file = open(sys.argv[1], 'r')
    book = book_file.read()
    book_file.close()
    lemma = prep_wordnet()
    dictionary = create_dictionary()
    found = process_book(lemma, dictionary, book)
    print_words(found, dictionary, 10)

if __name__ == "__main__":
    main()
