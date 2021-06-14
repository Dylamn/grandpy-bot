from requests import Response


class GeocodingMixin(object):
    _GEOCODING_URI = 'maps/api/geocode/{0}'

    def _request(self, method: str, url: str, params: dict) -> Response:
        raise NotImplementedError("`_request` method is not overrided in the base class.")

    def geocode(self, address: str = None, region: str = None, language: str = None) -> list:
        """
        GeocodingMixin is the process of converting addresses
        (like ``"1600 Amphitheatre Parkway, Mountain View, CA"``) into geographic
        coordinates (like latitude 37.423021 and longitude -122.083739).

        :param address: The address to geocode.
        :type address: string

        :param region: The region code, specified as a ccTLD ("top-level domain")
            two-character value.
        :type region: string

        :param language: The language in which to return results.
        :type language: string

        :rtype: list of geocoding results.
        """
        params = {}

        if address:
            params["address"] = address

        if region:
            params["region"] = region

        if language:
            params["language"] = language

        return self._request('GET', self._GEOCODING_URI, params).json().get('results', [])
