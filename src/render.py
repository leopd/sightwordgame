#!/usr/bin/python
"""Renders deck.json file into postscript.

Usage:
    python render.py deckfile.json num_colors

e.g.
    python reder.py deck5.json 3

(Fewer colors is harder.)

"""

import json
import sys
import random


class DeckRenderer:

    def __init__(self,fn, max_colors):
        self.cards = json.load(open(fn))
        self.num_cards = len(self.cards)
        self.num_words = len(self.cards[0])
        self.cards_rendered = 0
        self.center_x = 0
        self.center_y = 0
        self.max_colors = max_colors
        print """
            /Times-Roman findfont
            28 scalefont
            setfont
            200 650 translate
        """


    def __repr__(self):
        return "Deck with %d cards each with %d words" % (self.num_cards,self.num_words)


    def card_setup(self):
        print "%d %d translate" % (-self.center_x, -self.center_y)
        x = self.cards_rendered % 2
        y = (self.cards_rendered/2) % 3
        self.center_x = x * 250
        self.center_y = y * -250
        print """%d %d translate
            0 0 0 setrgbcolor
            newpath
            0 0 100 0 360 arc
            stroke
        """ % (self.center_x, self.center_y)
        self.cards_rendered += 1


    def render_word(self, word, position):
        colors = [
            '0 0 0',  # black
            '1 0 0',  # red
            '0 0 1',  # blue
            '0 1 0',  # green
            '1 0 1',  # purple
            '0 1 1',  # cyan
        ]
        # pick a color deterministically to help make matching easier
        color = colors[ hash(word) % self.max_colors ]
        print """
            %.0f rotate
            0 -80 translate
            %d 0 moveto
            %s setrgbcolor
            (%s) show
            0 80 translate
        """ % (360/self.num_words, len(word)*(-6), color, word.capitalize())


    def render_card(self,n):
        card = self.cards[n]
        print "%%%% Card= %s" % str(card)
        self.card_setup()
        for idx, word in enumerate(card):
            self.render_word(word, idx)
        if self.cards_rendered % 6 == 0:
            self.next_page()


    def next_page(self):
        print """
            showpage
            450 150 translate
        """


def ps_intro():
    """Prints a postscript header
    """
    print "%!\n"

def ps_closer():
    """Closes out the postscript
    """
    print "\nshowpage\n"


if __name__ == "__main__":
    try:
        fn = sys.argv[1]
        colors = int(sys.argv[2])
    except:
        print __doc__
        sys.exit(-1)

    ps_intro()
    deck = DeckRenderer(fn, colors)
    for idx in range(deck.num_cards):
        deck.render_card(idx)
    ps_closer()

