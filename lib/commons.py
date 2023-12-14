from calendar import month_abbr, month_name
from datetime import date as datetime_date, datetime
from functools import partial
from typing import Callable, Optional

import requests
from isbnlib import NotValidISBNError, mask as isbn_mask
from jdatetime import date as jdate
from regex import IGNORECASE, VERBOSE, Match, compile as rc

from config import LANG, NCBI_EMAIL, NCBI_TOOL, SPOOFED_USER_AGENT, USER_AGENT
from lib.generator_en import FOUR_DIGIT_NUM  # noqa: F401

if LANG == 'en':
    from lib.generator_en import sfn_cit_ref
else:
    from lib.generator_fa import sfn_cit_ref


rc = partial(rc, cache_pattern=False)
Search = Callable[[str], Optional[Match[str]]]
# The regex is from:
# http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
DOI_SEARCH: Search = rc(
    r"""
    \b
    10\.[0-9]{4,}+
    (?:\.[0-9]++)*+
    /[^"&\'\s]++
    \b
    """,
    VERBOSE,
).search


b_TO_NUM = {name.lower(): num for num, name in enumerate(month_abbr) if num}
B_TO_NUM = {name.lower(): num for num, name in enumerate(month_name) if num}

jB_TO_NUM = {
    'فروردین': 1,
    'فروردين': 1,
    'اردیبهشت': 2,
    'ارديبهشت': 2,
    'خرداد': 3,
    'تیر': 4,
    'تير': 4,
    'مرداد': 5,
    'شهریور': 6,
    'شهريور': 6,
    'مهر': 7,
    'آبان': 8,
    'آذر': 9,
    'دی': 10,
    'دي': 10,
    'بهمن': 11,
    'اسفند': 12,
}

DOUBLE_DIGIT_SEARCH = rc(r'\d\d').search

# Date patterns:

# January|February...
B = r"""
    (?<B>(?:J(?:anuary|u(?:ne|ly))
    |
    February
    |
    Ma(?:rch|y)
    |
    A(?:pril|ugust)
    |
    (?:(?:(?:Sept|Nov|Dec)em)|Octo)ber))
    """
# فروردین|اردیبهشت|خرداد...
jB = f"(?>(?<jB>{'|'.join([jm for jm in jB_TO_NUM]).replace('ی', '[یي]')}))"
# Month abbreviations:
b = r'(?>(?<b>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)).?'
# Month numbers 0?1-12
m = r'(?<m>0?[1-9]|1[012])'
# Zero padded month numbers 01-12
zm = r'(?<m>0[1-9]|1[012])'
# Day (0?1-31)
d = r'(?<d>0?[1-9]|[12][0-9]|3[01])(?>st|nd|th)?'
# Zero-padded day (01-31)
zd = r'(?<d>0[1-9]|[12][0-9]|3[01])'
# Gregorian year pattern 1900-2099
Y = r'(?<Y>(?:19|20)\d\d)'
ANYDATE_PATTERN = (
    rf'(?:(?:{B}|{b})\ {d},?\ {Y}|{d}\ (?:{B}|{b})\ {Y}|{Y}(?<sep>[-/]){zm}'
    rf'(?P=sep){zd}|(?<d>\d\d?)\ {jB}\ (?<Y>\d\d\d\d))'
)
ANYDATE_SEARCH: Search = rc(ANYDATE_PATTERN, VERBOSE).search
DIGITS_FINDALL = rc(r'\d').findall
MC_SUB = rc(r'MC(\w)', IGNORECASE).sub
LAST_FIRST = partial(rc(r'[,،]').split, maxsplit=1)


AGENT_HEADER = {
    'User-Agent': USER_AGENT,
    # Not required but recommended by
    # https://meta.wikimedia.org/wiki/User-Agent_policy
    'Api-User-Agent': f'{NCBI_TOOL}/{NCBI_EMAIL}',
}
SPOOFED_AGENT_HEADER = {
    'User-Agent': SPOOFED_USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}


urllib3 = requests.packages.urllib3
# Workaround for `[SSL: DH_KEY_TOO_SMALL] dh key too small`.
# https://stackoverflow.com/a/63349178/2705757
urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=0'

REQUEST = partial(requests.request, timeout=20)

# original regex from:
# https://www.debuggex.com/r/0Npla56ipD5aeTr9
# https://www.debuggex.com/r/2s3Wld3CVCR1wKoZ
ISBN_10OR13_SEARCH = rc(
    r'97[89]([ -]?+)(?=\d{1,5}\1?+\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*){9}\d'
    r'|(?=\d{1,5}([ -]?+)\d{1,7}\2?+\d{1,6}\2?+\d)(?:\d\2*+){9}[\dX]'
).search

ISBN10_SEARCH = rc(
    r'(?=\d{1,5}([ -]?+)\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*+){9}[\dX]'
).search

ISBN13_SEARCH = rc(
    r'97[89]([ -]?+)(?=\d{1,5}\1?+\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*+){9}\d'
).search


