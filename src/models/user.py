import logging
import os

from mongoengine import Document, StringField, BooleanField

from src.utils.db_utils import get_mongodb_name

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

STAGE = os.environ.get("STAGE", "test")
USER_COLLECTION = os.environ.get("USER_COLLECTION", f"webapp-{STAGE}-user")
MONGODB_NAME = get_mongodb_name(STAGE)


class User(Document):
    meta = {
        "allow_inheritance": False,
        "collection": USER_COLLECTION,
        "db_alias": MONGODB_NAME,
        "auto_create_index": False,
    }
    if STAGE == "test":
        meta["auto_create_index"] = True

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    is_admin = BooleanField(default=False)
