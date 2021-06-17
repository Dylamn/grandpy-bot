from flask import Blueprint, request, current_app as app

from grandpybot.helpers import data_get
from grandpybot.parser import Parser
from grandpybot.wrappers.google import Google
from grandpybot.wrappers.wikipedia import Wikipedia

api = Blueprint("api", __name__, url_prefix='/api')


@api.route('/questions/answer', methods=['POST'])
def ask_question():
    question = request.form.get('user_input')
    parser = Parser(string=question)

    # API wrappers instanciation
    google = Google(key=app.config.get('GMAPS_API_KEY'))
    wiki = Wikipedia()

    subject = parser.find_address()
    answer = {}
    error_msg = ''

    # If answer is not None, we'll call the maps API.
    if subject:
        gmaps_resp = google.geocode(subject, region='fr', language='fr')

        if gmaps_resp.get('status', '').upper() == 'OK':
            gmaps_result = data_get(gmaps_resp, 'results.0')

            # Add latitude and longitude to the final response.
            answer["location"] = data_get(gmaps_result, 'geometry.location', {})

            # Retrieve the street name to perform a search on wikipedia.
            # For example with: 10 Quai de la Charente, 75019 Paris, France
            # We'll get the "Quai de la Charente" substring.
            street = [
                comp['long_name']
                for comp in data_get(gmaps_result, 'address_components')
                if 'route' in comp['types']
            ].pop()

            # call wiki and get the first lines (if there's a result too)
            wiki_text = wiki.search(street)

            if wiki_text:
                # Complete the answer...
                answer.setdefault('wiki_text', wiki_text)

            else:  # Nothing found on wiki.
                error_msg = "Je me rappelle seulement de l'emplacement de cet " \
                            "endroit. Le voici : "
        else:  # Nothing found on maps
            error_msg = f"Ma mémoire me fait défaut, je ne me rappelle pas de " \
                        f"cet endroit."
    else:  # No subject found.
        error_msg = "Je n'ai pas de connaissances sur cet endroit."

    body = {
        "status": "ok",
        "message": error_msg or "Auto msg",
        **answer
    }

    return body, 200
