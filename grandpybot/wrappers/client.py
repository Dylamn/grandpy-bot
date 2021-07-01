import requests


class Client:
    """A class used for making HTTP requests."""
    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, base_url: str):
        """

        :param base_url: The base URL
        """
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        self.base_url = base_url

    def _request(self, method: str, uri: str = None, params: dict = None):
        """Send an HTTP request to the API.

        :param method: The HTTP method
        :param uri: The route complement of the base URL.
        :param params: The params to send as a query string or request body
            depending of the HTTP method.
        """
        if method.upper() not in self.METHODS:
            raise ValueError(f'{method} is not a valid HTTP method.')

        if params is None:
            params = {}

        if uri is not None and not uri.startswith('/'):
            uri = f'/{uri}'

        url = self.base_url if not uri else self.base_url + uri

        return requests.request(method, url, params=params)
