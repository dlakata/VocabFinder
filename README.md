VocabFinder
===========

VocabFinder finds the words in a given text with the least usage in the English language.

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
    $ npm install
    $ bower install
    $ pip install -r requirements.txt
    $ python
    >>> import nltk
    >>> nltk.download()
    [In the new window that appears, download 'wordnet' from Corpora and 'Punkt' from Models. Exit the window.]
    ```
3. Start the server.

    ```
    $ python runserver.py
    ```

The ```process_words``` module can be run independently:

```
$ python VocabFinder/process_words.py VocabFinder/books/nicomachean_ethics.txt
```