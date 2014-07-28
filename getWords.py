""" Finds words common to vocabulary list and text """
import string
import sys
import re
from nltk.corpus import wordnet as wn

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
            orig_text = self.book.split('\n')
        else:
            textFile = open(self.book, 'r')
            orig_text = textFile.readlines()
            textFile.close()
        text = ""
        for line in orig_text:
            if not line.strip():
                continue
            else:
                text += line.strip() + " "
        return text

    def sentences(self):
        """ Returns the text broken up into sentences """
        return re.split('\. +|! |\? ', self.text)

    def wordSet(self):
        """ Returns a set of all words in the text """
        to_clean = string.maketrans("", "")
        clean = self.text.translate(to_clean, string.punctuation)
        clean = clean.lower().split()
        for word in clean:
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
        self.vocab.pop(0)
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
            if ".num" in self.list:
                freq_pos = 0
                word_pos = 1
            elif "ANC" in self.list:
                freq_pos = 3
                word_pos = 0
            elif "en.txt" or "subtitles" in self.list:
                freq_pos = 1
                word_pos = 0
            for line in self.vocab:
                freq = line.split()[freq_pos]
                word = line.split()[word_pos]
                if word in self.words or not wn.synsets(word):
                    continue
                self.words[word] = int(freq)
        return self.words


def context(word, sentences):
    """ Displays sentences in which the words occur in the text """
    for sen in sentences:
        no_punc = sen.translate(string.maketrans("", ""), string.punctuation)
        if word in no_punc.split():
            return "\t" + sen.strip() + "\n"


def intersect(vocab, book):
    """ Displays words and definitions """
    bookWords = book.wordSet()
    vocabWords = vocab.wordDict()
    sentences = book.sentences()
    intersection = ""
    if len(sys.argv) == 4:
        show_context = True
    else:
        show_context = False
    intersect = list(bookWords.intersection(set(vocabWords.keys())))
    if "vocab" in vocab.list:
        for word in sorted(intersect):
            intersection += word + " - " + vocabWords.get(word) + "\n"
            if show_context:
                intersection += context(word, sentences)
    else:
        freqs = []
        for word in intersect:
            freqs.append(vocabWords.get(word))
        sort = [x for (y, x) in sorted(zip(freqs, intersect), reverse=True)]
        length = len(intersect) - 1
        for i in xrange(100):
            word = sort[length - i]
            intersection += word + " - " + wn.synsets(word)[0].definition + "\n"
            if show_context:
                intersection += context(word, sentences)
    return intersection


def main():
    """ Main function """
    book = Book(sys.argv[1], False)
    vocab = Vocab(sys.argv[2], False)
    print intersect(vocab, book)

if __name__ == "__main__":
    main()
