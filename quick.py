f = open('gre_words.txt', 'r')
f = f.readlines()
n = open('gre.txt', 'w+')
for line in f:
    word = line.split('\t', 1)[0]
    n.write(word + '\n')