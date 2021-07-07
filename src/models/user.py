import logging
import os

from mongoengine import Document, StringField, BooleanField

from src.utils.db_utils import get_mongodb_name

logger = logging.getLogger(__name__)
logger.setLevel(os.environ["LOG_LEVEL"])

STAGE = os.environ["STAGE"]
USER_COLLECTION = os.environ.get("USER_COLLECTION", f"webapp-{STAGE}-user")


class User(Document):
    meta = {
        "allow_inheritance": False,
        "collection": USER_COLLECTION,
        "db_alias": get_mongodb_name(),
        "auto_create_index": False,
    }
    if STAGE == "test":
        meta["auto_create_index"] = True

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    is_admin = BooleanField(default=False)
