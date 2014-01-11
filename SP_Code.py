#!/usr/bin/python

import os
import pickle
import cPickle
import sys
from collections import defaultdict

import nltk

BASEDIR  = "/home/bokinsky/727CSCE/"
NOUNTAGS = ['NN', 'NNS', 'NNP', 'NPS']
VERBTAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
ADJTAGS  = ['JJ']


def get_arts(where):
    where = os.path.join(BASEDIR, where)
    for jnl in os.listdir(where):
        for art in os.listdir(os.path.join(where, jnl)):
            #print "Sending", dir + '/' + jnl + '/' + art
            yield open(os.path.join(where, jnl, art), 'r').read()

def conserve(SPobject, filename=""):
    if not filename:
        filename = SPobject.get_name()
    cPickle.dump(SPobject, open(os.path.join(BASEDIR, filename) + '.pkl', 'wb'))


class SP_Text(object):
    def __init__(self, whichdir):
        # see dF's response to this question: http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
        self._text = nltk.Text([word for art in self.get_arts2(whichdir) for sent in nltk.sent_tokenize(art) for word in nltk.word_tokenize(sent)])
        self._pos = nltk.pos_tag([word for art in self.get_arts2(whichdir) for sent in nltk.sent_tokenize(art) for word in nltk.word_tokenize(sent)])
        self._name = whichdir

    def get_arts2(self, where):
        where = os.path.join(BASEDIR, where)
        for art in os.listdir(where):
            yield open(os.path.join(where, art), 'r').read()

    def get_name(self): return self._name

    def close_nouns(self, word_of_interest, WINDOW=30):
        """Return dictionary of noun:count for all nouns within WINDOW tokens on either side of word_of_interest."""
        retval = defaultdict(int)
        for i, t in enumerate(self._pos):
            if word_of_interest in t[0]:
                lind = i-WINDOW if i > WINDOW else 0
                rind = i+WINDOW if i+WINDOW < len(self._pos) else len(self._pos)-1
                for ii in range(lind, rind):
                    if self._pos[ii][1] in NOUNTAGS:
                        retval[self._pos[ii][0]] += 1
        return retval

    def close_verbs(self, word_of_interest, WINDOW=30):
        """Return dictionary of verb:count for all verbs within WINDOW tokens on either side of word_of_interest."""
        retval = defaultdict(int)
        for i, t in enumerate(self._pos):
            if word_of_interest in t[0]:
                lind = i-WINDOW if i > WINDOW else 0
                rind = i+WINDOW if i+WINDOW < len(self._pos) else len(self._pos)-1
                for ii in range(lind, rind):
                    if self._pos[ii][1] in VERBTAGS:
                        retval[self._pos[ii][0]] += 1
        return retval

    def close_adjs(self, word_of_interest, WINDOW=30):
        """Return dictionary of noun:count for all nouns within WINDOW tokens on either side of word_of_interest."""
        retval = defaultdict(int)
        for i, t in enumerate(self._pos):
            if word_of_interest in t[0]:
                lind = i-WINDOW if i > WINDOW else 0
                rind = i+WINDOW if i+WINDOW < len(self._pos) else len(self._pos)-1
                for ii in range(lind, rind):
                    if self._pos[ii][1] in ADJTAGS:
                        retval[self._pos[ii][0]] += 1
        return retval


    #/////////////////////////////////////////////////////////////
    # Wrapper functions for nltk.Text functions
    #/////////////////////////////////////////////////////////////

    def concordance(self, word, width=80, lines=25):
        """Print concordance for 'word' with specified context window."""
        self._text.concordance(word, width, lines)

    def collocations(self, num=20, window_size=2):
        """Print collocations derived from text."""
        self._text.collocations(num, window_size)

    def count(self, word):
        """Return number of times this word appears in text."""
        return self._text.count(word)

    def similar(self, word, num=20):
        """
        Find other words that appear in the same context as the 
        specified word.
        """
        self._text.similar(word, num)

    def common_contexts(self, word, num=20):
        """
        Find contexts wherein the specified word appears.
        List most common contexts first.
        """
        self._text.common_contexts(word, num)

    def findall(self, regexp):
        """
        Find instances of the regular expression in the text.
        A pattern to match a single token must be surrounded by
        angle brackets.  Eg.

        text_object.findall("<a>(<.*>)<man>")
        monied; nervous; dangerous; white; ...
        """
        self._text.findall(regexp)


if __name__ == "__main__":
    where = sys.argv[1]
    o = SP_Text(where)
    conserve(o, "asia.txt.pkl")
