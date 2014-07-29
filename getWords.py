""" Finds words common to vocabulary list and text """
import string
import cgi
import sys
import re
from nltk.corpus import wordnet as wn

def clean(string):
    try:
        return unicode(string, "ascii")
    except UnicodeError:
        return unicode(string, "utf-8")
    else:
        return unicode(string, "utf-8")

class Book(object):
    """ The book to be compared against the vocabulary """
    def __init__(self, book, stream):
        self.book = book
        self.stream = stream
        self.text = self.parse()
        self.words = set()

    def parse(self):
        """ Parses file and eliminates blank lines """
        if self.stream:
            orig_text = self.book
        else:
            textFile = open(self.book, 'r')
            orig_text = textFile.read()
            textFile.close()
        text = unicode(orig_text, 'utf-8')
        return text

    def sentences(self):
        """ Returns the text broken up into sentences """
        return re.split('\. +|! |\? ', self.text)

    def wordSet(self):
        """ Returns a set of all words in the text """
        clean = self.text.translate({ord(c): None for c in string.punctuation})
        clean = clean.lower().split()
        for word in clean:
            if any(ch.isdigit() for ch in word):
                continue
            else:
                self.words.add(word)
        return self.words


class Vocab(object):
    """ The vocabulary list with which to search for words in the book """
    def __init__(self, wordList, stream, filename=""):
        self.list = wordList
        self.filename = filename
        self.stream = stream
        self.words = {}
        self.vocab = self.parse()

    def parse(self):
        """ Parses the vocabulary file, and eliminates non-word lines """
        if self.stream:
            self.vocab = self.list
            self.list = self.filename
        else:
            vocabFile = open(self.list, 'r')
            self.vocab = vocabFile.read()
            vocabFile.close()
        self.vocab = self.vocab.split('\n')
        self.vocab.remove('')
        return self.vocab

    def wordDict(self):
        """ Returns a dictionary of the words and their frequencies """
        if "vocab" in self.list:
            for line in self.vocab:
                word = line.split('\t')[0]
                if len(line.split('\t')) > 1:
                    definition = line.split('\t')[1]
                else:
                    definition = wn.synsets(word)[0].definition
                if word in self.words or not wn.synsets(word):
                    continue
                self.words[word] = definition
        else:
            freq_pos = 1
            word_pos = 0
            for line in self.vocab:
                freq = line.split()[freq_pos]
                word = line.split()[word_pos]
                if word in self.words:
                    continue
                self.words[word] = int(freq)
        return self.words


def context(word, sentences):
    """ Displays sentences in which the words occur in the text """
    for sen in sentences:
        no_punc = sen.translate({ord(c): None for c in string.punctuation})
        if word in no_punc.lower().split():
            return sen.strip() + "\n"
    return ""


def intersect(vocab, book):
    """ Displays words and definitions """
    bookWords = book.wordSet()
    vocabWords = vocab.wordDict()
    sentences = book.sentences()
    intersection = ""
    showContext = ""
    intersect = list(bookWords.intersection(set(vocabWords.keys())))
    if "vocab" in vocab.list:
        for word in sorted(intersect):
            intersection += word + " - " + vocabWords.get(word) + "\n"
            showContext += context(word, sentences)
    else:
        freqs = []
        not_found = []
        for word in bookWords:
            if wn.synsets(word) and word not in vocabWords and word not in not_found:
                not_found.append(word)
            else:
                freqs.append(vocabWords.get(word))
        sortIntersect = [x for (y, x) in sorted(zip(freqs, intersect), reverse=True)]
        length = len(intersect) - 1
        sortNotFound = sorted(not_found)
        i = 0
        while i < 100 and i < len(sortNotFound):
            word = sortNotFound[i]
            intersection += word + " - " + wn.synsets(word)[0].definition + "\n"
            showContext += context(word, sentences)
            i += 1
        j = 0
        while i < 100 and i < len(sortIntersect):
            word = sortIntersect[length - j]
            intersection += word + " - " + wn.synsets(word)[0].definition + "\n"
            showContext += context(word, sentences)
            i += 1
            j += 1
        #sortContext = [x for (y, x) in sorted(zip(intersection.split('\n'), showContext.split('\n')))]
    return '\n'.join(sorted(intersection.split('\n'))), #'\n'.join(sortContext)


def main():
    """ Main function """
    book = Book(sys.argv[1], False)
    vocab = Vocab(sys.argv[2], False)
    print intersect(vocab, book)[0]

if __name__ == "__main__":
    main()
