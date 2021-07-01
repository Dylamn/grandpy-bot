from contextlib import contextmanager

from pytest import fixture
from flask import template_rendered

from grandpybot import create_app


class MockResponse:
    def __init__(self, json_data, status_code: int):
        self.json_data = json_data
        self._status_code = status_code

    def json(self):
        return self.json_data

    @property
    def status_code(self):
        return self._status_code


@fixture
def client():
    """Create a testing client for the flask app.
    """
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def mocked_responses(*args, **kwargs) -> MockResponse:
    """Generates mocked responses of external APIs.

    :return MockResponse:
    """
    if args[1] == "https://maps.googleapis.com/maps/api/geocode/json":
        return MockResponse({
            "results": [
                {
                    "address_components": [
                        {
                            "long_name": "10",
                            "short_name": "10",
                            "types": [
                                "street_number"
                            ]
                        },
                        {
                            "long_name": "Quai de la Charente",
                            "short_name": "Quai de la Charente",
                            "types": [
                                "route"
                            ]
                        },
                        {
                            "long_name": "Paris",
                            "short_name": "Paris",
                            "types": [
                                "locality",
                                "political"
                            ]
                        },
                        {
                            "long_name": "Département de Paris",
                            "short_name": "Département de Paris",
                            "types": [
                                "administrative_area_level_2",
                                "political"
                            ]
                        },
                        {
                            "long_name": "Île-de-France",
                            "short_name": "IDF",
                            "types": [
                                "administrative_area_level_1",
                                "political"
                            ]
                        },
                        {
                            "long_name": "France",
                            "short_name": "FR",
                            "types": [
                                "country",
                                "political"
                            ]
                        },
                        {
                            "long_name": "75019",
                            "short_name": "75019",
                            "types": [
                                "postal_code"
                            ]
                        }
                    ],
                    "formatted_address": "10 Quai de la Charente, "
                                         "75019 Paris, France",
                    "geometry": {
                        "location": {
                            "lat": 48.8975156,
                            "lng": 2.3833993
                        },
                        "location_type": "ROOFTOP",
                        "viewport": {
                            "northeast": {
                                "lat": 48.8988645802915,
                                "lng": 2.384748280291502
                            },
                            "southwest": {
                                "lat": 48.8961666197085,
                                "lng": 2.382050319708498
                            }
                        }
                    },
                    "place_id": "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8",
                    "plus_code": {
                        "compound_code": "V9XM+29 Paris, France",
                        "global_code": "8FW4V9XM+29"
                    },
                    "types": [
                        "establishment",
                        "point_of_interest"
                    ]
                }
            ],
            "status": "OK"
        }, 200)
    elif args[1] == "https://fr.wikipedia.org/w/api.php":
        return MockResponse({
            "batchcomplete": "",
            "query": {
                "pages": {
                    "3120618": {
                        "pageid": 3120618,
                        "ns": 0,
                        "title": "Quai de la Charente",
                        "extract": "Le quai de la Charente est un quai situé le "
                                   "long du canal Saint-Denis, à Paris, dans le "
                                   "19e arrondissement. \n\n\n== Situation et "
                                   "accès ==\nIl fait face au quai de la Gironde."
                                   "\n\n\n== Origine du nom ==\nIl est nommé "
                                   "d'après la Charente, un fleuve français qui "
                                   "donna son nom à deux départements : la "
                                   "Charente (16) et la Charente-Maritime (17).",
                        "contentmodel": "wikitext",
                        "pagelanguage": "fr",
                        "pagelanguagehtmlcode": "fr",
                        "pagelanguagedir": "ltr",
                        "touched": "2021-06-24T10:07:37Z",
                        "lastrevid": 163558565,
                        "length": 1632,
                        "fullurl": "https://fr.wikipedia.org/wiki/Quai_de_la_Charente",
                        "editurl": "https://fr.wikipedia.org/w/index.php?title=Quai_de_la_Charente&action=edit",
                        "canonicalurl": "https://fr.wikipedia.org/wiki/Quai_de_la_Charente"
                    }
                }
            }
        }, 200)

    return MockResponse({
        "status": "not_found", "message": "Route not found"
    }, 404)
