import pytest

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'The Email Phishing Detection Service' in res.data
