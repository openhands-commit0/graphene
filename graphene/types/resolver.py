def dict_or_attr_resolver(attname, default_value, root, info, **args):
    """
    Default resolver that tries to get the value from:
    1. The root dict (if root is a dict)
    2. An attribute of root
    3. Default value if nothing is found
    """
    if isinstance(root, dict):
        return root.get(attname, default_value)
    return getattr(root, attname, default_value)

default_resolver = dict_or_attr_resolver

def get_default_resolver():
    """Get the default resolver function."""
    return default_resolver