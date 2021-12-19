import json


class Parser:
    @classmethod
    def oas2(cls, node):
        """
        Convert a data structure, with :code:`node` as the root node,
        into OAS2 schema.
        """
        if isinstance(node.value, list):
            # TODO: don't assume that all of the child nodes are of the same
            # type.

            # OAS3 list
            if node.value == []:
                j = {"type": "array", "items": {}, "maxItems": 0}
            else:
                j = {"type": "array", "items": cls.oas2(node.children[0])}
        elif isinstance(node.value, dict):
            # TODO: don't assume that all of the child nodes are of the same
            # type.

            # OAS3 dictionary
            if node.value == {}:
                # Cannot parse {}.
                raise NotImplementedError
            else:
                j = {
                    "type": "object",
                    "additionalProperties": cls.oas2(node.children[0]),
                }
        else:
            if isinstance(node.value, str):
                j = {"type": "string"}
            elif isinstance(node.value, float):
                j = {"type": "number"}
            elif isinstance(node.value, bool):
                j = {"type": "boolean"}
            elif isinstance(node.value, int):
                j = {"type": "integer"}
            else:
                raise NotImplementedError

        return j

    @classmethod
    def oas3(cls, node):
        """
        Convert a data structure, with :code:`node` as the root node,
        into OAS3 schema. (Alias for OAS2.)
        """

        return cls.oas2(node)
