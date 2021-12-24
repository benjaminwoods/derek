import json

from .. import _typing

from ._oas2 import oas2 as _oas2


class Parser:
    __slots__ = tuple()

    oas2 = classmethod(_oas2)

    @classmethod
    def oas3(cls, node: _typing.DerekType, strategy: str = "permissive"):
        """
        Convert a data structure, with :code:`node` as the root node,
        into OAS3 schema. (Alias for OAS2.)

        Parameters
        ----------
        node: Derek
            Root node of tree.
        strategy
            Strategy for producing the schema. See :meth:`Parser.oas2`.

        Returns
        -------
        j: :data:`derek._typing.JSON`
            OAS2 schema, as JSON-serializable dictionary.
        """

        return cls.oas2(node, strategy)
