import requests


class Wikipedia:
    _BASE_URL = 'https://fr.wikipedia.org/w/api.php'

    def _request(self, method: str, uri: str = None, params=None) -> requests.Response:
        """Perform an HTTP request."""
        if params is None:
            params = {}

        url = self._BASE_URL if not uri else self._BASE_URL + uri

        return requests.request(method, url, params=params)

    def search(self, strinput) -> requests.Response:
        """Perform a query search against the wikipedia API."""
        params = {
            'titles': strinput,
            # static params
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "explaintext": 1,
        }

        return self._request('GET', params=params)
