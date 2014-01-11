#***************************************************
#
# Author:      Huston Bokinsky
# Title:       Web Crawler
# Date:        16 June, 2012
# Class:       CSCE 771
#
#***************************************************


import sys
import formatter
import htmllib
import sgmllib
import urllib2
import time
import os
import re
import multiprocessing
from io import BytesIO as StringIO

try:
    from lxml.html.clean import clean_html
except:
    print """    This module depends upon the third-party module lxml.

    On Ubuntu, enter sudo apt-get install python-lxml.
    On Windows, consult the lxml installation page at
        http://lxml.de/installation.html
    """

DEN = 0.6         # fixed text/bytes ratio
MAXRECS = 1000    # a cap on the number of records to write
MINRECLEN = 1000  # something to make sure we are writing texts
                  # of a minimum length to files


def start(seed):
    outdir = re.match(r"http:\/\/(www\.)?([-\.\w]+)(.*)", seed).group(2)
    os.makedirs(outdir)

    # a set of addresses to visit and a list of visited addresses
    # to make sure we aren't duplicating ourselves
    urllist = set()
    urllist.add(seed)
    visited = list()
    records = 0

    while len(urllist) > 0 and records < MAXRECS:
        # I put this sleep bit in here just to avoid slamming some
        # poor server with a blitzkrieg of requests
        time.sleep(3)
        html = str()

        # fetch a url from the waiting list and initialize
        # the key elements of our scrubber
        nexturl = urllist.pop() 
        visited.append(nexturl)
        w = LineWriter()
        f = formatter.AbstractFormatter(w)
        p = TrackingParser(w, f)

        # put the openurl sequence in a try-catch construct
        # to keep some exception raised by a weird page from
        # throwing our program for a loop
        try:
            print "Accessing %s" % (nexturl)
            # open url and get text
            response = urllib2.urlopen(nexturl)
            html = response.read()
            response.close()

        except:
            print "Could not access %s successfully." % (nexturl)
            continue

        # (hopefully) remove scripts and other junk
        # not 100% successful
        html = clean_html(html)

        # extract links for urllist
        #linklister = URLLister()
        #linklister.feed(html)
        #linklister.close()

        # this is a hack to make use of relative links found in
        # the document.  It can probably be done more effectively,
        # but this is a project for later...
        #for url in [l for l in linklister.urls if l not in visited]:
        for url in re_urlextract(html):
            if url.startswith(seed):
                urllist.add(url)
            else:
                urllist.add(seed + url)

        # extract article text
        p.feed(html)
        p.close()

        # test if article text is worth keeping (by length) and write it
        text = w.output()
        if len(text) > MINRECLEN:
            odir = outdir or os.getcwd()
            ofile = str(records) + ".ot"
            outname = os.path.join(odir, ofile)
            print "Writing to file %s" % (outname)
            out = open(outname, 'w')
            out.write(text)
            out.close()
            records += 1
        else:
            pass
            #print "Text not long enough."

def re_urlextract(page):
    urls = list()
    mos = re.finditer(r"href=\"([^\"]+)\"", page)
    for mo in mos:
        urls.append(mo.group(1))
    return urls

# classes recommended and outlined by alexjc in "The Easy Way to
# Extract Useful Text from Arbitrary HTML."
# http://ai-depot.com/articles/the-easy-way-to-extract-useful-text-from-arbitrary-html/
class Paragraph:
    def __init__(self):
        self.text = ''
        self.by = 0
        self.density = 0.0


class LineWriter(formatter.AbstractWriter):
    def __init__(self, *args):
        self.last_index = 0
        self.lines = [Paragraph()]
        formatter.AbstractWriter.__init__(self)

    def send_flowing_data(self, data):
        # Work out the length of this text chunk.
        t = len(data)
        # We've parsed more text, so increment index.
        self.index += t
        # Calculate the number of bytes since last time.
        b = self.index - self.last_index
        self.last_index = self.index
        # Accumulate this information in current line.
        l = self.lines[-1]
        l.text += data
        l.by += b

    def send_paragraph(self, blankline):
        """Create a new paragraph if necessary."""
        if self.lines[-1].text == '':
            return
        self.lines[-1].text += '\n' * (blankline+1)
        self.lines[-1].by += 2 * (blankline+1)
        self.lines.append(Paragraph())
    
    def send_literal_data(self, data):
        self.send_flowing_data(data)
    
    def send_line_break(self):
        self.send_paragraph(0)

    def compute_density(self):
        """Calculate the density for each line, and the average."""
        total = 0.0
        for l in self.lines:
            if l.by != 0:
                l.density = len(l.text) / float(l.by)
            else:
                l.density = 0
            total += l.density
        # Store for optional use by the neural network.
        self.average = total / float(len(self.lines))
    
    def output(self):
        """Return a string with the useless lines filtered out."""
        self.compute_density()
        output = StringIO()
        for l in self.lines:
            # Check density against threshold.
            # Custom filter extensions go here.
            if l.density >= DEN:
                output.write(l.text)
        return output.getvalue()


class TrackingParser(htmllib.HTMLParser):
    """Try to keep accurate pointer of parsing location."""
    def __init__(self, writer, *args):
        htmllib.HTMLParser.__init__(self, *args)
        self.writer = writer
    
    def parse_starttag(self, i):
        index = htmllib.HTMLParser.parse_starttag(self, i)
        self.writer.index = index
        return index
    
    def parse_endtag(self, i):
        self.writer.index = i
        return htmllib.HTMLParser.parse_endtag(self, i)


class URLLister(sgmllib.SGMLParser):
    def reset(self):
        sgmllib.SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        count = 0
        procs = list()
        for line in open(sys.argv[1], "r"):
            if line:
                procs.append(multiprocessing.Process(target=start, args=(line.strip(),)))
                count += 1
        for i in range(count):
            procs[i].start()
        for i in range(count):
            procs[i].join()
    else:
        print """        Called in non-interactive mode, this module requires a
            seed URL to be passed as an argument.

        Eg. python Crawler.py http://www.bbc.co.uk
        
        Otherwise, enter interactive mode, import the module, and type
            Crawler.start("http://www.bbc.co.uk")

        Best practice for choosing the seed would be to enter the top
            level of a domain (as the above example) rather than a specific
            article.  To understand why, see the code around line 90 that
            selects links for inclusion in the "to-visit" list.
        """
