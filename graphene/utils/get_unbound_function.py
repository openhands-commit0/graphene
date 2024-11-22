def get_unbound_function(func):
    """
    Get the unbound function from a bound method or function.
    This is useful when we want to get the original function from a method
    that has been bound to a class instance.
    """
    if hasattr(func, "__func__"):
        return func.__func__
    return func
