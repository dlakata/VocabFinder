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
3. Set up a ```virtualenv``` and install the requirements:

    ```
    $ virtualenv VocabFinder
    $ cd VocabFinder
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python
    >>> import nltk
    >>> nltk.download()
    [In the new window that appears, select 'wordnet' under Corpora, select 'Download', and exit the window.]
    ```
3. Find the book/text you wish to read in the form of a .txt file. The examples in the ```books``` folder were found using the Internet Archive (www.archive.org) and Project Gutenberg (www.gutenberg.org/).
4. Find a vocabulary list you'd like to use. Several examples can be found in the ```wordLists``` folder. Vocabulary lists, such as the Barron's and David Foster Wallace word lists, can be found using sites like www.quizlet.com and www.vocabulary.com. Each line should start with a word, followed by a tab, and end with the word's definition. Quizlet and Vocabulary.com can easily export lists in this tab-delimited format. If the file contains only words but no definitions, VocabFinder will find a definition for each word.
5. Alternatively, you can use a word-frequency list, such as the ```freq_all.num``` and ```freq_ANC-all-count.txt``` lists, which come from the British National Corpus (www.kilgarriff.co.uk/bnc-readme.html) and the American National Corpus (www.anc.org/data/anc-second-release/frequency-data/), respectively. VocabFinder will find a definition for each word.
6. Vocabulary lists (not frequency lists) should have "vocab" in their name. VocabFinder will print the sentences in which the word occurred in the text if it is given a fourth argument (no matter what it is). Having chosen a text and a vocabulary list, run VocabFinder:

    ```
    $ python getWords.py [path to book/text] [path to word list] [show context option]
    ```
Examples:

    ```
    $ python getWords.py books/walden.txt wordLists/vocab_dfw.txt
    fictile - capable of being molded or modeled (especially of earth or clay or other soft material)
    internecine - (of conflict) within a group or organization 
    invidious - containing or implying a slight or showing prejudice 
    pellicle - thin protective membrane in some protozoa
    pinnate - (of a leaf shape) featherlike; having leaflets on each side of a common axis
    poplar - any of numerous trees of north temperate regions having light soft wood and flowers borne in catkins

    $ python getWords.py books/love.txt wordLists/freq_subtitles.txt 1
    academician - someone elected to honorary membership in an academy

	    Urbino sat with him on the terrace in the patio, the coolest spot in the house, and he had summoned the most diligent reserves of his passion for pedagogy until the parrot learned to speak French like an academician

    accented - to stress, single out as important

	    The woman sat down across from him and spoke in accented Spanish

    acclimatization - adaptation to a new climate (a new temperature or altitude or environment)

	    He had heard of the black roses of Turkey, which were perhaps the most appropriate, but he had not been able to obtain any for acclimatization in his patio
    ```
