import json

from werkzeug import Response


def response(data=None, status_code=200):
    if isinstance(data, dict):
        data = json.dumps(data)
    return Response(data, status=status_code, content_type="application/json")
