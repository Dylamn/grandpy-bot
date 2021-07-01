import os
import unittest
from unittest import mock
from pathlib import Path

import pytest

from grandpybot.helpers import base_path, data_get, config


class HelpersTest(unittest.TestCase):
    # region base_path helper tests
    def testBasePath(self):
        bpath = base_path()

        self.assertTrue(bpath.endswith('grandpy-bot'))

    def test_base_path_append_relative_path(self):
        brpath = base_path('tests')
        expected_end = f'grandpy-bot{os.sep}tests'

        self.assertTrue(brpath.endswith(expected_end))

    @mock.patch('pathlib.Path.resolve', return_value='/home/user/foo/gp-bot')
    def test_base_path_project_dir_not_found(self, mocked_path: mock.MagicMock):
        with pytest.raises(EnvironmentError):
            mocked_path.assert_not_called()
            base_path('tests')

        mocked_path.assert_called_once()

    def test_base_path_recursive(self):
        fake_path = Path('/home/user/foo/bar/grandpy-bot/grandpybot/routes')

        with mock.patch('pathlib.Path.resolve', return_value=fake_path):
            bpath = base_path()

            self.assertTrue(bpath.endswith('grandpy-bot'))

    # endregion

    def test_data_get(self):
        json_content = {
            "posts": [
                {
                    "id": 1,
                    "name": "Foo",
                    "published": True
                },
                {
                    "id": 2,
                    "name": "Bar",
                    "published": False
                }
            ]
        }

        self.assertEqual(data_get(json_content, 'posts.0.name'), 'Foo')
        self.assertEqual(data_get(json_content, 'bar', 'default'), 'default')
        self.assertEqual(data_get(json_content, 'posts.1.published'), False)
        self.assertEqual(data_get(json_content, None), json_content)


if __name__ == '__main__':
    unittest.main()
