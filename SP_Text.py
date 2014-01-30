from persistent import Persistent
from collections import defaultdict

import nltk


#*****************************************************#
NOUNTAGS = ['NN', 'NNS', 'NNP', 'NPS']
VERBTAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
ADJTAGS  = ['JJ']
#*****************************************************#


#*****************************************************#
def pos_word(tup):
    return tup[0]
def pos_tag (tup):
    return tup[1]
def lower_buf_ind(index, window):
    return index - window if index > window else 0
def upper_buf_ind(index, window, listlen):
    targ = index + window
    return targ if targ < listlen else listlen - 1
#*****************************************************#


class SP_Text(Persistent):
    def __init__(self, path):
        self.name = path
        with open(self._name, 'r') as f:
            text = f.read()
            self._text = nltk.Text([tok for sent in nltk.sent_tokenize(text)
                                        for tok  in nltk.word_tokenize(sent)
                                   ],
                                   name=self.name)
        self._tagged = nltk.pos_tag(self._text.tokens)

    def close_nouns(self, words, width=15, arg_dict=None):
        """Build dictionary of noun : count items for nouns in proximity of
        word.  May take defaultdict pointer arg_dict as optional argument,
        in which case close_nouns adds to what is already there.  Return
        new dictionary if no arg_dict, else number of distinct close nouns
        found.
        """
        workspace = defaultdict(int) if arg_dict is None else arg_dict
        pos_tups  = self._tagged

        for index, posTup in enumerate(pos_tups):
            if pos_word(posTup) in words:
                lo_ind = lower_buf_ind(index, width)
                hi_ind = upper_buf_ind(index, width, len(pos_tups))
                for buf_ind in range(lo_ind, hi_ind+1):
                    if pos_tag(pos_tups[buf_ind]) in NOUNTAGS:
                        workspace[pos_word(pos_tups[buf_ind])] += 1
        return workspace if arg_dict is None else len(workspace)

    def close_verbs(self, words, width=15, arg_dict=None):
        """Build dictionary of verb : count items for verbs in proximity of
        word.  May take defaultdict pointer arg_dict as optional argument,
        in which case close_verbs adds to what is already there.  Return
        new dictionary if no arg_dict, else number of distinct close verbs
        found.
        """
        workspace = defaultdict(int) if arg_dict is None else arg_dict
        pos_tups  = self._tagged

        for index, posTup in enumerate(pos_tups):
            if pos_word(posTup) in words:
                lo_ind = lower_buf_ind(index, width)
                hi_ind = upper_buf_ind(index, width, len(pos_tups))
                for buf_ind in range(lo_ind, hi_ind+1):
                    if pos_tag(pos_tups[buf_ind]) in VERBTAGS:
                        workspace[pos_word(pos_tups[buf_ind])] += 1
        return workspace if arg_dict is None else len(workspace)

    def close_adjectives(self, words, width=15, arg_dict=None):
        """Build dictionary of adjective : count items for adjectives in
        proximity of word.  May take defaultdict pointer arg_dict as
        optional argument, in which case close_adjectives adds to what
        is already there.  Return new dictionary if no arg_dict, else
        number of distinct close adjectives found.
        """
        workspace = defaultdict(int) if arg_dict is None else arg_dict
        pos_tups  = self._tagged

        for index, posTup in enumerate(pos_tups):
            if pos_word(posTup) in words:
                lo_ind = lower_buf_ind(index, width)
                hi_ind = upper_buf_ind(index, width, len(pos_tups))
                for buf_ind in range(lo_ind, hi_ind+1):
                    if pos_tag(pos_tups[buf_ind]) in ADJTAGS:
                        workspace[pos_word(pos_tups[buf_ind])] += 1
        return workspace if arg_dict is None else len(workspace)

 # look at NLTK code to see what these functions do and how to aggregate
 # their results
    def concordance(self, word, width=80, lines=25):
        self._text.concordance(word, width, lines)

    def collocations(self, num=20, window=2):
        self._text.collocations(num, window)

    def count(self, word):
        return self._text.count(word)

    def similar(self, word, num=20):
        self._text.similar(word, num)

    def common_contexts(self, word, num=20):
        self._text.common_contexts(word, num)

    def findall(self, regexp):
        self._text.findall(regexp)


