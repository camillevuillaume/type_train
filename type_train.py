import curses
import curses.ascii
import random
import nltk
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

def wrap_text(text, width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word)  < width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    return lines


def printscreen(stdscr, message, percentage, speed, cursor, correct):
    height, width = stdscr.getmaxyx()
    wrapped_message = wrap_text(message, width)

    stdscr.addstr(0, 0, "correct: " + f"{percentage: .1f}" + "% | " + f"{speed: .1f}" + " words per min | ESC to exit    ", curses.A_REVERSE)
    y = 1
    position = 0

    for line in wrapped_message:
        stdscr.addstr(y, 0, line, curses.A_NORMAL)
        if(position <= cursor and cursor - position < len(line)):
            stdscr.chgat(y, cursor - position, 1, curses.A_REVERSE)
        for i in range(len(line)):
            if(position + i >= cursor):
                break
            elif correct[position + i] == 1:
                stdscr.chgat(y, i, 1, curses.color_pair(1))
            elif correct[position + i] == 0 and position + i < cursor:
                stdscr.chgat(y, i, 1, curses.color_pair(2))
        position += len(line)
        y += 1
    stdscr.refresh()
    return y
    

def main(stdscr):

    message = generate_sentence(50)
    correct = []

    # Initialize ncurses
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    printscreen(stdscr, message, 0, 0, 0, correct)
    start = time.time()

    x = 0
    y = 0
    while(x < len(message)):
        ch = stdscr.getch()
        if ch == curses.ascii.ESC:
            break
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            if x > 0:
                x -= 1
                correct.pop()
        else:
            if ch == ord(message[x]):
                correct.append(1)
            else:
                correct.append(0)
            x += 1
        current = time.time()
        speed = sum(correct)/5 / (current - start) * 60
        percentage = sum(correct) / x * 100
        y = printscreen(stdscr, message, percentage, speed, x, correct)
    stdscr.addstr(y, 0, "Press any key to exit", curses.A_REVERSE) 

    stdscr.getch()

# Run the application

if __name__ == "__main__": 

    curses.wrapper(main)