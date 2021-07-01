from flask.testing import FlaskClient


def test_welcome_route(client: FlaskClient):
    rv = client.get('/')
    assert rv.status_code == 200


def test_about_route(client: FlaskClient):
    resp = client.get('/about')
    assert resp.status_code == 200
