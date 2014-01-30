
try:
    import ZODB
except ImportError:
    print """This package depends upon the ZODB package.  Please
    check that this dependency is installed and that
    PYPATH points to it."""
    raise

try:
    import nltk
except ImportError:
    print """This package depends upon the Natural Language
    Toolkit package.  Please check that this dependency is
    installed and that PYPATH points to it."""
    raise

