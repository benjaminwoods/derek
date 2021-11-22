import json

def parse(node, format='oas3'):
    """
    Convert a tree of Derek nodes to a given format.
    """
    format = format.lower()
    if format == 'oas3':
        return _oas3(node)
    else:
        raise NotImplementedError

def _oas3(node):
    if isinstance(node.value, list):
        # TODO: don't assume that all of the child nodes are of the same
        # type.

        # OAS3 list
        if node.value == []:
            j = {
                "type": "array",
                "items": {},
                "maxItems": 0
            }
        else:
            j = {
                "type": "array",
                "items": json.loads(_oas3(node.children[0]))
            }
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
                "additionalProperties": json.loads(_oas3(node.children[0]))
            }
    else:
        if isinstance(node.value, str):
            j = {
                "type": "string"
            }
        elif isinstance(node.value, float):
            j = {
                "type": "number"
            }
        elif isinstance(node.value, bool):
            j = {
                "type": "boolean"
            }
        elif isinstance(node.value, int):
            j = {
                "type": "integer"
            }
        else:
            raise NotImplementedError

    return json.dumps(j)
