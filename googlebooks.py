#! /usr/bin/python
# -*- coding: utf-8 -*-

"""All things specifically related to the Google Books website."""

import re
from urllib.parse import parse_qs
from urllib.parse import urlparse

import requests

#import bibtex [1]
import ris
import config
import commons
if config.lang == 'en':
    import sfn_en as sfn
    import wikicite_en as wikicite
else:
    import sfn_fa as sfn
    import wikicite_fa as wikicite


class Citation():
    
    """Create google book citation object."""
    
    def __init__(self, googlebook_url, date_format='%Y-%m-%d'):
        self.url = googlebook_url
        #self.bibtex = get_bibtex(googlebook_url) [1]
        #self.dictionary = bibtex.parse(self.bibtex) [1]
        self.bibtex = get_ris(googlebook_url)
        self.dictionary = ris.parse(self.bibtex)
        pu = urlparse(googlebook_url)
        pq = parse_qs(pu.query)
        #default domain is prefered:
        self.dictionary['url'] = 'http://' + pu.netloc +\
                                 '/books?id=' + pq['id'][0]
        #manually adding page nubmer to dictionary:
        if 'pg' in pq:
            self.dictionary['pages'] = pq['pg'][0][2:]
            self.dictionary['url'] += '&pg=' + pq['pg'][0]
        #although google does not provide a language field:
        if 'language' in self.dictionary:
            self.error = 0
        else:
            lang, err = commons.detect_lang(self.dictionary['title'])
            self.dictionary['language'] = lang
            self.dictionary['error'] = self.error = err
        self.sfnt = sfn.create(self.dictionary)
        self.cite = wikicite.create(self.dictionary, date_format)


def get_bibtex(googlebook_url):
    """Get bibtex file content from a noormags url."""
    #getting id:
    pu = urlparse(googlebook_url)
    pq = parse_qs(pu.query)
    bookid = pq['id'][0]
    url = 'http://books.google.com/books/download/?id=' +\
      bookid + '&output=bibtex'
    #Agent spoofing is needed, otherwise: HTTP Error 401: Unauthorized
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0)' +
               ' Gecko/20100101 Firefox/24.0'}
    bibtex = requests.get(url, headers=headers).text
    return bibtex

def get_ris(googlebook_url):
    """Get ris file content from a noormags url."""
    #getting id:
    pu = urlparse(googlebook_url)
    pq = parse_qs(pu.query)
    bookid = pq['id'][0]
    url = 'http://books.google.com/books/download/?id=' +\
      bookid + '&output=ris'
    #Agent spoofing is needed, otherwise: HTTP Error 401: Unauthorized
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0)' +
           ' Gecko/20100101 Firefox/24.0'}
    ris = requests.get(url, headers=headers).text
    return ris
