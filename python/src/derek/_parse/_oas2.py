import json

from .. import _typing


def oas2(node: _typing.DerekType, strategy: str = "permissive"):
    """
    Convert a data structure, with :code:`node` as the root node,
    into OAS2 schema.

    Parameters
    ----------
    node: Derek
        Root node of tree.
    strategy
        For a JSON of the form:

        .. code-block:: javascript

           [
             {
               "a": A,
               "b": B1,
               "c": C
             },
             {
               "a": A,
               "b": B2
             }
           ]

        with sub-JSONs, :code:`A`, :code:`B1`, :code:`B2` and :code:`C`,

        * If "permissive" (default), assume that key names can be freely
          chosen, and that each corresponding value can be freely chosen
          from the schemas of :code:`A`, :code:`B1`, :code:`B2` and
          :code:`C`.

          Use this strategy if the structure of the data is open, or if
          you know very little about your data.

          The returned schema is:

          .. code-block:: javascript

             {
               "type": "array",
               "items": {
                 "oneOf": [
                   {
                     "type": "object",
                     "additionalProperties": {
                       "oneOf": [schema_A, schema_B1, schema_C]
                     }
                   },
                   {
                     "type": "object",
                     "additionalProperties": {
                       "oneOf": [schema_A, schema_B2]
                     }
                   }
                 ]
               }
             }

        * If "restricted", each key must be defined as specified, and each
          corresponding value must be of that schema.

          Use this strategy if you know that your data is well structured
          and if your dictionaries have no optional keys.

          The returned schema is:

          .. code-block:: javascript

             {
               "type": "array",
               "items": {
                 "oneOf": [
                   {
                     "type": "object",
                     "properties": {
                       "a": schema_A,
                       "b": schema_B1,
                       "c": schema_C
                     }
                   },
                   {
                     "type": "object",
                     "properties": {
                       "a": schema_A,
                       "b": schema_B2
                     }
                   }
                 ]
               }
             }

        * If "inner_join", if two or more dictionaries appear in a list, the
          keys are merged.

          If the values for a given key have different
          schemas across the dictionaries, a oneOf is used.

          If the value appears in all dictionaries, it is assumed to be
          a required key (properties). Otherwise, it is deemed to be
          an optional key (additionalProperties).

          No attempt is made to infer if the appearance of one key makes
          another key required.

          That is to say, the returned schema is:

          .. code-block:: javascript

             {
               "type": "array",
               "items": {
                 "type": "object",
                 "properties": {
                   "a": schema_A,
                   "b": {
                     "oneOf": [schema_B1, schema_B2]
                   },
                   "c": schema_C
                 },
                 "required": ["a", "b"]
               }
             }

    Returns
    -------
    j: :data:`derek._typing.JSON`
        OAS2 schema, as JSON-serializable dictionary.
    """
    if node.value == []:
        j = {"type": "array", "items": {}, "maxItems": 0}
    elif node.value == {}:
        j = {"type": "object", "properties": {}}
    elif isinstance(node.value, str):
        j = {"type": "string"}
    elif isinstance(node.value, float):
        j = {"type": "number"}
    elif isinstance(node.value, bool):
        j = {"type": "boolean"}
    elif isinstance(node.value, int):
        j = {"type": "integer"}
    elif isinstance(node.value, list):
        j = _oas2_list(node, strategy)
    elif isinstance(node.value, dict):
        j = _oas2_dict(node, strategy)
    else:
        raise NotImplementedError

    return j


def _oas2_list(node, strategy):
    if strategy in ["permissive", "restricted"]:
        subschemas = _get_subschemas(node, strategy)
        subschemas = _unique_schemas(subschemas)
        schema = _oneOf(subschemas)
        j = {"type": "array", "items": schema}
    elif strategy == "inner_join":
        subschemas = _get_subschemas(node, strategy)
        subschemas = _merge_schemas(subschemas)
        schema = _oneOf(subschemas)
        j = {"type": "array", "items": schema}
    return j


def _oas2_dict(node, strategy):
    if strategy == "permissive":
        subschemas = _get_subschemas(node, strategy)
        schema = _oneOf(subschemas)
        j = {"type": "object", "additionalProperties": schema}
    elif strategy in ["restricted", "inner_join"]:
        subschemas = _get_subschemas(node, strategy)
        subschemas = _merge_schemas(subschemas)
        schema = dict(zip(node.value.keys(), subschemas))
        j = {"type": "object", "properties": schema}
    return j


def _get_subschemas(node, strategy):
    # Parse each of the children
    subschemas = [oas2(c, strategy) for c in node.children]
    return subschemas


def _merge_schemas(schemas):
    schemas_split = _split_schemas_by_type(schemas)

    merged = []
    objects = schemas_split.get("object", [])
    non_objects = [
        s for k, schemas in schemas_split.items() for s in schemas if k != "object"
    ]

    if len(objects) > 0:
        merged.append(_merge_objects(objects))
    if len(non_objects) > 0:
        merged.extend(_unique_schemas(non_objects))

    return merged


def _merge_objects(schemas):
    merged = {"type": "object"}

    count = {}
    properties = {}
    for s in schemas:
        for k, v in s.get("properties", {}).items():
            if k not in properties:
                count[k] = 0
                properties[k] = []
            count[k] += 1
            if v not in properties[k]:
                properties[k].append(v)
    if len(properties) > 0:
        merged["properties"] = {k: _oneOf(v) for k, v in properties.items()}
    required = [k for k in properties.keys() if count[k] == len(schemas)]
    if len(required) > 0:
        merged["required"] = required

    for k, v in list(merged.items()):
        if len(v) == 0:
            merged.pop(k)

    return merged


def _oneOf(schemas):
    unique = _unique_schemas(schemas, ordered=True)
    return unique[0] if len(unique) <= 1 else {"oneOf": unique}


def _unique_schemas(schemas, ordered=False):
    # Convert schemas to string to make them hashable,
    # then use set to find unique strings

    if ordered:
        unique = []
        for i, s in enumerate(map(json.dumps, schemas)):
            schema = schemas[i]
            if schema not in unique:
                unique.append(schema)

        return unique
    else:
        return list(map(json.loads, set(map(json.dumps, schemas))))


def _split_schemas_by_type(schemas):
    """
    Split schemas into different types.
    """

    collection = {}
    for s in schemas:
        subschema_type = s["type"]
        if subschema_type not in collection:
            collection[subschema_type] = []
        collection[subschema_type].append(s)
    return collection
