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

    def update(self,n):
        if time.time() - self._last >= self._howoften:
            howlong = time.time() - self._start
            print "After %.1fs %s: %d" % (howlong, self._msg, n)
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

    candidates = Set()

    for card in combos:
        if len(candidates) == 0:
            candidates.add(card)
    
    pairs = subsets_of_size(combos,2,True)
    n=0
    progress = ProgressIndicator("pairs seen so far")
    last = time.time()
    for pair in pairs:
        n += 1
        progress.update(n)
    print "Found %d pairs total" % n


if __name__ == "__main__":
    words = Wordlist('wordlist.txt')
    find_card_pairs(words.words, 4)


