#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Codes required to create English Wikipedia citation templates."""


import datetime
import re

    
def citation_templates(d, date_format) -> tuple:
    """Create citation templates according to the given dictionary."""
    type_ = d['type']
    if type_ == 'book':
        cite = '* {{cite book'
    elif type_ in ('article', 'jour'):
        cite = '* {{cite journal'
    elif type_ == 'web':
        cite = '* {{cite web'
    else:
        raise KeyError(type_ + " is not a valid value for d['type']")

    sfn = '{{sfn'

    authors = d.get('authors')
    publisher = d.get('publisher')
    journal = d.get('journal')
    website = d.get('website')
    title = d.get('title')

    if authors:
        cite += names2para(authors, 'first', 'last', 'author')
        # {{sfn}} only supports a maximum of four authors
        for author in authors[:4]:
            sfn += ' | ' + author.lastname
    else:
        # the same order should be used in citation_template:
        sfn += ' | ' + (
            publisher or
            "''" + journal + "''" if journal else
            "''" + website + "''" if website else
            title or  'Anon.'
        )

    editors = d.get('editors')
    if editors:
        cite += names2para(editors, 'editor-first', 'editor-last', 'editor')
    translators = d.get('translators')
    if translators:
        for translator in translators:
            translator.fullname += ' (مترجم)'
        # todo: add a 'Translated by ' before name of translators
        others = d.get('others')
        if others:
            others.extend(d['translators'])
        else:
            d['others'] = d['translators']
    others = d.get('others')
    if others:
        cite += names1para(others, 'others')
    if title:
        cite += ' | title=' + title
    if journal:
        cite += ' | journal=' + journal
    elif website:
        cite += ' | website=' + website
    publisher = d.get('publisher')
    if publisher:
        cite += ' | publisher=' + publisher
    address = d.get('address')
    if address:
        cite += ' | location=' + address
    series = d.get('series')
    if series:
        cite += ' | series=' + series
    volume = d.get('volume')
    if volume:
        cite += ' | volume=' + volume
    issue = d.get('issue')
    if issue:
        cite += ' | issue=' + issue
    date = d.get('date')
    if date:
        if isinstance(date, datetime.date):
            date = (
                date.strftime(date_format).lstrip("0").replace(" 0", " ")
            )
        cite += ' | date=' + date
    year = d.get('year')
    if year:
        if not date or year not in date:
            cite += ' | year=' + year
        sfn += ' | ' + year
    isbn = d.get('isbn')
    if isbn:
        cite += ' | isbn=' + isbn
    issn = d.get('issn')
    if issn:
        cite += ' | issn=' + issn
    pmid = d.get('pmid')
    if pmid:
        cite += '| pmid=' + pmid
    pages = d.get('pages')
    if pages:
        if '–' in pages:
            sfn += ' | pp=' + pages
        else:
            sfn += ' | p=' + pages
    if type_ in ('article', 'jour'):
        if pages:
            if '–' in pages:
                cite += ' | pages=' + pages
            else:
                cite += ' | page=' + pages
    url = d.get('url')
    if url:
        cite += ' | url=' + url
    else:
        sfn += ' | p='
    doi = d.get('doi')
    if doi:
        cite += ' | doi=' + doi
    language = d.get('language')
    if language:
        if language.lower() not in ('english', 'en'):
            cite += ' | language=' + language
    if authors:
        cite += ' | ref=harv'
    else:
        # order should match sfn_template
        cite += ' | ref={{sfnref | ' +\
             (publisher or journal or website or title or 'Anon.')
        if year:
            cite += ' | ' + year
        cite += '}}'
    if url:
        cite += (
            ' | accessdate=' +
            datetime.date.strftime(datetime.date.today(), date_format).
            lstrip("0").replace(" 0", " ")
        )
    cite += '}}'
    sfn += '}}'
    return cite, sfn


def reference_tag(dictionary, sfn_template, citation_template):
    """Create named <ref> tag."""
    name = sfn_template[8:-2].replace(' | ', ' ').replace("'", '')
    text = re.sub(
        '( \| ref=({{.*?}}|harv))(?P<repl> \| |}})',
        '\g<repl>',
        citation_template[2:],
    )
    if ' p=' in name and ' | page=' not in text:
        name = name.replace(' p=', ' p. ')
        if 'pages' in dictionary:
            text = text[:-2] + ' | page=' + dictionary['pages'] + '}}'
        else:
            text = text[:-2] + ' | page=}}'
    elif ' pp=' in name:
        name = name.replace(' pp=', ' pp. ')
        if 'pages' in dictionary and ' | pages=' not in text:
            text = text[:-2] + ' | pages=' + dictionary['pages'] + '}}'
    return '<ref name="' + name + '">' + text + '</ref>'


def names2para(names, fn_parameter, ln_parameter, nofn_parameter=None):
    """Take list of names. Return the string to be appended to citation."""
    c = 0
    s = ''
    for name in names:
        c += 1
        if c == 1:
            if name.firstname or not nofn_parameter:
                s += ' | ' + ln_parameter + '=' + name.lastname
                s += ' | ' + fn_parameter + '=' + name.firstname
            else:
                s += ' | ' + nofn_parameter + '=' + name.fullname
        else:
            if name.firstname or not nofn_parameter:
                s += ' | ' + ln_parameter + str(c) + '=' + name.lastname
                s += ' | ' + fn_parameter + str(c) + '=' + name.firstname
            else:
                s += ' | ' + nofn_parameter + str(c) + '=' + name.fullname
    return s


def names1para(translators, para):
    """Take list of names. Return the string to be appended to citation."""
    s = ' | ' + para + '='
    c = 0
    for name in translators:
        c += 1
        if c == 1:
            s += name.fullname
        elif c == len(translators):
            s += ', and ' + name.fullname
        else:
            s += ', ' + name.fullname
    return s
