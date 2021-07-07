import logging
import os

import redis
from werkzeug import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Response, Request
from src.core import settings
from src.views.api import views
from src.core.urls import url_map

logger = logging.getLogger(__name__)


def _init_db(config):
    if config.get("databases") is None:
        return

    for db_type, db_detail in config["databases"].items():
        if db_type == "mongodb":
            from mongoengine import connect

            connect(db_detail["name"], alias=db_detail["name"])


def _init_redis(config):
    if config.get("redis") is None:
        return

    redis_detail = config["redis"]
    redis.Redis(redis_detail["host"], redis_detail["port"])


class App(object):
    def __init__(self, config):
        _init_redis(config)
        _init_db(config)
        self.url_map = url_map

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, request):
        map_adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = map_adapter.match()
            view_funcs = [
                getattr(module, endpoint)
                for module in views
                if hasattr(module, endpoint)
            ]
            if not view_funcs:
                return Response(status=404)

            view_func = view_funcs[0]
            return view_func(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)


def create_app(config, with_static=True):
    app = App(config)
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app,
            {"/static": os.path.join(os.path.dirname(__file__), "../static")},
        )
    return app


if __name__ == "__main__":
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["STAGE"] = "test"
    app = create_app(settings.config)
    run_simple("localhost", 5000, app, use_debugger=True, use_reloader=True)
