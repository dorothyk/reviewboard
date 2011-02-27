import re

from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from djblets.siteconfig.models import SiteConfiguration
from pygments import token
from pygments.filter import Filter
from pygments.filters import FILTERS


SpellingError = token.Token.SpellingError
token.STANDARD_TYPES[SpellingError] = 'spellerr'

siteconfig = SiteConfiguration.objects.get_current()
language = siteconfig.get('diffviewer_spell_checking_language')

spell_checker = SpellChecker(language, filters=[EmailFilter,URLFilter])

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
                wtype = SpellingError
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
