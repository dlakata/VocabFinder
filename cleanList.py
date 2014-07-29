import string
import sys
import re
from nltk.corpus import wordnet as wn

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

vocab = Vocab(sys.argv[1], False)
new = ""
words = {}
if ".num" in vocab.list:
    freq_pos = 0
    word_pos = 1
elif "ANC" in vocab.list:
    freq_pos = 3
    word_pos = 0
elif "en.txt" or "subtitles" in vocab.list:
    freq_pos = 1
    word_pos = 0
for line in vocab.vocab:
    freq = line.split()[freq_pos]
    word = line.split()[word_pos]
    if word in words or not wn.synsets(word):
        continue
    new += ' '.join([word, freq]) + "\n"
    words[word] = freq

newFile = open('fixed', 'w+')
newFile.write(new)
newFile.close()
