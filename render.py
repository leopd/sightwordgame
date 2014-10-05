#!/usr/bin/python
"""Renders deck.json file into postscript.

Usage:
    python render.py deck.json

"""

import json
import sys


class CompleteDeck:

    def __init__(self,fn):
        self.cards = json.load(open(fn))
        self.num_cards = len(self.cards)
        self.num_words = len(self.cards[0])


    def __repr__(self):
        return "Deck with %d cards each with %d words" % (self.num_cards,self.num_words)


    def text_setup(self):
        print """
            /Times-Roman findfont
            32 scalefont
            setfont
        """


    def render_word(self, word, position, number):
        print """100 200 translate
            45 rotate
            newpath
            0 0 moveto
            (%s) true charpath
            0.5 setlinewidth
            0.4 setgray
            stroke
        """ % word


    def render_card(self,n):
        card = self.cards[n]
        print "%%%% Card= %s" % str(card)
        self.text_setup()
        for word in card:
            self.render_word(word, 0, 0)


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
    deck.render_card(0)
    ps_closer()

