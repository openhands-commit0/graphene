from itertools import chain
from graphql import Undefined
from .dynamic import Dynamic
from .mountedtype import MountedType
from .structures import NonNull
from .utils import get_type

def to_arguments(args, extra_args=None):
    """
    Convert arguments to a list of Argument instances.
    """
    from .unmountedtype import UnmountedType

    extra_args = extra_args or {}
    arguments = []

    for name, value in chain(args.items(), extra_args.items()):
        if isinstance(value, Argument):
            argument = value
            if argument.name is None:
                argument.name = name
        elif isinstance(value, (UnmountedType, Dynamic)):
            argument = Argument(value, name=name)
        else:
            raise ValueError(f'Unknown argument "{name}" of type {type(value)}')
        arguments.append(argument)

    return sorted(arguments, key=lambda x: x.creation_counter)

class Argument(MountedType):
    """
    Makes an Argument available on a Field in the GraphQL schema.

    Arguments will be parsed and provided to resolver methods for fields as keyword arguments.

    All ``arg`` and ``**extra_args`` for a ``graphene.Field`` are implicitly mounted as Argument
    using the below parameters.

    .. code:: python

        from graphene import String, Boolean, Argument

        age = String(
            # Boolean implicitly mounted as Argument
            dog_years=Boolean(description="convert to dog years"),
            # Boolean explicitly mounted as Argument
            decades=Argument(Boolean, default_value=False),
        )

    args:
        type (class for a graphene.UnmountedType): must be a class (not an instance) of an
            unmounted graphene type (ex. scalar or object) which is used for the type of this
            argument in the GraphQL schema.
        required (optional, bool): indicates this argument as not null in the graphql schema. Same behavior
            as graphene.NonNull. Default False.
        name (optional, str): the name of the GraphQL argument. Defaults to parameter name.
        description (optional, str): the description of the GraphQL argument in the schema.
        default_value (optional, Any): The value to be provided if the user does not set this argument in
            the operation.
        deprecation_reason (optional, str): Setting this value indicates that the argument is
            depreciated and may provide instruction or reason on how for clients to proceed. Cannot be
            set if the argument is required (see spec).
    """

    def __init__(self, type_, default_value=Undefined, deprecation_reason=None, description=None, name=None, required=False, _creation_counter=None):
        super(Argument, self).__init__(_creation_counter=_creation_counter)
        if required:
            assert deprecation_reason is None, f'Argument {name} is required, cannot deprecate it.'
            type_ = NonNull(type_)
        self.name = name
        self._type = type_
        self.default_value = default_value
        self.description = description
        self.deprecation_reason = deprecation_reason

    def __eq__(self, other):
        return isinstance(other, Argument) and (self.name == other.name and self.type == other.type and (self.default_value == other.default_value) and (self.description == other.description) and (self.deprecation_reason == other.deprecation_reason))