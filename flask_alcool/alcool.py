"""
Base module for auth handling.

"""

from functools import wraps
from flask import current_app, request, abort, url_for


def if_auth_url_for(endpoint, **values):
    """Act like an ``url_for`` unless current context has no rights for the linked page."""
    fun = current_app.view_functions.get(endpoint)
    if fun and (not hasattr(fun, '_auth_fun') or fun._auth_fun(**values)):
        return url_for(endpoint, **values), fun
    return None, None


# These classes are decorators, they can begin with an lowercase letter
class alcool(object):
    """Utility decorator for access control in ``allow_if`` decorators.

    Allowing to write:
    ``@allow_if((Is.admin | Is.in_domain) & ~Is.in_super_domain)``
    given that ``Is`` module functions are decorated by alcool.

    It implements the following operators:

    - ``a & b`` → ``a and b``
    - ``a | b`` → ``a or b``
    - ``a ^ b`` → ``a xor b``
    - ``~ a`` → ``not a``

    """
    def __init__(self, function=lambda context: True):
        self.__name__ = function.__name__
        self.function = function

    def __call__(self, **kwargs):
        """Call the ACL function."""
        kwargs = kwargs or request.view_args or {}
        return self.function(**kwargs)

    def __or__(self, other):
        """Or operator."""
        def result(**kwargs):
            """Closure for the or operator."""
            return self(**kwargs) or other(**kwargs)
        result.__name__ = "%s | %s" % (self.__name__, other.__name__)
        return alcool(result)

    def __ror__(self, other):
        """Right or operator."""
        def result(**kwargs):
            """Closure for the right or operator."""
            return other(**kwargs) or self(**kwargs)
        result.__name__ = "%s | %s" % (other.__name__, self.__name__)
        return alcool(result)

    def __and__(self, other):
        """And operator."""
        def result(**kwargs):
            """Closure for the and operator."""
            return self(**kwargs) and other(**kwargs)
        result.__name__ = "%s & %s" % (self.__name__, other.__name__)
        return alcool(result)

    def __rand__(self, other):
        """Right and operator."""
        def result(**kwargs):
            """Closure for the right and operator."""
            return other(**kwargs) and self(**kwargs)
        result.__name__ = "%s & %s" % (other.__name__, self.__name__)
        return alcool(result)

    def __xor__(self, other):
        """Exclusive or operator."""
        def result(**kwargs):
            """Closure for the exclusive or operator."""
            return (
                self(**kwargs) and not other(**kwargs) or
                other(**kwargs) and not self(**kwargs))
        result.__name__ = "%s ^ %s" % (self.__name__, other.__name__)
        return alcool(result)

    def __rxor__(self, other):
        """Right exclusive or operator."""
        def result(**kwargs):
            """Closure for the right exclusive or operator."""
            return (
                other(**kwargs) and not self(**kwargs) or
                self(**kwargs) and not other(**kwargs))
        result.__name__ = "%s ^ %s" % (other.__name__, self.__name__)
        return alcool(result)

    def __invert__(self):
        """Invert operator."""
        def result(**kwargs):
            """Closure for the invert operator."""
            return not self(**kwargs)
        result.__name__ = "~%s" % self.__name__
        return alcool(result)


class allow_if(object):
    """Check that the global context matches a criteria."""
    def __init__(self, auth_fun):
        self.auth_fun = auth_fun

    def __call__(self, function):
        """Check the global context."""
        @wraps(function)
        def check_auth(*args, **kwargs):
            """Function wrapper."""
            if self.auth_fun():
                return function(*args, **kwargs)
            else:
                abort(403)
        check_auth._auth_fun = self.auth_fun
        return check_auth
