from app import app as flask_app

import pytest

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    # app.config['TESTING'] = True
    # app.config['WTF_CSRF_ENABLED'] = False
    return app.test_client()

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'The Email Phishing Detection Service' in res.data
