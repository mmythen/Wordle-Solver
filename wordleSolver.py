from itertools import product
import functools
import math
import sys
import os


# Allows for not pre-defined path to wordList to allow for .exe
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

file = open(resource_path("wordList.txt"), "r")
all_words = []
for line in file:
    all_words.append(line[:-1])




# actual stuff begins here




#cache :heart-eyes:
@functools.cache
def get_feedback(guess, actual):
    pattern = ['B'] * 5
    # counts how many of a letter exist to ensure correct amount of yellows
    letters = {}

    # populating letters
    # if letters[char] exists then += 1 else letters[char] = 1
    for char in actual:
        letters[char] = letters.get(char, 0) + 1
    
    # starting with yellows
    for i in range(5):
        if guess[i] in actual and letters[guess[i]] > 0:
            pattern[i] = 'Y'
            letters[guess[i]] -= 1
    
    #overriding B's and Y's with green as it takes priority
    for i in range(5):
        if guess[i] == actual[i]:
            pattern[i] = 'G'
    
    return tuple(pattern)

def get_entropy(guess, words):
    # map of all combinations of length 5 with characters B,Y,G : counter
    all_patterns = list(product(['B', 'Y', 'G'], repeat = 5))
    frequency = {pattern: 0 for pattern in all_patterns}

    #counts how often a pattern appears for a given guess word compared to all other possible words
    for actual in words:
        pattern = get_feedback(guess, actual)
        frequency[pattern] += 1
    
    #entropy function to calculate the amount of information given from the guess
    entropy = 0
    for val in frequency.values():
        if val != 0:
            prob = val / len(words)
            entropy += -prob * math.log(prob, 2)

    return entropy

def highest_entropy(words):
    d = {}
    for selection in words:
        d[selection] = get_entropy(selection, words)
    
    return max(d, key=d.get)


def guessing(feedback, prev_guess, round, candidates):
    # begin with all words possible
    if round == 1:
        candidates= all_words.copy()

    # loop through 5 guesses
    if feedback == 'GGGGG':
            print("congrats!!!")
            return
        
    green = {}
    yellow = {}
    excluded = set()

    
    for j in range(5):
        if feedback[j] == 'G':
            green[j] = prev_guess[j]
        elif feedback[j] == 'Y':
            yellow[j] = prev_guess[j]
        else:
            excluded.add(prev_guess[j])
    
    #updating candidate list based on input
    new_candidates = []
    for word in candidates:
        valid = True
        #greens
        for position, letter in green.items():
            if word[position] != letter:
                valid = False
                break
        #yellows
        for position, letter in yellow.items():
            if letter not in word or word[position] == letter:
                valid = False
                break
        #blank
        for letter in excluded:
            if letter in green.values() or letter in yellow.values():
                continue
            if letter in word:
                valid = False
                break
        #only carrying over words that hold for green yellow and blank
        if valid:
            new_candidates.append(word)

    candidates = new_candidates
    if not candidates:
        print("There are no possible words, please double check the feedback!")
        return
    
    prev_guess = highest_entropy(candidates)
    return [prev_guess, candidates]
    

        
    



