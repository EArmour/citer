"""Provide utilities to convert between language codes and names.

Data Source: http://data.okfn.org/data/core/language-codes

"""

THREE_LETTER_TO_TWO_LETTER_CODE = {
    'aar': 'aa', 'abk': 'ab', 'afr': 'af', 'aka': 'ak', 'alb': 'sq',
    'amh': 'am', 'ara': 'ar', 'arg': 'an', 'arm': 'hy', 'asm': 'as',
    'ava': 'av', 'ave': 'ae', 'aym': 'ay', 'aze': 'az', 'bak': 'ba',
    'bam': 'bm', 'baq': 'eu', 'bel': 'be', 'ben': 'bn', 'bih': 'bh',
    'bis': 'bi', 'bos': 'bs', 'bre': 'br', 'bul': 'bg', 'bur': 'my',
    'cat': 'ca', 'cha': 'ch', 'che': 'ce', 'chi': 'zh', 'chu': 'cu',
    'chv': 'cv', 'cor': 'kw', 'cos': 'co', 'cre': 'cr', 'cze': 'cs',
    'dan': 'da', 'div': 'dv', 'dut': 'nl', 'dzo': 'dz', 'eng': 'en',
    'epo': 'eo', 'est': 'et', 'ewe': 'ee', 'fao': 'fo', 'fij': 'fj',
    'fin': 'fi', 'fre': 'fr', 'fry': 'fy', 'ful': 'ff', 'geo': 'ka',
    'ger': 'de', 'gla': 'gd', 'gle': 'ga', 'glg': 'gl', 'glv': 'gv',
    'gre': 'el', 'grn': 'gn', 'guj': 'gu', 'hat': 'ht', 'hau': 'ha',
    'heb': 'he', 'her': 'hz', 'hin': 'hi', 'hmo': 'ho', 'hrv': 'hr',
    'hun': 'hu', 'ibo': 'ig', 'ice': 'is', 'ido': 'io', 'iii': 'ii',
    'iku': 'iu', 'ile': 'ie', 'ina': 'ia', 'ind': 'id', 'ipk': 'ik',
    'ita': 'it', 'jav': 'jv', 'jpn': 'ja', 'kal': 'kl', 'kan': 'kn',
    'kas': 'ks', 'kau': 'kr', 'kaz': 'kk', 'khm': 'km', 'kik': 'ki',
    'kin': 'rw', 'kir': 'ky', 'kom': 'kv', 'kon': 'kg', 'kor': 'ko',
    'kua': 'kj', 'kur': 'ku', 'lao': 'lo', 'lat': 'la', 'lav': 'lv',
    'lim': 'li', 'lin': 'ln', 'lit': 'lt', 'ltz': 'lb', 'lub': 'lu',
    'lug': 'lg', 'mac': 'mk', 'mah': 'mh', 'mal': 'ml', 'mao': 'mi',
    'mar': 'mr', 'may': 'ms', 'mlg': 'mg', 'mlt': 'mt', 'mon': 'mn',
    'nau': 'na', 'nav': 'nv', 'nbl': 'nr', 'nde': 'nd', 'ndo': 'ng',
    'nep': 'ne', 'nno': 'nn', 'nob': 'nb', 'nor': 'no', 'nya': 'ny',
    'oci': 'oc', 'oji': 'oj', 'ori': 'or', 'orm': 'om', 'oss': 'os',
    'pan': 'pa', 'per': 'fa', 'pli': 'pi', 'pol': 'pl', 'por': 'pt',
    'pus': 'ps', 'que': 'qu', 'roh': 'rm', 'rum': 'ro', 'run': 'rn',
    'rus': 'ru', 'sag': 'sg', 'san': 'sa', 'sin': 'si', 'slo': 'sk',
    'slv': 'sl', 'sme': 'se', 'smo': 'sm', 'sna': 'sn', 'snd': 'sd',
    'som': 'so', 'sot': 'st', 'spa': 'es', 'srd': 'sc', 'srp': 'sr',
    'ssw': 'ss', 'sun': 'su', 'swa': 'sw', 'swe': 'sv', 'tah': 'ty',
    'tam': 'ta', 'tat': 'tt', 'tel': 'te', 'tgk': 'tg', 'tgl': 'tl',
    'tha': 'th', 'tib': 'bo', 'tir': 'ti', 'ton': 'to', 'tsn': 'tn',
    'tso': 'ts', 'tuk': 'tk', 'tur': 'tr', 'twi': 'tw', 'uig': 'ug',
    'ukr': 'uk', 'urd': 'ur', 'uzb': 'uz', 'ven': 've', 'vie': 'vi',
    'vol': 'vo', 'wel': 'cy', 'wln': 'wa', 'wol': 'wo', 'xho': 'xh',
    'yid': 'yi', 'yor': 'yo', 'zha': 'za', 'zul': 'zu'
}

