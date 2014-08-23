""" Finds words common to vocabulary list and text """
import string
import sys
import re
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

class Book(object):
    """ The book to be compared against the vocabulary """
    def __init__(self, book, stream):
        self.book = book
        self.stream = stream
        self.text = self.parse()
        self.words = dict()

    def parse(self):
        """ Parses file and eliminates blank lines """
        if self.stream:
            orig_text = unicode(self.book, 'utf-8')
        else:
            textFile = open(self.book, 'r')
            orig_text = unicode(textFile.read(), 'utf-8')
            textFile.close()
        orig_text = orig_text.translate({ord(c): None for c in "\n"})
        return orig_text

    def sentences(self):
        """ Returns the text broken up into sentences """
        return re.split('\. +|! |\? ', self.text)

    def wordSet(self):
        """ Returns a set of all words in the text """
        wnl = WordNetLemmatizer()
        sentences = self.sentences()
        for sen in sentences:
            clean = sen.translate({ord(c): None for c in string.punctuation})
            clean = clean.lower().split()
            for word in clean:
                if any(ch.isdigit() for ch in word):
                    continue
                else:
                    self.words[wnl.lemmatize(word)] = sen
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


def intersect(vocab, book):
    """ Displays words and definitions """
    bookWords = book.wordSet()
    vocabWords = vocab.wordDict()
    intersection = ""
    showContext = ""
    intersect = list(set(bookWords.keys()).intersection(set(vocabWords.keys())))
    if "vocab" in vocab.filename:
        for word in sorted(intersect):
            intersection += word + " - " + vocabWords.get(word) + "\n"
            showContext += bookWords.get(word) + "\n"
    else:
        frWords = []
        frDefs = []
        frFreqs = []
        nfWords = []
        nfDefs = []
        for word in bookWords:
            synset = wn.synsets(word)
            if synset and word not in vocabWords and synset[0].definition not in nfDefs:
                nfWords.append(word)
                nfDefs.append(synset[0].definition)
            elif synset and synset[0].definition not in nfDefs:
                frWords.append(word)
                frDefs.append(synset[0].definition)
                frFreqs.append(vocabWords.get(word))
        nfSort = sorted(zip(nfWords, nfDefs))
        nfWords = [x for (x, y) in nfSort]
        nfDefs = [y for (x, y) in nfSort]
        frSort = sorted(zip(frFreqs, frWords, frDefs), reverse=True)
        frWords = [y for (x, y, z) in frSort]
        frDefs = [z for (x, y, z) in frSort]
        length = len(frWords) - 1
        i = 0
        while i < 100 and i < len(nfSort):
            word = nfWords[i]
            intersection += word + " - " + nfDefs[i] + "\n"
            showContext += bookWords.get(word) + "\n"
            i += 1
        j = 0
        while i < 100 and i < len(frSort):
            word = frWords[length - j]
            intersection += word + " - " + frDefs[i] + "\n"
            showContext += bookWords.get(word) + "\n"
            i += 1
            j += 1
    sortContext = [x for (y, x) in sorted(zip(intersection.split('\n'), showContext.split('\n')))]
    return '\n'.join(sorted(intersection.split('\n'))), '\n'.join(sortContext)


def main():
    """ Main function """
    book = Book(sys.argv[1], False)
    vocab = Vocab(sys.argv[2], False)
    print intersect(vocab, book)[0]

if __name__ == "__main__":
    main()
