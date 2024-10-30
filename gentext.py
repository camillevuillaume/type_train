"""Generate text using the Reuters corpus."""

import random
import re
import nltk
nltk.download('reuters')
nltk.download('punkt')

from nltk.corpus import reuters
from nltk import bigrams, FreqDist, ConditionalFreqDist


def is_number(word):
    """Check if a word is a number."""
    if word.isdigit():
        return True
    return False

def is_symbol(word):
    """Check if a word is a symbol."""
#     if re.search(r'[\(\)\[\]\{\}<>/\\\|=\+-_\*\^&%\$@`~]', word):
    if re.search(r'[\(\)\[\]\{\}<>/\\\|=\+\-_\*\^&%\$@`~\"]', word):
        return True
    return False

def is_punctuation(word):
    """Check if a word is a punctuation mark."""
    if re.search(r'[\.,!\?:;]', word):
        return True
    return False

def clean_sentence(sentence):
    """Clean up a sentence by removing extra spaces and fixing punctuation."""
    sentence = re.sub(r' +', ' ', sentence)
    sentence = re.sub(r' ([\.,!\?;]) ', r'\1 ', sentence)
    return sentence

def generate_sentence(length, symbols, numbers, punctuation):
    """Generate a sentence of a given length."""
    words = reuters.words()
    #filter out symbols, numbers, and punctuation depending on the user's settings
    if not symbols:
        words = [word for word in words if not is_symbol(word)]
    if not numbers:
        words = [word for word in words if not is_number(word)]
    if not punctuation:
        words = [word for word in words if not is_punctuation(word)]

    #create bigrams and conditional frequency distribution
    bigrams = list(nltk.bigrams(words))
    cfd = nltk.ConditionalFreqDist(bigrams)

    #select a random word to start the sentence
    word = random.choice(words)
    sentence = []

    for i in range(length):
        sentence.append(word)
        #select a random word that follows the current word
        if word in cfd:
            word = random.choice(list(cfd[word].keys()))
        else:
            break

    return clean_sentence(' '.join(sentence))


