from random import choice
from typing import Tuple, Union

from grandpybot.wrappers import Google, Wikipedia
from grandpybot.helpers import config, data_get


class GrandpyBot:

    texts = [
        "Je me rappelle, c'était en 1939 : ",
        "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en "
        "culottes courtes ? ",
    ]

    def __init__(self, gmap_key=None):
        gmap_key = gmap_key or config('GMAPS_API_KEY')

        self._maps = Google(key=gmap_key)
        self._wiki = Wikipedia()

    def find_place(self, txt_input: str) -> Tuple[dict, Union[str, None]]:
        """Find the location of a place with google maps.
        """
        result = {}
        street = None

        gmaps_resp = self._maps.geocode(txt_input, region='fr', language='fr')

        if gmaps_resp.get('status', '').upper() == 'OK':
            gmaps_result = data_get(gmaps_resp, 'results.0')

            # Add latitude, longitude and the address to the result.
            result["location"] = data_get(gmaps_result, 'geometry.location', {})
            result["address"] = data_get(gmaps_result, 'formatted_address')

            # Retrieve the street name to perform a search on wikipedia.
            # For example with: 10 Quai de la Charente, 75019 Paris, France
            # We'll get the "Quai de la Charente" substring.
            street = [
                comp['long_name']
                for comp in data_get(gmaps_result, 'address_components')
                if 'route' in comp['types']
            ].pop()
        else:
            result['error'] = {
                'status': 'place_not_found',
                'message': f"Ma mémoire me fait défaut, je ne me rappelle pas de "
                           f"cet endroit."
            }

        return result, street

    def find_wiki_text(self, subject) -> dict:
        wiki_resp = self._wiki.search(subject)

        if not wiki_resp:
            return {
                'error': {
                    'status': 'wiki_not_found',
                    'message': "Je me rappelle seulement de l'emplacement de "
                               "cet endroit. Le voici : "
                }
            }

        return wiki_resp

    def random_text(self):
        """Get a random sentence."""
        return choice(self.texts)
