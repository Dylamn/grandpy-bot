from grandpybot.wrappers.client import Client
from .geocoding import GeocodingMixin

_DEFAULT_BASE_URL = 'https://maps.googleapis.com'


class Google(Client, GeocodingMixin):
    def __init__(self, key: str,
                 base_url: str = _DEFAULT_BASE_URL, output: str = 'json'):
        """
        :param key: Maps API key.
        :param output: The output format of the APIs.
        """
        super().__init__(base_url=base_url)

        self.key = key
        self.output = output

    def _request(self, method: str, uri: str = None, params: dict = None):
        """Send an HTTP request to the API.

        :param method: The HTTP method
        :param uri: The route complement of the base URL.
        :param params: The params to send as a query string or request body
            depending of the HTTP method.
        :return:
        """
        if params is None:
            params = {}

        params.setdefault('key', self.key)
        uri = uri.format(self.output)

        return super(Google, self)._request(method, uri, params)
