import os
import glob
import transaction
from collections import defaultdict
from ZODB import FileStorage, DB


from .SP_Text import SP_Text


class SP_Session(object):
    """An SP_Session instance represents a database session."""
    def __init__(self, path):
        ## TODO: probably want something to check for relative paths, convert 
        #       filenames to absolute paths.
        self._path = path
        self._storage = FileStorage.FileStorage(self._path)
        self._db = DB(self._storage)
        self._conn = self._db.open()
        self._dbroot = self._conn.root()

    def close(self, save=False):
        self._conn.close()
        self._db.close()
        self._storage.close()
        if not save:
            # need a closing os.sep ???
            for f in glob.glob(self._path + '*'):
                os.remove(f)

    @property
    def index(self):
        return self._dbroot.keys()

    def read_data(self, path):
        db = self._dbroot
        for dirpath, dirs, files in os.walk(path):
            # this should yield unique names for articles contained
            # on single filesystem.  Should thought be given to possible
            # multiple filesystems???
            for art in [os.path.join(dirpath, f) for f in files]:
                nt = SP_Text(art)
                db[nt.name] = nt
            transaction.commit()

# This should use wordnet to look up all related forms and mutations
# of word (eg 'French' from 'France') and pass list as argument to
# SP_Text function of same name.  Announce to user 'Looking for words
# in list: France, French, franco, ...
#
# or better, create function related_forms(word) in separate utils file
# that does this.  Session.close_* takes list of words, not single word,
# as argument
    def close_nouns(self, words, width=15):
        ret = defaultdict(int)
        texts = self._dbroot.values()
        for text in texts:
            text.close_nouns(words, width, ret)
        return ret

    def close_verbs(self, word, width=15):
        pass
    def close_adjectives(self, word, width=15):
        pass
    def concordance(self, word, width=80, lines=25):
        pass
    def collocations(self, num=20, window=2):
        pass
    def count(self, word):
        pass
    def similar(self, word, num=20):
        pass
    def common_contexts(self, word, num=20):
        pass
    def findall(self, regexp):
        pass
