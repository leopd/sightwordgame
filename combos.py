#!/usr/bin/python

import itertools
from sets import Set
import time


class Wordlist:

    def __init__(self,fn):
        self.words = Set()
        self.load(fn, 31)

    def load(self, fn, limit=999):
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


def find_card_pairs(words, words_per_card):
    print "Finding all possible combos..."
    combos = subsets_of_size(words,words_per_card)
    print "Num of %d word combos: %d" % (words_per_card, len(combos))

    deck = Set()

    def can_use(card):
        for card2 in deck:
            both = card.intersection(card2)
            if len(both) != 1:
                return False
        return True

    progress = ProgressIndicator("deck size")
    for card in combos:
        if len(deck) == 0:
            deck.add(card)
            next
        if can_use(card):
            deck.add(card)
        progress.update( len(deck ) )

    return deck


if __name__ == "__main__":
    words = Wordlist('wordlist.txt')
    deck = find_card_pairs(words.words, 6)
    print "Deck size: %d" % len(deck)
    print deck


