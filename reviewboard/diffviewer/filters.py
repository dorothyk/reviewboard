import re

from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter

from pygments import token
from pygments.filter import Filter
from pygments.filters import FILTERS


SpellingError = token.Token.SpellingError
token.STANDARD_TYPES[SpellingError] = 'spellerr'


class SpellError(Filter):
    """A Filter for Pygments that check spell errors."""
    def check_line(self, ttype, value):
        """Method called by the filter to check certain type of tokens.

        Change some word's type into Error if it is with spell error.
        """
        spell_checker = SpellChecker("en_US",filters=[EmailFilter,URLFilter])
        spell_checker.set_text(value)
        spell_errors = []

        for err in spell_checker:
            spell_errors.append(err.word)

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
                for ttype, word in self.check_line(ttype, value):
                    yield ttype, word
            else:
                yield ttype, value


FILTERS['spellerror'] = SpellError
