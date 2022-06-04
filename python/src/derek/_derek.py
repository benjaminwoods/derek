import json
from copy import deepcopy as dcp

from . import _parse

from typing import Optional, Any, Iterable
from . import _typing


class Derek:
    """
    A node in a data structure.

    Contains information about itself, its parent node, and any child nodes.

    Parameters
    ----------
    parent:
        Parent node.

        If specified, the Derek instance stores a reference to the parent
        node.

        The Derek instance is *not* added to the :code:`children` of the
        parent node.

        If not specified, the Derek instance has :code:`parent`
        set to :code:`None`.
    children:
        Child nodes.

        If specified, the Derek instance stores a reference to the children
        nodes.

        The Derek instance is *not* added as a :code:`parent` for any of the
        child nodes.

        If not specified, the Derek instance has :code:`children`
        set to :code:`None`.
    value: :data:`derek._typing.JSON`
        A JSON-serializable dictionary/list.
    name:
        Name of the returned Derek instance.
    """

    # TODO: Add reload method
    # TODO: Add checkIntegrity method

    __slots__ = "parent", "children", "value", "name"

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
    def parser(self) -> type:
        """
        Return the parser class.

        Returns
        -------
        type
            The parser class.
        """
        return _parse.Parser

    @classmethod
    def tree(
        cls,
        obj: _typing.JSON,
        parent: Optional[_typing.DerekType] = None,
        name: Optional[str] = None,
    ) -> _typing.DerekType:
        """
        Create a tree representation of :code:`obj`.

        Parameters
        ----------
        obj: :data:`derek._typing.JSON`
            A JSON-serializable dictionary/list.
        parent
            Parent node to attach subtree to.

            If specified, the returned Derek instance is attached as a child
            of the node.

            If not specified, the returned Derek instance has :code:`parent`
            set to :code:`None`.
        name:
            Name of the returned Derek instance.

        Returns
        -------
        Tree representation of :code:`obj`, as a Derek instance.

        :code:`obj` is identical (same :code:`id`) to `self.value`.
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

    def parse(self, format: str = "oas3", **kwargs) -> _typing.JSON:
        """
        Convert a tree of Derek nodes to a given format.

        Parameters
        ----------
        format
            Output format.
        kwargs
            Keyword arguments to pass to self.parser.

        Returns
        -------
        j: :data:`derek._typing.JSON`
            A JSON-serializable dictionary/list.
        """
        format = format.lower()
        if hasattr(self.parser, format):
            parser = getattr(self.parser, format)
        else:
            raise NotImplementedError

        result = parser(self, **kwargs)
        result["example"] = self.example()
        return {self.name or "untitled": result}

    def example(self) -> _typing.JSON:
        """
        Generate example JSON-serializable dictionary from self.

        The example yields the same schema as a tree created
        with self.value.

        Returns
        -------
        j: :data:`derek._typing.JSON`
            Example, as a JSON-serializable dictionary.
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
