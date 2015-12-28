"""Playing around with Python text modules to do MadLibs

This will read a PDF file. It will produce a version with random words removed, that
can be filled out for fun. It will also produce a version with words replaced with
the same part of speech: adverb, adjective, verb, or noun. TextBlob doesn't seem to
work well with words with apostrophes, like doesn't. It transforms that into four
syntactical components: "does", "n", "'", and "t". Hence, this will only work on
text PDFs without apostrophes.


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
# The parts of speech we are interested in replacing
ADS_NN_VB = ADJECTIVES + ADVERBS + NOUNS + VERBS

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
    text_version = re.sub(r"(\.\n)\s*", "\g<1>", x)
    return text_version


def find_same_part_of_speech(type_list, word_list, num_words, word_index):
    """Finds a random element in word_list that is the same sort of word (e.g., adverb).

    Just increments the index into the word list (modulo for wrapping around) until it gets
    a match in type_list, and it returns that word.

    """
    while True:
        word_blob = TextBlob(word_list[word_index])
        if word_blob.tags[0][1] in type_list:
            return(word_list[word_index])
        else:
            word_index = (word_index+1) % num_words



def main():
    input_file = "test-1.pdf"
    string_form = text_list(input_file)
    # print(string_form)
    string_form = clean_text(string_form)
    # print(string_form)
    # Exit if an apostrophe is found
    if string_form.find("'") != -1:
        print("Apostrophes found at location {0}. Can't parse.".format(string_form.find("'")))
        return
    blob = TextBlob(string_form)
    # string_form = string_form.replace("Amazon", "Dragon")

    # print(string_form)
    # print("Blob length = ", len(blob.tags), blob.tags)

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
    # print("There are {} words in words.txt. It is of type {}".format(num_words, type(words)))

    random.seed()
    for i in range(0, len(blob.tags),4):
        if blob.tags[i][1] in ADS_NN_VB:
            # print(blob.tags[i][0], "is a changable syntactic element of type", blob.tags[i][1], end=". ")
            index = random.randint(0, num_words)
            if blob.tags[i][1] in ADJECTIVES:
                new_word = find_same_part_of_speech(ADJECTIVES, words,num_words, index).rstrip()
            elif blob.tags[i][1] in ADVERBS:
                new_word = find_same_part_of_speech(ADVERBS, words,num_words, index).rstrip()
            elif blob.tags[i][1] in NOUNS:
                new_word = find_same_part_of_speech(NOUNS, words,num_words, index).rstrip()
            elif blob.tags[i][1] in VERBS:
                new_word = find_same_part_of_speech(VERBS, words,num_words, index).rstrip()
            # print("Replace with", new_word)
            string_form = string_form.replace(blob.tags[i][0], new_word)
    print("\n")
    print(string_form)




# Check for interactive session
if __name__ == '__main__':
    # execute main program
    main()
