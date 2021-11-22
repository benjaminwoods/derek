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

    def example(self):
        # TODO: don't assume that all of the child nodes are of the same
        # type.

        if isinstance(self.value, list):
            if self.value == []:
                result = []
            else:
                c = self.children[0]
                if isinstance(c, Derek):
                    v = c.example()
                else:
                    v = c
                result = [
                    c if not isinstance(c, Derek)
                    else c.example()
                ]
        elif isinstance(self.value, dict):
            if self.value == {}:
                result = {}
            else:
                result = {
                    k: (v if not isinstance(v, Derek)
                    else v.example()) for k,v in zip(
                        self.value.keys(),
                        self.children
                    )
                }
        else:
            result = self.value

        return result
