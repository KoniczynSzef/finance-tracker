

from tests.api_setup import client


def test_main():
    response = client.get("/")
    data = response.json()

    assert response.status_code == 200
    assert data == {"status": "ok"}
