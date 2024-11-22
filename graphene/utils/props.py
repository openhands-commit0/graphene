class _OldClass:
    pass

class _NewClass:
    pass
_all_vars = set(dir(_OldClass) + dir(_NewClass))

def props(obj):
    """
    Extract all properties from a class or instance.
    Properties are attributes that are not in the base class.
    """
    if isinstance(obj, type):
        # If obj is a class, get its attributes
        attrs = obj.__dict__
    else:
        # If obj is an instance, get its class's attributes
        attrs = obj.__class__.__dict__

    return {
        key: value
        for key, value in attrs.items()
        if key not in _all_vars and not key.startswith('_')
    }