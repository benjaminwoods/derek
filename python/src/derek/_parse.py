import json

from . import _typing


class Parser:
    @classmethod
    def oas2(cls, node: _typing.DerekType):
        """
        Convert a data structure, with :code:`node` as the root node,
        into OAS2 schema.
        """
        if node.value == []:
            j = {"type": "array", "items": {}, "maxItems": 0}
        elif node.value == {}:
            j = {"type": "object", "properties": {}}
        elif isinstance(node.value, list) or isinstance(node.value, dict):
            # OAS3 list/dict

            # Parse each of the children
            subschemas = [cls.oas2(c) for c in node.children]

            # Convert subschemas to string to make them hashable,
            # then use set to find unique strings
            unique = set(json.dumps(s) for s in subschemas)

            # TODO: add a switch to use a "hash" approach for speed, instead

            if len(unique) > 1:
                # If multiple unique subschemas exist, use oneOf

                oneOf = [json.loads(s) for s in unique]
                internals = {"oneOf": oneOf}
            else:
                # Just use the first one
                internals = subschemas[0]

            if isinstance(node.value, list):
                j = {"type": "array", "items": internals}
            else:
                j = {"type": "object", "additionalProperties": internals}
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
    def oas3(cls, node: _typing.DerekType):
        """
        Convert a data structure, with :code:`node` as the root node,
        into OAS3 schema. (Alias for OAS2.)
        """

        return cls.oas2(node)
