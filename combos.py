#!/usr/bin/python

import itertools
from sets import Set

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


    def subsets(self, size):
        """Returns all possible sub-sets of length size
        """
        it = itertools.combinations(self.words,size)
        # Convert to a set of sets
        out = Set()
        for x in it:
            out.add( Set(x) )
        return out
        

if __name__ == "__main__":
    words = Wordlist('wordlist.txt')
    for n in range(1,7):
        subset = words.subsets(n)
        print "Num of %d word combos: %d" % (n, len(subset))
    combo6 = words.subsets(6)


