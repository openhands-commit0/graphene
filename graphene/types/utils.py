import inspect
from functools import partial
from ..utils.module_loading import import_string
from .mountedtype import MountedType
from .unmountedtype import UnmountedType

def get_type(type_):
    """
    Returns the type for the given type. It can be:
    - A MountedType (which will be returned as is)
    - A UnmountedType (which will be mounted)
    - A Type string (which will be imported and mounted)
    - A callable (which will be called and mounted)
    """
    if isinstance(type_, MountedType):
        return type_
    elif isinstance(type_, UnmountedType):
        return type_.mount()
    elif isinstance(type_, str):
        return import_string(type_)
    elif callable(type_):
        return get_type(type_())
    return type_

def get_field_as(value, _as=None):
    """
    Get type mounted
    """
    if isinstance(value, MountedType):
        return value
    elif isinstance(value, UnmountedType):
        return value.mount(_as)
    return value

def yank_fields_from_attrs(attrs, _as=None, sort=True):
    """
    Extract all the fields in given attributes (dict)
    and return them ordered
    """
    fields = []
    for key, value in attrs.items():
        if isinstance(value, (MountedType, UnmountedType)):
            fields.append((key, get_field_as(value, _as)))
    if sort:
        fields = sorted(fields, key=lambda f: f[1].creation_counter)
    return fields

def get_underlying_type(_type):
    """Get the underlying type even if it is wrapped in structures like NonNull"""
    while hasattr(_type, 'of_type'):
        _type = _type.of_type
    return _type