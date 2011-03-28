import re

from djblets.siteconfig.models import SiteConfiguration
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

language = None
spell_checker = None

siteconfig = SiteConfiguration.objects.get_current()
new_lang = siteconfig.get('diffviewer_spell_checking_language')
person_wordlist = siteconfig.get('diffviewer_spell_checking_dir')


class SpellCheckerWithPWL(SpellChecker):
    """Implement a spell checker with personal word list"""
    def __init__(self, pwl=None, *args, **kwargs):
        SpellChecker.__init__(self, *args, **kwargs)
        if pwl is not None:
            self.dict = DictWithPWL(self.lang, pwl)

if language != new_lang:
    language = new_lang
    spell_checker = SpellCheckerWithPWL(lang = language, pwl=person_wordlist,
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
                elif ttype == token.Comment:
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
