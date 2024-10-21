# type_train
Keyboard touch typing training with python/ncurses.
The script generates a random sentence with a given number of words using the Python nltk package.
Your job is to type the sentence following the cursor (you can also use backspace). The script displays your accuracy and speed (measured in correct characters per minute).
You can exit at any time by pressing ESC.

Note that the sentences are generated using a rather simple method (calculate frequencies of pair of consecutive words in a large corpus of text, select next word based on calcualted frequencies) and in most cases, will not make sense. 

## Prerequisites 
Tested on Linux, should also work on MacOS. Windows is currently not supported.
The script needs the python nltk package, which can be install with:
```sh
pip install nltk
```
Or with the relevant OS command in case the package is managed by the OS.

## Configuration
You can configure the following parameters in the configuration file `config.ini`:
 - `TimeLimit`: A timer. Any positive value (in seconds) will indicate that the typing test will end automatically after the timer expires.
 - `TextLength`: The length of the random text, in words (including punctuation).
