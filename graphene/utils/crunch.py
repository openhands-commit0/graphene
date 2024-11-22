import json
from collections.abc import Mapping

def crunch(data):
    """
    Transforms data structures into a more compact form by:
    - Converting primitives into single-item lists
    - Converting arrays into a list of values followed by indices
    - Converting objects into a list of values followed by a key-index mapping
    """
    values = []
    value_to_index = {}

    def get_index(value):
        if not isinstance(value, (bool, int, float, str, type(None))):
            value = json.dumps(value, sort_keys=True)
        if value not in value_to_index:
            value_to_index[value] = len(values)
            values.append(value)
        return value_to_index[value]

    def process(obj):
        if isinstance(obj, (bool, int, float, str, type(None))):
            return [obj]
        elif isinstance(obj, list):
            if not obj:
                return [[]]
            indices = []
            for item in obj:
                processed = process(item)
                if len(processed) > 1:
                    indices.append(get_index(processed))
                else:
                    indices.append(get_index(processed[0]))
            result = []
            for i in range(len(values)):
                if isinstance(values[i], str) and values[i].startswith('['):
                    try:
                        array = json.loads(values[i])
                        if array == indices:
                            return values[:i] + [indices]
                    except:
                        pass
            values.append(json.dumps(indices))
            return values
        elif isinstance(obj, Mapping):
            if not obj:
                return [{}]
            obj_indices = {}
            for key, value in sorted(obj.items()):
                processed = process(value)
                if len(processed) > 1:
                    obj_indices[key] = get_index(processed)
                else:
                    obj_indices[key] = get_index(processed[0])
            result = []
            for i in range(len(values)):
                if isinstance(values[i], str) and values[i].startswith('{'):
                    try:
                        mapping = json.loads(values[i])
                        if mapping == obj_indices:
                            return values[:i] + [obj_indices]
                    except:
                        pass
            values.append(json.dumps(obj_indices))
            return values
        return [obj]

    return process(data)