import os

import logging

from src.core.auth import login_required
from src.models.user import User
from src.core.response import response
from src.core.urls import url
from src.core.dispatcher import dispatch

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


@login_required
def create_user(request):
    data = request.get_json()
    user = User(**data).save()
    return response(user.to_json())


@url("/users/")
def user_list_endpoint(request):
    return dispatch({"POST": create_user}, request)
