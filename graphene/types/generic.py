from __future__ import unicode_literals
from graphql.language.ast import BooleanValueNode, FloatValueNode, IntValueNode, ListValueNode, ObjectValueNode, StringValueNode
from graphene.types.scalars import MAX_INT, MIN_INT
from .scalars import Scalar

def identity(value):
    """Return the value unchanged."""
    return value

class GenericScalar(Scalar):
    """
    The `GenericScalar` scalar type represents a generic
    GraphQL scalar value that could be:
    String, Boolean, Int, Float, List or Object.
    """
    serialize = identity
    parse_value = identity