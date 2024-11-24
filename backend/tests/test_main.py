

from tests.api_setup import client  # type: ignore # noqa: F401


def test_main_status_code():
    response = client.get("/")

    assert response.status_code == 200


def test_main_response():
    response = client.get("/")

    assert response.json() == {"status": "ok"}
