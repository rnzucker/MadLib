"""Playing around with Python text modules to do MadLibs

This will read a webpage, preferably a newspaper article.
It will produce a version with random words removed, that
can be filled out for fun. It will also produce a version
with words replaced with the same part of speech: adverb,
adjective, verb, or noun.

default URL, if none passed in is an article from the NY Times:
http://www.nytimes.com/2015/10/27/upshot/trust-your-eyes-a-hot-streak-is-not-a-myth.html
"""

from urllib.request import urlopen
from urllib.error import HTTPError
import PyPDF2
import sys, logging, requests
import os

__author__ = 'rnzucker'

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def text_list(filename):
    """Takes a PDF filename and returns the text in the file

    """
    input_file = open(filename, "rb")
    print("Opened", filename)
    input = PyPDF2.PdfFileReader(input_file)
    text = ""
    i = 0
    for page in input.pages:
        text += page.extractText()
        i += 1
        if i > 10:
            return text
    return text

def main():
    input_file = "test.pdf"
    print(text_list(input_file))


# Check for interactive session
if __name__ == '__main__':
    # execute main program
    main()
