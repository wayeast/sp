Repo: SP\_Project
-------------------
Features
--------------
- *Python*
- *NLTK*
- *Python* ``multiprocessing`` *threading library*
Description
------------
The code files in this folder are the pieces of a class project to investigate
the feasibility of using natural language processing techniques on large 
amounts of text data to help political analysts gauge soft power.  *SP_Code.py*
implements a class to process large corpora of text altogether; several of
the member functions are merely wrapper functions for NLTK methods, but 
others (close_nouns, close_verbs, and close_adjs) are of my own creation.
These latter are designed to find all nouns, verbs, or adjectives within a
given proximity of all occurrences of a word of interest in a corpus.

The paper *ISA_submission* is a paper I wrote to present the project to the ISA
South conference in Charlotte, NC, 17-19 October, 2013.  It contains a 
thorough and non-technical description of what the code aims to do, the 
results obtained during development and testing, and a discussion of some
of the areas for improvement.  Please refer to this paper for a more in-depth
description of the functionality of this code.

*SP_Crawler.py* is a simple web crawler I wrote as part of a Natural Language
Processing course.  Despite its crude sophistication, I was able to use it to
scour a host of online newspaper sites for article content I could use to test
and demonstrate the efficacy of SP_Code.py.
