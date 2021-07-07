import pytest
from mongoengine import disconnect_all, connect
from werkzeug.test import Client
from src.application import create_app
from src.utils.db_utils import get_mongodb_name
from src.core.settings import config

MONGO_TEST_DB = get_mongodb_name()


@pytest.fixture(autouse=True)
def mongodb():
    disconnect_all()
    mongo = config["databases"]["mongodb"]
    connection = connect(
        host=mongo["host"], port=mongo["port"], db=mongo["name"], alias=mongo["name"]
    )
    connection.drop_database(mongo["name"])
    yield
    connection.drop_database(mongo["name"])
    disconnect_all()


@pytest.fixture
def client():
    return Client(create_app(config, test_app=True))
