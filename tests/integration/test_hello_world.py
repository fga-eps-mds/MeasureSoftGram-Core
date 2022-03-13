from src.app import app


def test_hello_world():
    # FIXME - add fixture for app client and other fixtures
    with app.test_client() as client:
        response = client.get("/hello")
        assert response.status_code == 200
        assert response.data == b'{"Hello":"World!"}\n'
