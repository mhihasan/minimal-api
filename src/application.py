import logging
import os

from werkzeug import run_simple
from werkzeug.exceptions import HTTPException
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

            if config.get("test_app"):
                connect(db_detail["test"]["name"], alias=db_detail["test"]["name"])
            else:
                connect(db_detail["name"], alias=db_detail["name"])


def _init_redis(config):
    if config.get("redis") is None:
        return

    import redis

    redis_detail = config["redis"]
    redis.Redis(redis_detail["host"], redis_detail["port"])


def _setup_env(config):
    os.environ["LOG_LEVEL"] = config.get("log_level", "INFO")
    os.environ["STAGE"] = config.get("stage", "test")


class App(object):
    def __init__(self, config):
        _init_redis(config)
        _init_db(config)
        _setup_env(config)
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


def create_app(config=None, test_app=True):
    if config is None:
        config = {}
    config.update({"test_app": test_app})
    app = App(config)
    return app


if __name__ == "__main__":
    app = create_app(settings.config, test_app=False)
    run_simple("localhost", 5000, app, use_debugger=True, use_reloader=True)
