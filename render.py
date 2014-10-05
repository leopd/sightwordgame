#!/usr/bin/python
"""Renders deck.json file into postscript.

Usage:
    python render.py deck.json

"""

import json
import sys
import random


class CompleteDeck:

    def __init__(self,fn):
        self.cards = json.load(open(fn))
        self.num_cards = len(self.cards)
        self.num_words = len(self.cards[0])


    def __repr__(self):
        return "Deck with %d cards each with %d words" % (self.num_cards,self.num_words)


    def card_setup(self):
        print """
            /Times-Roman findfont
            28 scalefont
            setfont
            300 500 translate
        """


    def render_word(self, word, position):
        print """
            %.0f rotate
            0 -80 translate
            %d 0 moveto
            (%s) show
            0 80 translate
        """ % (360/self.num_words, len(word)*(-6), word)


    def render_card(self,n):
        card = self.cards[n]
        print "%%%% Card= %s" % str(card)
        self.card_setup()
        for idx, word in enumerate(card):
            self.render_word(word, idx)


def ps_intro():
    print "%!\n"

def ps_closer():
    print "\nshowpage\n"


if __name__ == "__main__":
    try:
        fn = sys.argv[1]
    except:
        print __doc__
        sys.exit(-1)

    deck = CompleteDeck(fn)
    ps_intro()
    deck.render_card(random.randint(0,deck.num_cards-1))
    ps_closer()

