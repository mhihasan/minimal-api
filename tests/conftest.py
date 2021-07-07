import pytest
from mongoengine import disconnect_all, connect
from werkzeug.test import Client
from src.application import create_app
from src.utils.db_utils import get_mongodb_name

MONGO_TEST_DB = get_mongodb_name()

test_settings = {
    "databases": {"mongodb": {"name": "webapp", "test": {"name": "webapp-test"}}},
    "redis": {"host": "localhost", "port": 6379},
    "env": {"stage": "test", "log_level": "INFO"},
}


@pytest.fixture(autouse=True)
def mongodb():
    disconnect_all()
    connection = connect(db=MONGO_TEST_DB, alias=MONGO_TEST_DB)
    connection.drop_database(MONGO_TEST_DB)
    yield
    connection.drop_database(MONGO_TEST_DB)
    disconnect_all()


@pytest.fixture
def client():
    return Client(create_app(test_settings, test_app=True))
