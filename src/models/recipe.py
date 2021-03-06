import logging
import os

from mongoengine import Document, StringField, IntField, BooleanField, ListField
from src.utils.db_utils import get_mongodb_name

logger = logging.getLogger(__name__)
logger.setLevel(os.environ["LOG_LEVEL"])

STAGE = os.environ["STAGE"]
COLLECTION_NAME = os.environ.get("RECIPE_COLLECTION_NAME", f"webapp-{STAGE}-recipe")


class Recipe(Document):
    meta = {
        "allow_inheritance": False,
        "collection": COLLECTION_NAME,
        "db_alias": get_mongodb_name(),
        "indexes": ["name"],
        "auto_create_index": False,
    }
    if STAGE == "test":
        meta["auto_create_index"] = True

    name = StringField(required=True)
    difficulty = IntField(default=1, min_value=1, max_value=3)
    vegetarian = BooleanField(default=False)
    prep_time = IntField()
    ratings = ListField(IntField(), default=list)

    def add_rating(self, rating):
        if rating < 1 or rating > 5:
            logger.info(f"Rating {rating} is invalid. It must be between 1 and 5")
            raise ValueError("Rating must be between 1 and 5")
        super().update(add_to_set__ratings=rating)
        self.reload()
        return self

    def update(self, **kwargs):
        super().update(**kwargs)
        self.reload()
        return self
