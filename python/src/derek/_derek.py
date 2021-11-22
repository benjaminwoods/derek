class Derek:
    # TODO: Add docstrings
    # TODO: Add reload method
    # TODO: Add checkIntegrity method
    # TODO: Add typing

    def __init__(self, parent=None, children=None, value=None, name=None):
        self.parent = parent
        self.children = children
        self.value = value
        self.name = name

    @classmethod
    def tree(cls, obj, parent=None, name=None):
        """
        Create a tree.
        """
        self = cls.__new__(cls)
        children = []

        if isinstance(obj, list):
            # Make child nodes
            children = [
                cls.tree(item, self)
                for item in obj
            ]
        elif isinstance(obj, dict):
            # Make child nodes
            children = [
                cls.tree(item, self)
                for item in obj.values()
            ]
        else:
            # Not iterable
            children = None

        self.parent = parent
        self.children = children
        self.value = obj
        self.name = name
        return self
