"""Playing around with Python text modules to do MadLibs

This will read a PDF file. It will produce a version with random words removed, that
can be filled out for fun. It will also produce a version with words replaced with
the same part of speech: adverb, adjective, verb, or noun.

"""

from urllib.request import urlopen
from urllib.error import HTTPError
import PyPDF2
import sys, logging, requests
from textblob import TextBlob
import os

__author__ = 'rnzucker'

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

def main():
    input_file = "test.pdf"
    text_version = text_list(input_file)
    # Create a special string that won't occur naturally, three multiplication symbols in a row
    repl_string = chr(215) + chr(215) + chr(215)
    # Replace normal line breaks after a period with the special marker
    text_version = text_version.replace(".\n", repl_string)
    # Replace the line breaks left with a null string
    text_version = text_version.replace("\n", "")
    # Replace the special marker with a period and a line break
    text_version = text_version.replace(repl_string, ".\n")
    # Get rid of the extra space resulting at the beginning of some lines
    text_version = text_version.replace("\n ", "\n")
    blob = TextBlob(text_version)
    # extractText seems to add a line break after 80 characters, so those need to be stripped out.
    # This results in one long line.

    print(blob)
    print(blob.tags)


# Check for interactive session
if __name__ == '__main__':
    # execute main program
    main()
