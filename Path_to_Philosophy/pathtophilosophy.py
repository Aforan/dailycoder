""" 
Reddit's DailyProgrammer : [03/27/13] Challenge #121 [Intermediate] Path to Philosophy

Written By: Andrew Foran
"""
from bs4 import BeautifulSoup
from urllib import urlopen
import StringIO
import gzip
import urllib2
import re
import threading

''' Some Static Variables '''

base = 'http://en.wikipedia.org'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#Page cache in case we want to look at other links than just the first one, implement backtracking etc.
pages = {}

def wikiP(url):

	"""
	Main function, gets the page, then the links from the page,
	then checks if the page is the target page, and then calls 
	itself recursively (returns) on the first link that was found.
	"""

	page = getContent(url)

	print 'Getting links from ', url
	links = getLinks(page)

	if links == None:
		return 0

	for link in links:
		if not link in pages:
			title = link.lstrip('/wiki/')

			if title == 'Philosophy':
				print 'Found philosophy, exiting'
				return 0

			pages[title] = link

			return wikiP(base + link)

def getLinks(page):
	"""
	Gets all the links from the content are of the page excluding content in parenthesis,
	Uses BeautifulSoup to grap all content in <p> tags and then parses each for links
	"""

	content = BeautifulSoup(strip_parens(page))
	contentSoup = content.find('div', attrs={'class': 'mw-content-ltr', 'id': 'mw-content-text'})
	paraSoup = contentSoup.findAll('p')

	if paraSoup == None:
		return None

	links = []

	for para in paraSoup:
		linkSoup = para.findAll('a', title=True)

		for l in linkSoup:
			if 'Help' in l['title']:
				continue

			link = l['href']
			if '/wiki' in link:
				links += [link]

	return links


def strip_parens(s):
    """
    Strips parentheses and their contents from input, except parentheses
    appearing in < > brackets
    CREDIT: Reddit user, NUNTIUMNECAVI 

    """
    result, parens, bracks = '', 0, 0
    for i in xrange(len(s)):
        if not bracks and s[i] is '(':
            parens += 1
        elif not bracks and s[i] is ')':
            parens -= 1
            continue
        elif not parens and s[i] is '<':
            bracks += 1
        elif not parens and s[i] is '>':
            bracks -= 1
        if not parens:
            result += s[i]
    return result

def getContent(url):
	content = opener.open(url)
	
	if content.info().get('Content-Encoding') == 'gzip':
		buf = StringIO.StringIO(content.read())
		gzip_f = gzip.GzipFile(fileobj=buf)
		content = gzip_f.read()
	else:
		content = content.read()

	return content

if __name__ == '__main__':
	wikiP('http://en.wikipedia.org/wiki/Molecule')