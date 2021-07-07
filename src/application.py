import logging
import os

from werkzeug import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response, Request
from src.core import settings
from src.views.api import views
from src.core.urls import url_map

logger = logging.getLogger(__name__)


def _init_db(databases, test_app=True):
    if databases is None:
        return

    for db_type, db_detail in databases.items():
        if db_type == "mongodb":
            from mongoengine import connect

            connect(
                host=db_detail["host"],
                port=db_detail["port"],
                db=db_detail["name"],
                alias=db_detail["name"],
            )


def _init_redis(redis_conf):
    if redis_conf is None:
        return

    import redis

    redis.Redis(redis_conf["host"], redis_conf["port"])


def _setup_env(env):
    if env is None:
        return
    os.environ["LOG_LEVEL"] = env.get("log_level", "INFO")
    os.environ["STAGE"] = env.get("stage", "test")


class App(object):
    def __init__(self, config):
        _init_redis(config.get("redis"))
        _init_db(config.get("databases"))
        _setup_env(config.get("env"))
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
    run_simple("", 5000, app, use_debugger=True, use_reloader=True)
