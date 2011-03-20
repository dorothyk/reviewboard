import re

from enchant import DictWithPWL
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from pygments import token
from pygments.filter import Filter
from pygments.filters import FILTERS


SSpellingError = token.Token.SSpellingError
CSpellingError = token.Token.CSpellingError
token.STANDARD_TYPES[SSpellingError] = 's_spellerr'
token.STANDARD_TYPES[CSpellingError] = 'c_spellerr'

siteconfig = SiteConfiguration.objects.get_current()
language = siteconfig.get('diffviewer_spell_checking_language')


class SpellCheckerWithPWL(SpellChecker):
    """Implement a spell checker with personal word list"""
    def __init__(self, lang=None, pwl=None, text=None,
                 tokenize=None, chunker=None, filters=None):
        """Constructor for the SpellChckerWithPWl class"""
        SpellChecker.__init__(self, lang, text, tokenize, chunker, filters)
        if pwl is not None:
            self.dict = DictWithPWL(lang, pwl)

spell_checker = SpellCheckerWithPWL(language,
                                    pwl='./diffviewer/LocalDictionary.txt',
                                    filters=[EmailFilter,URLFilter])


class SpellError(Filter):
    """A Filter for Pygments that check spell errors."""
    def check_line(self, ttype, value):
        """Method called by the filter to check certain type of tokens.

        Change some word's type into Error if it is with spell error.
        """
        spell_checker.set_text(value)
        spell_errors = [err.word for err in spell_checker]

        string = re.split('(\W+)', value)
        result = []

        for word in string:
            if word in spell_errors:
                if ttype == token.String:
                    wtype = SSpellingError
                else:
                    wtype = CSpellingError
            else:
                wtype = ttype

            result.append((wtype, word))

        return result

    def filter(self, lexer, stream):
        """The filter only check spell for string and comment."""
        for ttype, value in stream:
            if ttype is token.String or ttype is token.Comment:
                for val in self.check_line(ttype, value):
                    yield val
            else:
                yield ttype, value


FILTERS['spellerror'] = SpellError
