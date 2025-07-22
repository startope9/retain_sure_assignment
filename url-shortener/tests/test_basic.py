import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app
from app.models import url_store

@pytest.fixture(autouse=True)
def clear_store():
    # Reset in-memory store before each test
    url_store._data.clear()
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy", "service": "URL Shortener API"}

def test_shorten_and_redirect_and_stats_flow(client):
    # Shorten a valid URL
    res = client.post('/api/shorten', json={"url": "https://example.com/page"})
    assert res.status_code == 201
    body = res.get_json()
    assert "short_code" in body and len(body["short_code"]) == 6
    code = body["short_code"]
    # Redirect (should increment click count)
    res2 = client.get(f'/{code}')
    assert res2.status_code == 302
    assert res2.location == "https://example.com/page"
    # Stats should show 1 click
    stats = client.get(f'/api/stats/{code}')
    data = stats.get_json()
    assert stats.status_code == 200
    assert data["url"] == "https://example.com/page"
    assert data["clicks"] == 1
    assert "created_at" in data

def test_redirect_404_for_unknown_code(client):
    res = client.get('/nonexist')
    assert res.status_code == 404

def test_stats_404_for_unknown_code(client):
    res = client.get('/api/stats/nonexist')
    assert res.status_code == 404

def test_invalid_url_shorten(client):
    res = client.post('/api/shorten', json={"url": "not_a_url"})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid URL"

def test_missing_url_field(client):
    res = client.post('/api/shorten', json={})
    assert res.status_code == 400
    assert 'Missing' in res.get_json()["error"]
