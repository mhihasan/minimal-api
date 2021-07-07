import logging
import os

from mongoengine import Document, StringField, BooleanField

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

STAGE = os.environ.get("STAGE", "test")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", f"webapp-{STAGE}-user")
DB_NAME = os.environ.get("DB_NAME", f"webapp-{STAGE}")


class User(Document):
    meta = {
        "allow_inheritance": False,
        "collection": COLLECTION_NAME,
        "db_alias": DB_NAME,
        "auto_create_index": False,
    }
    if STAGE == "test":
        meta["auto_create_index"] = True

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    is_admin = BooleanField(default=False)
