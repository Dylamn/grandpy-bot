from unittest import mock

from flask.testing import FlaskClient

from .conftest import mocked_responses


@mock.patch('requests.request', side_effect=mocked_responses)
def test_bot_answer(mock_post: mock.MagicMock, client: FlaskClient):
    rv = client.post('/api/questions/answer', data={
        "user_input": "Salut GrandPy ! Est-ce que tu connais, "
                      "par hasard, l'adresse d'OpenClassrooms ?"
    })
    json_body = rv.get_json()

    # Assert that the Fake HTTP call has been made.
    mock_post.assert_called()

    assert rv.status_code == 200 and json_body['status'] == 'ok'

    # All outermost keys that should be present in the JSON body.
    response_keys = [
        'location', 'message', 'wiki_text', 'wiki_url', 'address', 'status',
    ]

    # Check if all JSON keys are present.
    for response_key in response_keys:
        assert response_key in json_body

    assert json_body.get("location") == {"lat": 48.8975156, "lng": 2.3833993}
