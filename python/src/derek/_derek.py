import json

from . import _parse

from typing import Optional, Any, Iterable
from . import _typing


class Derek:
    """
    A node in a data structure.

    Contains information about itself, its parent node, and any child nodes.
    """

    # TODO: Add docstrings
    # TODO: Add reload method
    # TODO: Add checkIntegrity method

    def __init__(
        self,
        parent: Optional["Derek"] = None,
        children: Optional[Iterable["Derek"]] = None,
        value: Optional[Any] = None,
        name: Optional[str] = None,
    ) -> "Derek":
        self.parent = parent
        self.children = children
        self.value = value
        self.name = name

    @property
    def parser(self) -> _parse.Parser:
        """
        Return an instance of the parser class.
        """
        return _parse.Parser()

    @classmethod
    def tree(
        cls,
        obj: _typing.JSON,
        parent: Optional["Derek"] = None,
        name: Optional[str] = None,
    ) -> "Derek":
        """
        Create a tree.
        """

        # TODO: return DerekTree (a subclass of Derek) instead of Derek.
        self = cls.__new__(cls)
        children = []

        if isinstance(obj, list):
            # Make child nodes
            children = [cls.tree(item, self) for item in obj]
        elif isinstance(obj, dict):
            # Make child nodes
            children = [cls.tree(item, self) for item in obj.values()]
        else:
            # Not iterable
            children = None

        self.parent = parent
        self.children = children
        self.value = obj
        self.name = name
        return self

    def parse(self, format: str = "oas3") -> _typing.JSON:
        """
        Convert a tree of Derek nodes to a given format.
        """
        format = format.lower()
        if format == "oas3":
            return self.parser.oas3(self)
        else:
            raise NotImplementedError

    def serialize(self, format: str = "oas3") -> str:
        """
        Convert tree to a string.
        """

        j = self.parse(format=format)
        j["example"] = self.example()

        # TODO: handle other formats, not just OAS3
        return json.dumps({self.name or "untitled": j})

    def example(self) -> _typing.JSON:
        """
        Generate example JSON from self.
        """
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
                result = [c if not isinstance(c, Derek) else c.example()]
        elif isinstance(self.value, dict):
            if self.value == {}:
                result = {}
            else:
                result = {
                    k: (v if not isinstance(v, Derek) else v.example())
                    for k, v in zip(self.value.keys(), self.children)
                }
        else:
            result = self.value

        return result
