class SolObject:
    """
    All data in Sol is an instance of SolObject. SolObjects are created by calling
    `clone()` on another SolObject.
    """
    def __init__(self):
        # The object from which this object was cloned
        self.proto = None

        self.slots = {}

        # Python representation of this object's value. Only used
        # for primitive types like String and Int.
        self.value = id(self)

    def get_slot(self, name):
        if not isinstance(name, str):
            raise Exception('Invalid name argument to get_slot:', name)

        return self.slots.get(name)

    def set_slot(self, name, value):
        if not isinstance(name, str):
            raise Exception('Invalid name argument to set_slot:', name)
        if not isinstance(value, SolObject):
            raise Exception('Invalid value argument to set_slot:', value)

        self.slots[name] = value

    def clone(self):
        clone = SolObject()
        clone.proto = self
        clone.slots = dict(self.slots)
        return clone

    def __repr__(self):
        return '<SolObject {}>'.format(self.value)
