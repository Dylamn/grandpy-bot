import re

from grandpybot.helpers import data_get
from grandpybot.wrappers.client import Client

_DEFAULT_BASE_URL = 'https://fr.wikipedia.org'


class Wikipedia(Client):
    """Class used for getting texts from wikipedia and format it."""
    def __init__(self):
        super(Wikipedia, self).__init__(base_url=_DEFAULT_BASE_URL)

    def search(self, strinput) -> dict:
        """Perform a query search against the wikipedia API."""
        params = {
            'titles': strinput,
            # static params
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "inprop": "url",
            "exsentences": 3,
            "explaintext": 1,
        }

        resp = self._request(method='GET', uri='/w/api.php', params=params)
        jsonbody = resp.json()

        pages_found = data_get(jsonbody, 'query.pages')

        if "-1" in pages_found:  # -1 means no results
            return {}

        first_page = list(pages_found.values())[0]

        return {
            'wiki_text': self._format_text(data_get(first_page, 'extract', '')),
            'wiki_url': data_get(first_page, 'fullurl', '')
        }

    @staticmethod
    def _format_text(text_) -> str:
        """Format the extracted text from wikipedia

        This method removes the section titles.

        :param text_: The text to format.
        """
        paragraphs = re.split("={2,3}.*={2,3}", text_)

        return " ".join(f_p.strip('\n ') for f_p in paragraphs)
