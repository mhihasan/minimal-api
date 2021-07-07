from werkzeug.exceptions import MethodNotAllowed


def dispatch(handlers, request, *args, **kwargs):
    try:
        handler = handlers[request.method]
    except KeyError:
        raise MethodNotAllowed(valid_methods=list(handlers.keys()))

    return handler(request, *args, **kwargs)
