VocabFinder
===========

VocabFinder compares the text of a book/article/etc. against either a vocabulary list, or a word-frequency list. For a vocabulary list, the output consists of all the words in the vocabulary list that occur in the text, along with their definitions. For a word-frequency list, the output consists of the 100 least commonly used words in the English language that were found in the text.

Using VocabFinder
-----------
1. Make sure you have Python and git installed on your system.
2. Clone this repository:
  ```
  $ git clone https://github.com/dlakata/VocabFinder.git
  ```
3. Find the book/text you wish to read in the form of a .txt file. The examples in the ```books``` folder were found using the Internet Archive (www.archive.org) and Project Gutenberg (www.gutenberg.org/).
4. Find a vocabulary list you'd like to use. Several examples can be found in the ```wordLists``` folder. Vocabulary lists, such as the Barron's and David Foster Wallace word lists, can be found using sites like www.quizlet.com and www.vocabulary.com. Each line should start with a word, followed by a tab, and end with the word's definition. Quizlet and Vocabulary.com can easily export lists in this tab-delimited format.
5. Alternatively, you can use a word-frequency list, such as the ```freq_all``` and ```freq_ANC-all-count.txt``` lists, which come from the British National Corpus (www.kilgarriff.co.uk/bnc-readme.html) and the American National Corpus (www.anc.org/data/anc-second-release/frequency-data/), respectively.
6. Vocabulary lists (not frequency lists) should have "vocab" in their name. Having chosen a text and a vocabulary list, run VocabFinder:
```
$ python getWords.py [path to book/text] [path to word list]
```
Example:
```
$ python getWords.py books/walden.txt wordLists/vocab_dfw.txt
fictile - capable of being molded or modeled (especially of earth or clay or other soft material)
internecine - (of conflict) within a group or organization
invidious - containing or implying a slight or showing prejudice
pellicle - thin protective membrane in some protozoa
pinnate - (of a leaf shape) featherlike; having leaflets on each side of a common axis
poplar - any of numerous trees of north temperate regions having light soft wood and flowers borne in catkins
```
