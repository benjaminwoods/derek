import json
from copy import deepcopy as dcp

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
        parent: Optional[_typing.DerekType] = None,
        children: Optional[Iterable[_typing.DerekType]] = None,
        value: Optional[Any] = None,
        name: Optional[str] = None,
    ):
        self.parent = parent
        self.children = children
        self.value = value
        self.name = name

    @property
    def parser(self) -> _typing.ParserType:
        """
        Return an instance of the parser class.
        """
        return _parse.Parser()

    @classmethod
    def tree(
        cls,
        obj: _typing.JSON,
        parent: Optional[_typing.DerekType] = None,
        name: Optional[str] = None,
    ) -> _typing.DerekType:
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
        if hasattr(self.parser, format):
            parser = getattr(self.parser, format)
        else:
            raise NotImplementedError

        result = parser(self)
        result["example"] = self.example()
        return {self.name or "untitled": result}

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
                v = c.example()
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
            result = dcp(self.value)

        return result
