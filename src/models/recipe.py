import logging
import os

from mongoengine import Document, StringField, IntField, BooleanField, ListField

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

STAGE = os.environ.get("STAGE", "test")
COLLECTION_NAME = os.environ.get("RECIPE_COLLECTION_NAME", f"webapp-{STAGE}-recipe")
DB_NAME = os.environ.get("DB_NAME", f"webapp-{STAGE}")


class Recipe(Document):
    meta = {
        "allow_inheritance": False,
        "collection": COLLECTION_NAME,
        "db_alias": DB_NAME,
        "indexes": ["name"],
        "auto_create_index": False,
    }
    # if STAGE == "test":
    #     meta["auto_create_index"] = True

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
