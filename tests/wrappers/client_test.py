import unittest
from unittest import mock

import pytest

from grandpybot.wrappers.client import Client
from tests.conftest import mocked_responses


class ClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client('https://jsonplaceholder.typicode.com/todos/')

    def test_base_url_trailling_slash_formatting(self):
        self.assertEqual(
            'https://jsonplaceholder.typicode.com/todos', self.client.base_url
        )

    @mock.patch('requests.request', side_effect=mocked_responses)
    def test_http_methods(self, mocked_request):
        http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

        for http_method in http_methods:
            self.client._request(http_method, uri='1')

        with pytest.raises(ValueError):
            self.client._request('DEL')


if __name__ == '__main__':
    unittest.main()
