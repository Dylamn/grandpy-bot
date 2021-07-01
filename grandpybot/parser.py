import re
import json

from typing import Union
from grandpybot.helpers import base_path


class Parser:
    """The parser used for user questions input.

        Attributes:
            _stopwords (set): A list of words considered as non keywords.
            _punctuation (set): A list which contains punctuation characters.
            _original_string (str): The string which will be parsed.
            _parsed_string (list): The parsed string as a list.
    """
    _stopwords: set

    _original_string: Union[str, None]

    _parsed_string: list

    _punctuation: set = {".", ",", "!", "?", ":", ";"}

    def __init__(self, language: str = 'fr', string=None):
        """Parser constructor

        :param language: The language of the stopwords.
        """
        self._original_string = string
        self._parsed_string = []

        try:
            print("LNG", language)
            with open(base_path(f'stopwords_{language.lower()}.json')) as file:
                self._stopwords = set(json.load(file))
        except IOError:
            self._stopwords = set()

    @property
    def original_string(self):
        """Get the original string."""
        return self._original_string

    @original_string.setter
    def original_string(self, value):
        """Set the original string to be parsed.

        :param value: The string to be parsed.
        """
        self._parsed_string.clear()
        self._original_string = value

    def parse(self, question: Union[str, None] = None):
        """Parse a string and return the considered keywords.

        :param question: The question input.
        """
        if question is not None:
            self.original_string = question
        elif not self.original_string:
            raise ValueError("No string to be parsed.")

        cleaned = self._clean_string(self.original_string)
        pieces = list(dict.fromkeys(cleaned.split()))  # Removes duplicates

        # Finally, remove stopwords...
        self._parsed_string = [
            kw for kw in pieces
            if kw not in self._stopwords
        ]

        return self._parsed_string

    def _clean_string(self, string: str):
        """Clean a string for parsing.

        :param string: The string to clean.
        """
        string = string.lower().strip()
        return self._clean_apostrophe(self._split_punctuation(string))

    def _split_punctuation(self, string):
        """Surround all punctuations characters with spaces.

        :param string:
        :return: str
        """
        # Reserved characters for RegExp which requires escape '\'.
        reserved_chars = {'.', '?'}

        pattern = '|'.join({
            '\\' + char if char in reserved_chars else char
            for char in self._punctuation
        })

        return re.sub(pattern, self._surround_char, string)

    @staticmethod
    def _clean_apostrophe(string):
        """Remove all apostrophes and their prefixed letter.

        :param string: The string on which operates.
        """
        return re.sub(r"[a-zA-Z]+\s*'", '', string)

    @staticmethod
    def _surround_char(match: re.Match, surrounded_by=" "):
        """Surround each regexp match with a given character.

        :param match: The Match object of a regexp.
        :param surrounded_by: the character used to surround the match.
        :return: str
        """
        return match.group(0).replace(
            match.group(0), match.group(0).center(3, surrounded_by)
        )

    def find_address(self, address_keyword='adresse'):
        """Find an extract an address from the parsed string.

        :param address_keyword: A string where an address can follow this one.
        :return: str
        """
        address = ''

        if len(self._parsed_string) < 1 and self.original_string:
            self.parse()

        try:
            i = self._parsed_string.index(address_keyword) + 1
        except ValueError:
            return ''

        for word in self._parsed_string[i:]:
            if word in self._punctuation:
                break
            address += f'{word} '

        return address.rstrip()  # Remove the trailling whitespace on the end.
