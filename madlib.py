"""Playing around with Python text modules to do MadLibs

This will read a PDF file. It will produce a version with random words removed, that
can be filled out for fun. It will also produce a version with words replaced with
the same part of speech: adverb, adjective, verb, or noun.

The code is stalled as I realized that TextBlog is unreliable. It took the word
doesn't and turned it into "does", "n", "'", and "t"

"""

import PyPDF2
import sys, logging
from textblob import TextBlob
import requests, random, re

__author__ = 'rnzucker'

ADJECTIVES = ['JJ', 'JJR', 'JJS']
ADVERBS = ['RB', 'RBR', 'RBS']
# Nouns will include pronouns
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def text_list(filename):
    """Takes a PDF filename and returns the text in the file

    """
    input_file = open(filename, "rb")
    input = PyPDF2.PdfFileReader(input_file)
    text = ""
    i = 0
    for page in input.pages:
        text += page.extractText()
        i += 1
        if i > 10:
            return text
    return text

def clean_text(text_version):
    """Takes the string version of a PDF, and gets rid of the extra line breaks that were added

    PyPDF2.extractText seems to add a line break after 80 characters, so those need to be stripped out.
    But that results in one long line. This function restores the line breaks that were there after
    periods.
    """
    # Remove the newlines that are not preceded by periods
    x = re.sub(r"([^\.])\n", "\g<1>", text_version)
    # Remove the white space after the newline that is preceded by a period (and is on the next line)
    y = re.sub(r"(\.\n)\s*", "\g<1>", x)
    text_version = y
    return text_version


def main():
    input_file = "test-1.pdf"
    string_form = text_list(input_file)
    print(string_form)
    string_form = clean_text(string_form)
    blob = TextBlob(string_form)
    string_form = string_form.replace("Amazon", "Dragon")

    print(string_form)
    print("Blob length = ", len(blob.tags), blob.tags)

    # Wanted to pull word list from a website, but I was worried about hitting the website too much
    # while developing the code. I downloaded the file, but left the old code here as an example.
    # This code results in each element of the list being a byte literal. To convert to a string use
    # the decode option, like words[index].decode("utf-8")
    #
    # word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    # word_list = requests.get(word_site)
    # words = word_list.content.splitlines()
    word_file = open("words.txt", "r")
    words = word_file.readlines()
    num_words = len(words)
    print("There are {} words. It is of type {}".format(num_words, type(words)))

    random.seed()
    index = random.randint(0, num_words)
    single_blob = TextBlob(words[index])
    print("Random word", index, "is", words[index].rstrip(), ", type", single_blob.tags[0][1], "is a", end="")
    if single_blob.tags[0][1] in ADJECTIVES:
        print('adjective')
    elif single_blob.tags[0][1] in ADVERBS:
        print(' adverb')
    elif single_blob.tags[0][1] in NOUNS:
        print(' noun')
    elif single_blob.tags[0][1] in VERBS:
        print(' verb')
    else:
        print(' other type')



# Check for interactive session
if __name__ == '__main__':
    # execute main program
    main()