# original regex from: http://stackoverflow.com/a/14260708/2705757
# ISBN_REGEX = regex_compile(
#     r'(?=[-0-9 ]{17}|[-0-9X ]{13}|[0-9X]{10})(?:97[89][- ]?)'
#     r'?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]'
# )

WS_NORMALIZE = partial(rc(r'\s{2,}').sub, ' ')


class InvalidNameError(ValueError):

    """Base class for RawName exceptions."""


class NumberInNameError(InvalidNameError):

    """Raise when a RawName() contains digits."""


class ReturnError(Exception):
    """Raise to display message to end user.

    Pass sfn, cit, and ref fields as positional args.
    """

    def __init__(self, sfn, cit, ref):
        super().__init__(sfn, cit, ref)


def request(url, spoof=False, method='get', **kwargs) -> requests.Response:
    headers = SPOOFED_AGENT_HEADER if spoof else AGENT_HEADER
    if 'headers' in kwargs:
        headers |= kwargs.pop('headers')
    return REQUEST(method, url, headers=headers, **kwargs)


def dict_to_sfn_cit_ref(dictionary: dict) -> tuple:
    # Return (sfn, cite, ref) strings.
    get = dictionary.get
    if title := get('title'):
        dictionary['title'] = WS_NORMALIZE(title)

    if isbn := get('isbn'):
        try:
            dictionary['isbn'] = isbn_mask(isbn)
        except NotValidISBNError:
            # https://github.com/CrossRef/rest-api-doc/issues/214
            del dictionary['isbn']

    return sfn_cit_ref(dictionary)


def first_last(fullname, separator=None) -> tuple:
    """Return firstname and lastname as a tuple.

    (Jr.|Sr.) suffixes will be considered as part of the firstname.
    Usually called from RawName() class and not used directly.

    Examples:

    >>> first_last('JAMES C. MCKINLEY Jr.', None)
    ('James C. Jr.', 'McKinley')

    >>> first_last('DeBolt, V.', ',')
    ('V.', 'DeBolt')

    The function is more strict if the separator is None:

    >>> first_last('BBC', None)  # InvalidNameError
    >>> first_last('BBC', ',')
    ('', 'BBC')
    """
    fullname = fullname.strip()
    if (
        '\n' in fullname
        or len(fullname) > 40
        # "Jennifer 8. Lee"
        or DOUBLE_DIGIT_SEARCH(fullname)
    ):
        raise InvalidNameError
    if fullname[-4:] in (' Sr.', ' Jr.'):
        suffix = fullname[-4:]
        fullname = fullname[:-4]
    else:
        suffix = None
    if separator is None:
        try:
            lastname, firstname = LAST_FIRST(fullname)
        except ValueError:  # not enough values to unpack, use whitespace
            sname = fullname.split()
            if len(sname) == 1:  # single word first-last with None separator
                raise InvalidNameError
            lastname = sname.pop()
            firstname = ' '.join(sname)
    else:
        if separator in fullname:
            lastname, _, firstname = fullname.partition(separator)
        else:
            lastname, firstname = fullname, ''
    firstname = firstname.strip()
    if (firstname.isupper() and lastname.isupper()) or (
        firstname.islower() and lastname.islower()
    ):
        firstname = firstname.title()
        lastname = lastname.title()
        lastname = MC_SUB(lambda m: 'Mc' + m[1].upper(), lastname)
    if suffix:
        firstname += suffix.title()
    return firstname, lastname


def uninum2en(string) -> str:
    """Convert non-ascii unicode digits to equivalent English ones (0-9).

    Example:
    >>> uninum2en('٤۴৪౪')
    '4444'
    """
    if not string:
        raise ValueError
    digits = set(DIGITS_FINDALL(string))
    for digit in digits:
        string = string.replace(digit, str(int(digit)))
    return string


def find_any_date(str_or_match) -> datetime.date or None:
    """Try to find a date in input string and return it as a date object.

    If there is no matching date, return None.
    The returned date can't be from the future.
    """
    if isinstance(str_or_match, str):
        match = ANYDATE_SEARCH(str_or_match)
    else:
        match = str_or_match
    if not match:
        return None
    groupdict = match.groupdict()
    day = int(groupdict['d'])
    year = int(groupdict['Y'])
    today = datetime.today().date()
    get = groupdict.get

    if (month := get('jB')) is not None:
        date = jdate(year, jB_TO_NUM[month], day).togregorian()
        if date <= today:
            return date
        return

    if (month := get('B')) is not None:
        date = datetime_date(year, B_TO_NUM[month.lower()], day)
        if date <= today:
            return date
        return

    if (month := get('b')) is not None:
        date = datetime_date(year, b_TO_NUM[month.lower()], day)
        if date <= today:
            return date
        return

    if (month := get('m')) is not None:
        date = datetime_date(year, int(month), day)
        if date <= today:
            return date
        return
