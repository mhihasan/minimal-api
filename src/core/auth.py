import functools

from werkzeug.exceptions import Unauthorized

from src.models.user import User


def login_required(view=None, admin_only=False):
    if view is None:
        return functools.partial(login_required, admin_only=admin_only)

    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        user_id = request.headers.get("Authorization")
        if not user_id:
            raise Unauthorized()

        user = User.objects(id=user_id).first()
        if user is None or (admin_only and not user.is_admin):
            raise Unauthorized()

        request.user = user

        return view(request, *args, **kwargs)

    return wrapper
