import curses
import curses.ascii
import random
import nltk
import time
import configparser
import threading

nltk.download('reuters')
nltk.download('punkt')

from nltk.corpus import reuters
from nltk import bigrams, FreqDist, ConditionalFreqDist

endloop = False

def timer():
    global endloop
    endloop = True

def set_timer(interval):
    threading.Timer(interval, timer).start()

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


def printscreen(stdscr, message, percentage, speed, cursor, correct, time):
    height, width = stdscr.getmaxyx()
    wrapped_message = wrap_text(message, width)

    stdscr.addstr(0, 0, f"{speed: .1f} words per min | {percentage: .1f} % accuracy | {time: .1f} s | ESC to exit    ", curses.A_REVERSE)
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
    
def update_hiscore(config, speed, percentage, time):
    updated = False
    ret = 0
    if(speed > config['Hiscore1'].getfloat('WordsPerMin')):
        config['Hiscore3']['WordsPerMin'] = config['Hiscore2']['WordsPerMin']
        config['Hiscore3']['Accuracy'] = config['Hiscore2']['Accuracy']
        config['Hiscore3']['Time'] = config['Hiscore2']['Time']

        config['Hiscore2']['WordsPerMin'] = config['Hiscore1']['WordsPerMin']
        config['Hiscore2']['Accuracy'] = config['Hiscore1']['Accuracy']
        config['Hiscore2']['Time'] = config['Hiscore1']['Time']

        config['Hiscore1']['WordsPerMin'] = str(round(speed,1))
        config['Hiscore1']['Accuracy'] = str(round(percentage,1))
        config['Hiscore1']['Time'] = str(round(time,1))

        updated = True
        ret = 1
    elif(speed > config['Hiscore2'].getfloat('WordsPerMin')):
        config['Hiscore3']['WordsPerMin'] = config['Hiscore2']['WordsPerMin']
        config['Hiscore3']['Accuracy'] = config['Hiscore2']['Accuracy']
        config['Hiscore3']['Time'] = config['Hiscore2']['Time']

        config['Hiscore2']['WordsPerMin'] = str(round(speed,1))
        config['Hiscore2']['Accuracy'] = str(round(percentage,1))
        config['Hiscore2']['Time'] = str(round(time,1))
        updated = True
        ret = 2
    elif(speed > config['Hiscore3'].getfloat('WordsPerMin')):
        config['Hiscore3']['WordsPerMin'] = str(round(speed,1))
        config['Hiscore3']['Accuracy'] = str(round(percentage,1))
        config['Hiscore3']['Time'] = str(round(time,1))
        updated = True
        ret = 3
    if updated:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    return ret

def main(stdscr):
    config = configparser.ConfigParser()
    config.read('config.ini')


    message = generate_sentence(config['UI'].getint('TextLength'))
    correct = []

    # Initialize ncurses
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.nodelay(True)    #set getch() non-blocking

    interval = config['UI'].getint('TimeLimit')
    if(interval > 0):
        set_timer(interval)
    start = time.time()
    printscreen(stdscr, message, 0, 0, 0, correct, 0)

    x = 0
    y = 0
    while(x < len(message)):
        if(endloop):
            break
        ch = stdscr.getch()
        if ch == -1:
            continue
        elif ch == curses.ascii.ESC:
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if x > 0:
                x -= 1
                correct.pop()
        #normal key press
        else:
            if ch == ord(message[x]):
                correct.append(1)
            else:
                correct.append(0)
            x += 1
        current = time.time()
        speed = sum(correct)/5 / (current - start) * 60
        percentage = sum(correct) / x * 100
        y = printscreen(stdscr, message, percentage, speed, x, correct, time.time() - start)
    hiscore = update_hiscore(config, speed, percentage, time.time() - start)
    stdscr.addstr(y, 0, f"High score 1: {config['Hiscore1']['WordsPerMin']} words per min | {config['Hiscore1']['Accuracy']} % accuracy | {config['Hiscore1']['Time']} s", curses.A_REVERSE)
    stdscr.addstr(y+1, 0, f"High score 2: {config['Hiscore2']['WordsPerMin']} words per min | {config['Hiscore2']['Accuracy']} % accuracy | {config['Hiscore2']['Time']} s", curses.A_REVERSE)
    stdscr.addstr(y+2, 0, f"High score 3: {config['Hiscore3']['WordsPerMin']} words per min | {config['Hiscore3']['Accuracy']} % accuracy | {config['Hiscore3']['Time']} s", curses.A_REVERSE)
    if hiscore > 0:
        stdscr.addstr(y+3, 0, f"New high score {hiscore}!", curses.A_REVERSE)
        stdscr.refresh()
        time.sleep(5)
        stdscr.addstr(y+4, 0, "Finished - Press any key to exit", curses.A_REVERSE)
    else:
        stdscr.refresh()
        time.sleep(5)
        stdscr.addstr(y+3, 0, "Finished - Press any key to exit", curses.A_REVERSE)
    stdscr.refresh()

    curses.flushinp()
    while(stdscr.getch() == -1):
        pass

# Run the application
if __name__ == "__main__": 

    curses.wrapper(main)