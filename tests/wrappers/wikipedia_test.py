import unittest
from unittest import mock

from grandpybot.wrappers.wikipedia import Wikipedia
from tests.conftest import mocked_responses


class WikipediaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wiki = Wikipedia()

    @mock.patch('requests.request', side_effect=mocked_responses)
    def test_extracted_url(self, mocked_get: mock.MagicMock):
        result = self.wiki.search('Quai de la Charente')
        mocked_get.assert_called()

        expected_url = 'https://fr.wikipedia.org/wiki/Quai_de_la_Charente'

        assert 'wiki_url' in result and result['wiki_url'] == expected_url

    @mock.patch('requests.request', side_effect=mocked_responses)
    def test_extracted_text(self, mocked_get: mock.MagicMock):
        result = self.wiki.search('Quai de la Charente')
        mocked_get.assert_called()

        expectedtext = "Le quai de la Charente est un quai situé le long du " \
                       "canal Saint-Denis, à Paris, dans le 19e arrondissement." \
                       " Il fait face au quai de la Gironde. Il est nommé " \
                       "d'après la Charente, un fleuve français qui donna son " \
                       "nom à deux départements : " \
                       "la Charente (16) et la Charente-Maritime (17)."

        assert "wiki_text" in result and result["wiki_text"] == expectedtext


if __name__ == '__main__':
    unittest.main()
