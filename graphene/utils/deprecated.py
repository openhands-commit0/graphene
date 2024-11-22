import functools
import inspect
import warnings
string_types = (type(b''), type(''))

def warn_deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)

def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    if isinstance(reason, string_types):
        def decorator(func):
            if inspect.isclass(func):
                fmt = "{name} class is deprecated. {reason}"
            else:
                fmt = "{name} function is deprecated. {reason}"

            msg = fmt.format(name=func.__name__, reason=reason)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warn_deprecation(msg)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    elif inspect.isclass(reason) or inspect.isfunction(reason):
        func = reason
        msg = "{} is deprecated.".format(func.__name__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warn_deprecation(msg)
            return func(*args, **kwargs)
        return wrapper
    else:
        raise TypeError(repr(type(reason)))