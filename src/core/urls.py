from werkzeug.routing import Rule, Map

url_map = Map()


def url(rule, **kwargs):
    def decorated(func):
        kwargs["endpoint"] = func.__name__
        url_map.add(Rule(rule, **kwargs))
        return func

    return decorated
