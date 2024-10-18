import curses
import random
import nltk
import textwrap
import time

nltk.download('reuters')
nltk.download('punkt')

from nltk.corpus import reuters
from nltk import bigrams, FreqDist, ConditionalFreqDist

def generate_sentence(length):
    words = reuters.words()
    bigrams = list(nltk.bigrams(words))
    cfd = nltk.ConditionalFreqDist(bigrams)

    word = random.choice(words)
    sentence = []

    for i in range(length):
        sentence.append(word)
        if word in cfd:
            word = random.choice(list(cfd[word].keys()))
        else:
            break

    return ' '.join(sentence)


def printscreen(stdscr, message, percentage, speed):
    height, width = stdscr.getmaxyx()
    wrapped_message = textwrap.wrap(message, width)

    stdscr.addstr(0, 0, "correct: " + f"{percentage: .1f}" + "% | " + f"{speed: .1f}" + " characters per min | Ctrl+C to exit", curses.A_REVERSE)
    y = 1

    for line in wrapped_message:
        stdscr.addstr(y, 0, line)
        y += 1
    stdscr.refresh()
    

def main(stdscr):

    message = generate_sentence(50)

    # Initialize ncurses
    curses.curs_set(0)

    printscreen(stdscr, message, 0, 0)
    start = time.time()

    x = 0
    ok = 0
    while(x < len(message)):
        ch = stdscr.getch()
        if ch == ord(message[x]):
            ok += 1
        
        x += 1
        current = time.time()
        speed = ok / (current - start) * 60
        percentage = ok / x * 100
        printscreen(stdscr, message, percentage, speed)
    # Wait for user input
    stdscr.getch()


# Run the application

if __name__ == "__main__": 

    curses.wrapper(main)