NAME_TO_2LETTER_CODE = {
    'abkhazian': 'ab',
    'afar': 'aa',
    'afrikaans': 'af',
    'akan': 'ak',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'aragonese': 'an',
    'armenian': 'hy',
    'assamese': 'as',
    'avaric': 'av',
    'avestan': 'ae',
    'aymara': 'ay',
    'azerbaijani': 'az',
    'bambara': 'bm',
    'bashkir': 'ba',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bihari languages': 'bh',
    'bislama': 'bi',
    'bokmål, norwegian': 'nb',
    'bosnian': 'bs',
    'breton': 'br',
    'bulgarian': 'bg',
    'burmese': 'my',
    'castilian': 'es',
    'catalan': 'ca',
    'central khmer': 'km',
    'chamorro': 'ch',
    'chechen': 'ce',
    'chewa': 'ny',
    'chichewa': 'ny',
    'chinese': 'zh',
    'chuang': 'za',
    'church slavic': 'cu',
    'church slavonic': 'cu',
    'chuvash': 'cv',
    'cornish': 'kw',
    'corsican': 'co',
    'cree': 'cr',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dhivehi': 'dv',
    'divehi': 'dv',
    'dutch': 'nl',
    'dzongkha': 'dz',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'ewe': 'ee',
    'faroese': 'fo',
    'fijian': 'fj',
    'finnish': 'fi',
    'flemish': 'nl',
    'french': 'fr',
    'fulah': 'ff',
    'gaelic': 'gd',
    'galician': 'gl',
    'ganda': 'lg',
    'georgian': 'ka',
    'german': 'de',
    'gikuyu': 'ki',
    'greek, modern (1453-)': 'el',
    'greenlandic': 'kl',
    'guarani': 'gn',
    'gujarati': 'gu',
    'haitian': 'ht',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hebrew': 'he',
    'herero': 'hz',
    'hindi': 'hi',
    'hiri motu': 'ho',
    'hungarian': 'hu',
    'icelandic': 'is',
    'ido': 'io',
    'igbo': 'ig',
    'indonesian': 'id',
    'interlingua (international auxiliary language association)': 'ia',
    'interlingue': 'ie',
    'inuktitut': 'iu',
    'inupiaq': 'ik',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jv',
    'kalaallisut': 'kl',
    'kannada': 'kn',
    'kanuri': 'kr',
    'kashmiri': 'ks',
    'kazakh': 'kk',
    'kikuyu': 'ki',
    'kinyarwanda': 'rw',
    'kirghiz': 'ky',
    'komi': 'kv',
    'kongo': 'kg',
    'korean': 'ko',
    'kuanyama': 'kj',
    'kurdish': 'ku',
    'kwanyama': 'kj',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'letzeburgesch': 'lb',
    'limburgan': 'li',
    'limburger': 'li',
    'limburgish': 'li',
    'lingala': 'ln',
    'lithuanian': 'lt',
    'luba-katanga': 'lu',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maldivian': 'dv',
    'maltese': 'mt',
    'manx': 'gv',
    'maori': 'mi',
    'marathi': 'mr',
    'marshallese': 'mh',
    'moldavian': 'ro',
    'moldovan': 'ro',
    'mongolian': 'mn',
    'nauru': 'na',
    'navaho': 'nv',
    'navajo': 'nv',
    'ndebele, north': 'nd',
    'ndebele, south': 'nr',
    'ndonga': 'ng',
    'nepali': 'ne',
    'north ndebele': 'nd',
    'northern sami': 'se',
    'norwegian': 'no',
    'norwegian bokmål': 'nb',
    'norwegian nynorsk': 'nn',
    'nuosu': 'ii',
    'nyanja': 'ny',
    'nynorsk, norwegian': 'nn',
    'occidental': 'ie',
    'occitan (post 1500)': 'oc',
    'ojibwa': 'oj',
    'old bulgarian': 'cu',
    'old church slavonic': 'cu',
    'old slavonic': 'cu',
    'oriya': 'or',
    'oromo': 'om',
    'ossetian': 'os',
    'ossetic': 'os',
    'pali': 'pi',
    'panjabi': 'pa',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'provençal': 'oc',
    'punjabi': 'pa',
    'pushto': 'ps',
    'quechua': 'qu',
    'romanian': 'ro',
    'romansh': 'rm',
    'rundi': 'rn',
    'russian': 'ru',
    'samoan': 'sm',
    'sango': 'sg',
    'sanskrit': 'sa',
    'sardinian': 'sc',
    'scottish gaelic': 'gd',
    'serbian': 'sr',
    'shona': 'sn',
    'sichuan yi': 'ii',
    'sindhi': 'sd',
    'sinhala': 'si',
    'sinhalese': 'si',
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'sotho, southern': 'st',
    'south ndebele': 'nr',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swati': 'ss',
    'swedish': 'sv',
    'tagalog': 'tl',
    'tahitian': 'ty',
    'tajik': 'tg',
    'tamil': 'ta',
    'tatar': 'tt',
    'telugu': 'te',
    'thai': 'th',
    'tibetan': 'bo',
    'tigrinya': 'ti',
    'tonga (tonga islands)': 'to',
    'tsonga': 'ts',
    'tswana': 'tn',
    'turkish': 'tr',
    'turkmen': 'tk',
    'twi': 'tw',
    'uighur': 'ug',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uyghur': 'ug',
    'uzbek': 'uz',
    'valencian': 'ca',
    'venda': 've',
    'vietnamese': 'vi',
    'volapük': 'vo',
    'walloon': 'wa',
    'welsh': 'cy',
    'western frisian': 'fy',
    'wolof': 'wo',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zhuang': 'za',
    'zulu': 'zu'
}

TO_TWO_LETTER_CODE = {
    **NAME_TO_2LETTER_CODE, **THREE_LETTER_TO_TWO_LETTER_CODE
}.get
