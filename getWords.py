import string, sys, re

book = sys.argv[1]
wordList = sys.argv[2]    

textFile = open(book, 'r')
vocabFile = open(wordList, 'r')
orig_text = textFile.readlines()
text = ""
for line in orig_text:
    if not line.strip():
        continue
    else:
        text += line.strip() + " "

vocab = vocabFile.read()
textFile.close()
vocabFile.close()

vocabWords = {}
vocab = vocab.split('\n')
vocab.remove('')

sentences = re.split('\. +|! |\? |\t*', text)
text = text.translate(string.maketrans("", ""), "!\"#$%&'()*+-,./:;<=>?@[\]^_`{|}~0123456789")

lower = text.lower().split()

textWords = set()

for i in lower:
    textWords.add(i)

def vocabulary():
    for line in vocab:
        definition = line.split('\t')[1]
        word = line.split('\t')[0]
        if word in vocabWords:
            continue
        vocabWords[word] = definition

    intersect = list(textWords.intersection(set(vocabWords.keys())))
    for word in sorted(intersect):
        print word + " - " + vocabWords.get(word)
        print
        for sen in sentences:
            if word in sen:
                print "\t" + sen.strip()
                print

def frequencies():
    if ".num" in wordList:
        for line in vocab:
            freq = line.split()[0]
            word = line.split()[1]
            if word in vocabWords:
                continue
            vocabWords[word] = freq
    elif "ANC" in wordList:
        for line in vocab:
            freq = line.split()[3]
            word = line.split()[0]
            if word in vocabWords:
                continue
            vocabWords[word] = freq
    elif "en.txt" or "subtitles" in wordList:
        for line in vocab:
            freq = line.split()[1]
            word = line.split()[0]
            if word in vocabWords:
                continue
            vocabWords[word] = freq

    intersect = list(textWords.intersection(set(vocabWords.keys())))
    intersect_freqs = []
    for word in intersect:
        intersect_freqs.append(vocabWords.get(word))
    sort = [x for (y,x) in sorted(zip(intersect_freqs, intersect), reverse=True)]
    length = len(intersect) - 1
    for i in xrange(100):
        word = sort[length - i]
        print word, intersect_freqs[intersect.index(word)]

if "vocab" in sys.argv[2]:
    vocabulary()
else:
    frequencies()
