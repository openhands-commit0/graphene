from typing import Any, Optional, Union
from graphql import Undefined
from graphql.language.ast import BooleanValueNode, FloatValueNode, IntValueNode, StringValueNode
from .base import BaseOptions, BaseType
from .unmountedtype import UnmountedType

MAX_INT = 2147483647
MIN_INT = -2147483648

def coerce_int(value: Any) -> Optional[int]:
    """Convert a value to an integer if possible."""
    if value is None or value is Undefined:
        return None
    try:
        num = int(value)
        if num > MAX_INT or num < MIN_INT:
            return None
        return num
    except (TypeError, ValueError):
        return None

def coerce_float(value: Any) -> Optional[float]:
    """Convert a value to a float if possible."""
    if value is None or value is Undefined:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def coerce_string(value: Any) -> Optional[str]:
    """Convert a value to a string if possible."""
    if value is None or value is Undefined:
        return None
    return str(value)

class ScalarOptions(BaseOptions):
    def freeze(self):
        self._frozen = True

class Scalar(UnmountedType, BaseType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums) and are defined with a name and a series of functions
    used to parse input from ast or variables and to ensure validity.
    """

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        _meta = ScalarOptions(cls)
        super(Scalar, cls).__init_subclass_with_meta__(_meta=_meta, **options)
    serialize = None
    parse_value = None
    parse_literal = None

    @classmethod
    def get_type(cls):
        """
        This function is called when the unmounted type (Scalar instance)
        is mounted (as a Field, InputField or Argument)
        """
        return cls

    def mount(self, _as=None):
        """Mount the scalar type as a Field."""
        from .field import Field
        return Field(self.get_type(), *self.args, **self.kwargs)

class Int(Scalar):
    """
    The `Int` scalar type represents non-fractional signed whole numeric
    values. Int can represent values between -(2^53 - 1) and 2^53 - 1 since
    represented in JSON as double-precision floating point numbers specified
    by [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
    """
    serialize = coerce_int
    parse_value = coerce_int

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, IntValueNode):
            return coerce_int(ast.value)
        return None

class BigInt(Scalar):
    """
    The `BigInt` scalar type represents non-fractional whole numeric values.
    `BigInt` is not constrained to 32-bit like the `Int` type and thus is a less
    compatible type.
    """
    serialize = coerce_int
    parse_value = coerce_int

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, IntValueNode):
            return coerce_int(ast.value)
        return None

class Float(Scalar):
    """
    The `Float` scalar type represents signed double-precision fractional
    values as specified by
    [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
    """
    serialize = coerce_float
    parse_value = coerce_float

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (IntValueNode, FloatValueNode)):
            return coerce_float(ast.value)
        return None

class String(Scalar):
    """
    The `String` scalar type represents textual data, represented as UTF-8
    character sequences. The String type is most often used by GraphQL to
    represent free-form human-readable text.
    """
    serialize = coerce_string
    parse_value = coerce_string

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, StringValueNode):
            return ast.value
        return None

class Boolean(Scalar):
    """
    The `Boolean` scalar type represents `true` or `false`.
    """
    serialize = bool
    parse_value = bool

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, BooleanValueNode):
            return ast.value
        return None

class ID(Scalar):
    """
    The `ID` scalar type represents a unique identifier, often used to
    refetch an object or as key for a cache. The ID type appears in a JSON
    response as a String; however, it is not intended to be human-readable.
    When expected as an input type, any string (such as `"4"`) or integer
    (such as `4`) input value will be accepted as an ID.
    """
    serialize = str
    parse_value = str

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (StringValueNode, IntValueNode)):
            return str(ast.value)
        return None