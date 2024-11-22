from typing import Type
from ..utils.subclass_with_meta import SubclassWithMeta, SubclassWithMeta_Meta
from ..utils.trim_docstring import trim_docstring

class BaseOptions:
    name = None
    description = None
    _frozen = False

    def __init__(self, class_type):
        self.class_type = class_type

    def __setattr__(self, name, value):
        if not self._frozen:
            super(BaseOptions, self).__setattr__(name, value)
        else:
            raise Exception(f"Can't modify frozen Options {self}")

    def __repr__(self):
        return f'<{self.__class__.__name__} name={repr(self.name)}>'

    def freeze(self):
        """Freeze the options to prevent further modifications."""
        self._frozen = True

BaseTypeMeta = SubclassWithMeta_Meta

class BaseType(SubclassWithMeta):

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, description=None, _meta=None, **_kwargs):
        assert '_meta' not in cls.__dict__, "Can't assign meta directly"
        if not _meta:
            return
        _meta.name = name or cls.__name__
        _meta.description = description or trim_docstring(cls.__doc__)
        _meta.freeze()
        cls._meta = _meta
        super(BaseType, cls).__init_subclass_with_meta__()