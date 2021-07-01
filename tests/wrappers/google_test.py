import unittest
from unittest import mock
from os import getenv

from dotenv import load_dotenv

from tests.conftest import mocked_responses
from grandpybot.helpers import data_get
from grandpybot.wrappers import Google


class GoogleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Load .env variables in the environment.
        load_dotenv()

    def setUp(self) -> None:
        self.google = Google(getenv('GOOGLE_MAPS_API_KEY'))

    @mock.patch('requests.request', side_effect=mocked_responses)
    def test_get_place(self, mocked_get: mock.MagicMock):
        mocked_get.assert_not_called()
        result = self.google.geocode('OpenClassrooms', 'fr', 'fr')
        mocked_get.assert_called_once()

        self.assertEqual('OK', result['status'])
        self.assertIn('results', result)
        self.assertEqual(
            "10 Quai de la Charente, 75019 Paris, France",
            data_get(result, 'results.0.formatted_address')
        )
