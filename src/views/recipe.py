import os

from bson import json_util
from werkzeug.exceptions import NotFound
import logging
from src.models.recipe import Recipe
from src.core.auth import login_required
from src.core.response import response
from src.core.urls import url
from src.core.dispatcher import dispatch

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def list_recipe(request):
    query_params = request.args

    if query_params:
        recipes = Recipe.objects(**query_params)
    else:
        recipes = [recipe.to_mongo() for recipe in Recipe.objects.all()]

    return response(json_util.dumps(recipes))


@login_required
def create_recipe(request):
    data = request.get_json()
    name = data["name"]
    difficulty = data["difficulty"]
    prep_time = data["prep_time"]

    recipe = Recipe(name=name, difficulty=difficulty, prep_time=prep_time).save()
    return response(recipe.to_json())


@login_required
def update_recipe(request, recipe_id):
    data = request.get_json()
    if data.get("rating"):
        logger.info("Rating cannot be changed")
        data.pop("rating")

    Recipe.objects(id=recipe_id).update_one(**data, full_result=True)
    return response(data)


@login_required
def delete_recipe(request, recipe_id):
    Recipe.objects(id=recipe_id).delete()
    return response(status_code=204)


def get_recipe_detail(request, recipe_id):
    recipe = Recipe.objects(id=recipe_id).first()
    if recipe is None:
        raise NotFound()
    return response(recipe.to_json())


def add_recipe_rating(request, recipe_id):
    data = request.get_json()
    rating = data["rating"]

    Recipe(id=recipe_id).add_rating(rating)
    return response(data)


@url("/recipes/")
def recipe_list_endpoint(request):
    return dispatch({"GET": list_recipe, "POST": create_recipe}, request)


@url("/recipes/<recipe_id>/")
def recipe_detail_endpoint(request, recipe_id):
    return dispatch(
        {
            "GET": get_recipe_detail,
            "DELETE": delete_recipe,
            "PATCH": update_recipe,
            "PUT": update_recipe,
        },
        request,
        recipe_id,
    )


@url("/recipes/<recipe_id>/rating")
def recipe_rating_endpoint(request, recipe_id):
    return dispatch({"POST": add_recipe_rating}, request, recipe_id)
