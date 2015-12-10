#!/usr/bin/python
import random
from math import sqrt
import os 

KNOWNS = set([3, 9, 16, 12, 8.2, 4, 27, 30, 18, 54, 4, 
              6, 2.4, 12, '8-4', 109*17, 47, sqrt(14)])
NAMES = ['Julie', 'Simon']

try:
    input = raw_input
except NameError:
    pass

def main():
    rgen = random.SystemRandom()
    print("Hello! and welcome to Numberwang, \nthe maths quiz that simply everyone is talking about!")
    you_name = input("What's your name? ")
    their_name = NAMES[rgen.randint(0, 1)]
    print("Today, you'll be playing against {}".format(their_name))
    while True:
        scores = [0,0]
        locale, learned, difficulty = _setup()
        resps = _localegen(locale)
        Numberwang = False
        turns = 0
        MAX_SCORE = 5
        while not Numberwang:
            you = input("Your turn! ")
            match = _verify(you, difficulty, KNOWNS, learned, rgen)
            new_learn = (you not in KNOWNS.union(learned)) and (rgen.random() > .9)
            print(resps[match])
            if new_learn:
                _learn(you)
            if match:
               scores[0] += 1
            them = rgen.randint(0, 109*17)
            print('{} guesses {}'.format(their_name, them))
            match = _verify(them, difficulty, KNOWNS, learned, rgen)
            print(resps[match])
            if new_learn:
                _learn(them)
            if match:
                scores[1] += 1
            if max(scores) >= MAX_SCORE:
                print("The game's been won!")
                print("{}: {}, \t {}: {}".format(you_name, scores[0], 
                                                 their_name, scores[1]))
                break
            else:
                if turns > MAX_SCORE:
                    MAX_SCORE -= 1
        again = input('Play again? [Y/N] ')
        if again.lower() in ['n', 'no']:
            print('Goodbye!')
            break

def _localegen(loc):
    """
    Generic function map, could just be a dict but ehhh
    """
    if loc.lower() == 'uk':
        resps = {True: "That's numberwang!",
                 False: "That's not numberwang!"}
    elif loc.lower() == 'us':
        resps = {True: "That is a number!", 
                 False:"Ooh, I'm sorry. That is not a number!"}
    elif loc.lower() == 'aus':
        resps = {True: "Thet's numberwang, m8!", 
                 False: "Thet's not numberwang, m8!"}
    elif loc.lower() == 'nz':
        resps = {True:"Baaaaaaah :)", False:"Baaaaaaah :("}
    elif loc.lower() == 'ger': 
        resps = {True: "Das ist numberwang!", 
                 False: "Das ist nicht numberwang!"}
    return resps

def _verify(num, difficulty, KNOWNS, learned, rgen):
    """
    Verify if a number is numberwang using Bertrand's Theorem.
    PATENT PENDING, Copyright British Broadcasting Corporation
    """
    try:
        match = False
        match |= (num in KNOWNS) or (float(num) in KNOWNS)
        match |= (num in learned)
        match &= rgen.randint(0,10 + 1) > difficulty
        threshold = difficulty/10
        new_learn = (num not in KNOWNS) and (rgen.random() < threshold)
    except ValueError:
        match = False
    return match

def _setup():
    """
    Setting up numberwang
    """
    fp = os.path.dirname(__file__)
    if os.path.isfile(os.path.join(fp, '.locale')):
        with open(os.path.join(fp, '.locale')) as f:
            locale = f.readline().strip()
    else:
        locale = 'uk'
    if os.path.isfile(os.path.join(fp, '.learned')):
        with open(os.path.join(fp, '.locale')) as f:
            learned = set([s.strip() for s in f.readlines()])
    else:
        learned = {}
    if os.path.isfile(os.path.join(fp, '.d')):
        with open(os.path.join(fp, '.d')) as f:
            difficulty = int(f.readline().strip())
    else:
        difficulty = 5 
    return locale, learned, difficulty

def _learn(num):
    """
    look ma, machine learning
    """
    fp = os.path.dirname(__file__)
    if not isinstance(num, str):
        num = str(num)
    with open(os.path.join(fp, '.learned'), 'a') as f:
        f.write(num)
        f.write('\n')

if __name__ == '__main__':
    main()
