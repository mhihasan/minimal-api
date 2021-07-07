from src.core.settings import config


def get_mongodb_name(stage="staging"):
    db = config["databases"]["mongodb"]
    return db["test"]["name"] if stage == "test" else db["name"]
