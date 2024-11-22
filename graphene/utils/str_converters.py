import re

def to_camel_case(snake_str):
    """Convert a snake_case string to camelCase."""
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    return components[0] + ''.join(x.capitalize() if x else '_' for x in components[1:])

def to_snake_case(camel_str):
    """Convert a camelCase string to snake_case."""
    pattern = re.compile(r'(?<!^)(?<!_)([A-Z])')
    # Insert underscore before capital letters (except at start or after underscore)
    # and convert to lowercase
    return pattern.sub(r'_\1', camel_str).lower()