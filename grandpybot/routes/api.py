from flask import Blueprint, request, current_app as app

from grandpybot.helpers import data_get
from grandpybot.parser import Parser
from grandpybot.wrappers.google import Google
from grandpybot.wrappers.wikipedia import Wikipedia

api = Blueprint("api", __name__, url_prefix='/api')


@api.route('/ask-question', methods=['POST'])
def ask_question():
    question = request.form.get('user_input')
    parser = Parser(string=question)

    # API wrappers instanciation
    google = Google(key=app.config.get('GMAPS_API_KEY'))
    wiki = Wikipedia()

    subject = parser.find_address()
    answer = None

    # If answer is not None, we'll call the maps API.
    if subject:
        # Then if maps returns a result, call wiki and get the first lines (if there's a result too)
        gmaps_result = google.geocode(subject, region='fr', language='fr')

        if gmaps_result:
            lat, lng = data_get(gmaps_result[0], 'geometry.location').values()
            street = [
                comp['long_name'] for comp in data_get(gmaps_result, '0.address_components')
                if 'route' in comp['types']
            ].pop()

            wiki_response = wiki.search(street)

            if wiki_response:
                wiki_text = data_get(wiki_response.json(), 'query.pages')

                # Complete the answer...
                answer = next(iter(wiki_text.values()))['extract']

            else:
                # Nothing found on wiki, simply answer with the address only.
                answer = data_get(gmaps_result[0], 'formatted_address')

        else:
            # Nothing found on maps
            answer = f"Ma mémoire me fait défaut ou bien je ne connais pas l'adresse."

    body = {
        'answer': answer or "I don't understand, i'm sorry! :("
    }

    return body, 200
