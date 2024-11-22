from functools import total_ordering

@total_ordering
class OrderedType:
    creation_counter = 1

    def __init__(self, _creation_counter=None):
        self.creation_counter = _creation_counter or self.gen_counter()

    @classmethod
    def gen_counter(cls):
        """Generate a new counter value."""
        counter = cls.creation_counter
        cls.creation_counter += 1
        return counter

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return self.creation_counter == other.creation_counter
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, OrderedType):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, OrderedType):
            return self.creation_counter > other.creation_counter
        return NotImplemented

    def __hash__(self):
        return hash(self.creation_counter)