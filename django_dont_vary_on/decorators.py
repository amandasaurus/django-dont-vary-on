# encoding: utf-8
from functools import wraps

def only_vary_on(*new_vary):
    """
    Decorator that changes response to *only* vary on the headers you give.

    Usage:

        @only_vary_on("Accept-Language", "Cookie")
        def myview(request):
            …

    Requires the RemoveUnneededVaryHeadersMiddleware middleware to be used.
    This should not be chained, since each call to this will overwrite any previous
    setting.
    """

    def decorator(func):
        @wraps(func)
        def newfunc(*args, **kwargs):
            response = func(*args, **kwargs)
            response.only_vary_on = new_vary
            return response

        return newfunc

    return decorator

def dont_vary_on(*what_not_to_vary_on):
    """
    Decorator that changes response to mark that certain HTTP headers must not be included in the Vary header

    Usage:

        @dont_vary_on("Cookie", "Accept-Language")
        def myview(request):
            …

    Requires the RemoveUnneededVaryHeadersMiddleware middleware to be used.
    This can be chained, since each call will append the given strings to the
    current value
    """
    def decorator(func):
        @wraps(func)
        def newfunc(*args, **kwargs):
            response = func(*args, **kwargs)
            if hasattr(response, 'dont_vary_on'):
                response.dont_vary_on.extend(what_not_to_vary_on)
            else:
                response.dont_vary_on = list(what_not_to_vary_on)

            return response

        return newfunc

    return decorator

