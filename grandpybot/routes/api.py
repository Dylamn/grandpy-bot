from flask import Blueprint, request

from grandpybot.parser import Parser
from grandpybot.grandpy import GrandpyBot

api = Blueprint("api", __name__, url_prefix='/api')


@api.route('/questions/answer', methods=['POST'])
def ask_question():
    question = request.form.get('user_input')
    answer = {}
    grandpy = GrandpyBot()
    parser = Parser(string=question)

    # Parse the input
    subject = parser.find_address()

    if subject:
        map_result, street = grandpy.find_place(subject)
        # Add the results of google maps to the answer
        answer.update(map_result)

        if street:
            wiki_result = grandpy.find_wiki_text(street)
            answer.update(wiki_result)

    else:  # No subject parsed
        answer['error'] = {
            'status': 'subject_not_found',
            'message': "Excusez-moi mais je n'ai pas compris votre question."
        }

    # Create the response which will be sent to the client.
    # A unsuccessful response as always 'error' as the outermost key.
    body, http_code = (answer, 400) if 'error' in answer else ({
        'status': 'ok',
        'message': grandpy.random_text(),
        **answer,
    }, 200)

    return body, http_code
