from upt import create_app
import pytest

@pytest.fixture
def target():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        return client
