from src.core.settings import config


def get_mongodb_name():
    return config["databases"]["mongodb"]["name"]
