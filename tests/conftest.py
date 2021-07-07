import pytest
from mongoengine import disconnect_all, connect, get_db
from werkzeug.test import Client
from src.application import create_app

MONGO_TEST_DB = "webapp-test"


@pytest.fixture(autouse=True)
def mongodb():
    disconnect_all()
    connection = connect(db=MONGO_TEST_DB)
    connection.drop_database(MONGO_TEST_DB)
    yield get_db()
    connection.drop_database(MONGO_TEST_DB)
    disconnect_all()


@pytest.fixture
def client():
    return Client(create_app())
