import requests

from .geocoding import GeocodingMixin


class Google(GeocodingMixin):

    _BASE_URL = "https://maps.googleapis.com"

    def __init__(self, key: str, output: str = 'json') -> None:
        """
        :param key: Maps API key.
        :param output:
        """
        super().__init__()
        self.key = key
        self.output = output

    def _request(self, method: str, uri: str, params: dict) -> requests.Response:
        url = self._BASE_URL + '/' + uri.format(self.output)
        params.setdefault('key', self.key)

        return requests.request(method, url, params=params)
