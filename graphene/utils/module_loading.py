from functools import partial
from importlib import import_module

def import_string(dotted_path, dotted_attributes=None):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. When a dotted attribute path is also provided, the
    dotted attribute path would be applied to the attribute/class retrieved from
    the first step, and return the corresponding value designated by the
    attribute path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        module = import_module(module_path)
    except ImportError as err:
        raise ImportError('Module "%s" does not exist' % module_path) from err

    try:
        attribute = getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err

    if dotted_attributes:
        try:
            for attr in dotted_attributes.split('.'):
                attribute = getattr(attribute, attr)
        except AttributeError as err:
            raise ImportError('Object "%s" does not have attribute "%s"' % (attribute, dotted_attributes)) from err

    return attribute

def lazy_import(dotted_path, dotted_attributes=None):
    """
    Lazy version of import_string that returns a proxy object that imports the module
    only when needed.
    """
    return partial(import_string, dotted_path, dotted_attributes)