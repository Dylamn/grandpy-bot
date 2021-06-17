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

    mock_post.assert_called()

    assert rv.status_code == 200 and json_body['status'] == 'ok'

    # Check if all JSON keys are present.
    for res_k in ['location', 'wiki_text', 'message']:
        assert res_k in json_body

    assert json_body.get("location") == {"lat": 48.8975156, "lng": 2.3833993}
