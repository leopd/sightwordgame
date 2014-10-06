#!/usr/bin/python
"""Finds a deck using a wordlist file

Specify word list (one word per line) and number of words per card.

Usage:
    python combos.py wordlist.txt 5

"""

import json
import itertools
import random
from sets import Set
import sys
import time


class Wordlist:

    def __init__(self,fn, limit=999):
        self.words = Set()
        self.load(fn, limit)

    def load(self, fn, limit):
        fh = open(fn)
        for word in fh.readlines():
            self.words.add(word.rstrip())
            if len(self.words) == limit:
                return

    def show(self):
        for word in self.words:
            print word


class ProgressIndicator:

    def __init__(self, msg="Update", howoften=5):
        self._start = time.time()
        self._last = self._start - howoften*0.9
        self._howoften=howoften
        self._msg = msg
        self._calls = 0

    def update(self,n):
        self._calls += 1
        if self._calls % 100 != 0:
            return
        if time.time() - self._last >= self._howoften:
            howlong = time.time() - self._start
            print "After %.1fs, %d calls, %s: %d" % (howlong, self._calls, self._msg, n)
            self._last = time.time()


def subsets_of_size(input_set, size, as_iter=False):
    """Returns all possible sub-sets of length size
    """
    it = itertools.combinations(input_set,size)
    if as_iter:
        return it
    else:
        # Convert to a set of sets
        out = Set()
        for x in it:
            out.add( Set(x) )
        return out


class Deck:
    
    def __init__(self):
        self._deck = Set()


    def can_use(self, card):
        for card2 in self._deck:
            both = card.intersection(card2)
            if len(both) != 1:
                return False
        return True


    def find_card_pairs(self, words, words_per_card, shuffle=False):
        print "Finding all possible combos..."
        combos = subsets_of_size(words,words_per_card)
        print "Num of %d word combos: %d" % (words_per_card, len(combos))

        if shuffle:
            combos = list(combos)
            random.shuffle(combos)

        progress = ProgressIndicator("deck size")
        for card in combos:
            if len(self._deck) == 0:
                self._deck.add(card)
                next
            if self.can_use(card):
                self._deck.add(card)
            progress.update( len(self._deck ) )


    def __repr__(self):
        out = "Deck size: %d\n" % len(self._deck)
        for card in self._deck:
            out += str(list(card))
            out += "\n"
        return out


    def validate(self):
        print "Validating deck"
        pairs = subsets_of_size(self._deck, 2, True)
        progress = ProgressIndicator("pairs checked",1)
        for pair in pairs:
            card1 = pair[0]
            card2 = pair[1]
            both = card1.intersection(card2)
            if len(both) != 1:
                print "!!! Bad card pair found with %s and %s" % (card1,card2)
                return False
            progress.update(0)
        print "All good!"
        return True


    def size(self):
        return len(self._deck)


    def as_json(self):
        return json.dumps([list(x) for x in self._deck], indent=2)


def optimal_deck_size(n):
    return 1+ n*(n-1)


if __name__ == "__main__":
    try:
        fn = sys.argv[1]
        N = int(sys.argv[2])
    except:
        print __doc__
        sys.exit(-1)

    words = Wordlist(fn)
    print "Using %d words" % len(words.words)

    best_deck = None
    while True:
        deck = Deck()
        deck.find_card_pairs(words.words, N, True)

        if ((not best_deck) or (deck.size() > best_deck.size())) and deck.validate():
            print "\nNew best!\n%s" % deck
            best_deck = deck
            if deck.size() >= optimal_deck_size(N):
                print "\n\nOptimal deck!\n"
                print deck.as_json()
                sys.exit(0)
        else:
            print "Worse.  Deck size=%d" % deck.size()


