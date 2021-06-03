from flask import Blueprint, request

api = Blueprint("api", __name__, url_prefix='/api')


@api.route('/ask-question', methods=['POST'])
def ask_question():
    return {
        "answer":  'Replied with: ' + request.form.get('user_input')
    }, 200
