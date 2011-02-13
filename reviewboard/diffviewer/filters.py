import re

from pygments import token
from pygments.filter import Filter
from pygments.filters import FILTERS

from pyaspell import AspellLinux


SpellingError = token.Token.SpellingError
token.STANDARD_TYPES[SpellingError] = 'spellerr'


class SpellError(Filter):
    """A Filter for Pygments that check spell errors."""
    def check_line(self, ttype, value):
        """Method called by the filter to check certain type of tokens.
        
        Only words consisted of letters are checked.
        Change some word's type into Error if it is with spell error.
        """
        spell_checker = AspellLinux(("lang", "en"))
        result = []
        string = re.split('(\W+)', value)
        words = re.findall('[a-zA-Z]+', value)

        for word in string:
            if word in words and not spell_checker.check(str(word)):
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
