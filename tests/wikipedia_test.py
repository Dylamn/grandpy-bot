import unittest
from unittest import mock

from grandpybot.wrappers.wikipedia import Wikipedia
from .conftest import mocked_responses


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.wiki = Wikipedia()

    @mock.patch('requests.request', side_effect=mocked_responses)
    def test_something(self, mocked_get: mock.MagicMock):
        result = self.wiki.search('Quai de la Charente')
        mocked_get.assert_called()

        expectedtext = "Le quai de la Charente est un quai situé le long du " \
                       "canal Saint-Denis, à Paris, dans le 19e arrondissement." \
                       " Il fait face au quai de la Gironde. Il est nommé " \
                       "d'après la Charente, un fleuve français qui donna son " \
                       "nom à deux départements : " \
                       "la Charente (16) et la Charente-Maritime (17)."

        assert result == expectedtext


if __name__ == '__main__':
    unittest.main()
