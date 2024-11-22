from functools import wraps
from .deprecated import deprecated

@deprecated('resolve_only_args decorator is deprecated. Use normal resolver function instead.')
def resolve_only_args(resolver):
    """
    This function wraps a resolver to only pass root and args,
    disregarding info and context (info=None).
    """
    @wraps(resolver)
    def wrapped_resolver(root, info, **args):
        return resolver(root, **args)
    return wrapped_resolver