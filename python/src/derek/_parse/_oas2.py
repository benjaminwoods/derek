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
    strategy: str
        Schema extraction strategy.

        Must be one of "permissive" (default), "restricted", or "inner_join".

        * "permissive" considers each dictionary in the data structure to have
          optional key-value pairs. Key names can be freely chosen. For each
          list in the data structure, the spec requires one or more of the
          specified elements in any order, with each element matching the
          subschema for any element in the list.
        * "restricted" extends "permissive", restricting dictionary key names to
          the values specified in :code:`node.value`.
        * "inner_join" extends "restricted", combining subschemas together for
          each element in lists in the data structure.


    Examples
    --------

    For "permissive":
    * Dictionaries:
      * If :code:`{"a": 1, "b": 2.0}` is :code:`node.value`:
        * :code:`{"a": 1}` and :code:`{"b": 2.0}` will pass validation against
          the schema. (Partial values.)
        * :code:`{"c": 1}` will pass validation against the schema. (Different
          key name.)
        * :code:`{"a": "text"}` will not pass validation against the schema.
          (Different value type.)
    * Lists:
      * If :code:`[{"a": 1}, {"b": 2.0}]` is :code:`node.value`:
        * :code:`[{"a": 1}]` and :code:`[{"b": 2.0}]` will pass validation
          against the schema. (Minimum length.)
        * :code:`[{"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Order.)
        * :code:`[{"a": 1}, {"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Maximum length.)
        * :code:`[{"a": 1, "b": 2.0}]` will not pass validation against the
          schema. (Merged subschemas.)

    For "restricted":
    * Dictionaries:
      * If :code:`{"a": 1, "b": 2.0}` is :code:`node.value`:
        * :code:`{"a": 1}` and :code:`{"b": 2.0}` will pass validation against
          the schema. (Partial values.)
        * :code:`{"c": 1}` will not pass validation against the schema.
          (Different key name.)
        * :code:`{"a": "text"}` will not pass validation against the schema.
          (Different value type.)
    * Lists:
      * If :code:`[{"a": 1}, {"b": 2.0}]` is :code:`node.value`:
        * :code:`[{"a": 1}]` and :code:`[{"b": 2.0}]` will pass validation
          against the schema. (Minimum length.)
        * :code:`[{"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Order.)
        * :code:`[{"a": 1}, {"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Maximum length.)
        * :code:`[{"a": 1, "b": 2.0}]` will not pass validation against the
          schema. (Merged subschemas.)

    For "inner_join":
    * Dictionaries:
      * If :code:`{"a": 1, "b": 2.0}` is :code:`node.value`:
        * :code:`{"a": 1}` and :code:`{"b": 2.0}` will pass validation against
          the schema. (Partial values.)
        * :code:`{"c": 1}` will not pass validation against the schema.
          (Different key name.)
        * :code:`{"a": "text"}` will not pass validation against the schema.
          (Different value type.)
    * Lists:
      * If :code:`[{"a": 1}, {"b": 2.0}]` is :code:`node.value`:
        * :code:`[{"a": 1}]` and :code:`[{"b": 2.0}]` will pass validation
          against the schema. (Minimum length.)
        * :code:`[{"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Order.)
        * :code:`[{"a": 1}, {"b": 2.0}, {"a": 1}]` will pass validation
          against the schema. (Maximum length.)
        * :code:`[{"a": 1, "b": 2.0}]` will pass validation against the
          schema. (Merged subschemas.)

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
    """
    Parse a list node with a given strategy, and return an OAS2 JSON
    schema.

    Parameters
    ----------
    node: Derek
        Root node of tree.
    strategy:
        Schema extraction strategy.

        Must be one of "permissive" (default), "restricted", or "inner_join".

    Examples
    --------
    For a JSON of the form

    .. code-block:: javascript

       [
         A,
         {
           "b": B1
           "c": C
         }
         },
         {
           "b": B2
           "d": D
         }
       ]

    with sub-JSONs, :code:`A`, :code:`B1`, :code:`B2`, :code:`C`, and
    :code:`D`:

    * If "permissive" (default):

      .. code-block:: python

         {
           "type": "array",
           "items": {
             "oneOf": [
                schema_A,
                {
                  "type": "object",
                  "additionalProperties": {
                    "b": schema_B1,
                    "c": schema_C
                  }
                },
                {
                  "type": "object",
                  "additionalProperties": {
                    "b": schema_B2,
                    "d": schema_D
                  }
                }
             ]
           }
         }

    * If "restricted":

      .. code-block:: python

         {
           "type": "array",
           "items": {
             "oneOf": [
                schema_A,
                {
                  "type": "object",
                  "properties": {
                    "b": schema_B1,
                    "c": schema_C
                  }
                },
                {
                  "type": "object",
                  "properties": {
                    "b": schema_B2,
                    "d": schema_D
                  }
                }
             ]
           }
         }

    * If "inner_join":

      .. code-block:: python

         {
           "type": "array",
           "items": {
             "oneOf": [
                schema_A,
                {
                  "type": "object",
                  "properties": {
                    "b": {
                      "oneOf": [schema_B1, schema_B2]
                    },
                    "c": schema_C,
                    "d": schema_D
                  },
                  "required": ["b"]
                }
             ]
           }
         }
    """
    if strategy in ["permissive", "restricted"]:
        subschemas = _get_subschemas(node, strategy)
        subschemas = _unique_schemas(subschemas, ordered=True)
        schema = _oneOf(subschemas)
        j = {"type": "array", "items": schema}
    elif strategy == "inner_join":
        subschemas = _get_subschemas(node, strategy)
        subschemas = _merge_schemas(subschemas)
        schema = _oneOf(subschemas)
        j = {"type": "array", "items": schema}
    return j


def _oas2_dict(node, strategy):
    """
    Parse a dict node with a given strategy, and return an OAS2 JSON
    schema.

    Parameters
    ----------
    node: Derek
        Root node of tree.
    strategy:
        Schema extraction strategy.

        Must be one of "permissive" (default), "restricted", or "inner_join".

    Examples
    --------
    For a JSON of the form

    .. code-block:: python

       {
         "a": A,
         "b": B1,
         "c": C
       }

    with sub-JSONs, :code:`A`, :code:`B1`, and :code:`C`,

    * If "permissive" (default), assume that key names can be freely
      chosen, and that each corresponding value can be freely chosen
      from the schemas of :code:`A`, :code:`B1`, :code:`B2` and
      :code:`C`.

      Use this strategy if the structure of the data is open, or if
      you know very little about your data.

      The returned schema is:

      .. code-block:: python

         {
           "type": "object",
           "additionalProperties": {
             "oneOf": [schema_A, schema_B1, schema_C]
           }
         }

    * If "restricted", each key must be defined as specified, and each
      corresponding value must be of that schema.

      Use this strategy if you know that your data is well structured
      and if your dictionaries have no optional keys.

      The returned schema is:

      .. code-block:: python

         {
           "type": "object",
           "properties": {
             "a": schema_A,
             "b": schema_B1,
             "c": schema_C
           }
         }

    * If "inner_join", if two or more dictionaries appear in a list, the
      keys are merged.

      If the values for a given key have different
      schemas across the dictionaries, a oneOf is used.

      If the value appears in all dictionaries, it is assumed to be
      a required key. Otherwise, it is deemed to be an optional key.

      No attempt is made to infer if the appearance of one key makes
      another key required.

      That is to say, the returned schema is:

      .. code-block:: python

         {
           "type": "object",
           "properties": {
             "a": schema_A,
             "b": schema_B1,
             "c": schema_C
           }
         }
    """
    if strategy == "permissive":
        subschemas = _get_subschemas(node, strategy)
        schema = _oneOf(subschemas)
        j = {"type": "object", "additionalProperties": schema}
    elif strategy in ["restricted", "inner_join"]:
        subschemas = _get_subschemas(node, strategy)
        schema = dict(zip(node.value.keys(), subschemas))
        j = {"type": "object", "properties": schema}
    return j


def _get_subschemas(node, strategy):
    """
    Get subschemas for each of the node's children.

    Parameters
    ----------
    node: Derek
        Root node of tree.
    strategy:
        Schema extraction strategy.

        Must be one of "permissive" (default), "restricted", or "inner_join".

    Returns
    -------
    subschemas: List[Dict]
        Subschemas, returned as a list of dictionaries.
    """
    # Parse each of the children
    subschemas = [oas2(c, strategy) for c in node.children]
    return subschemas


def _merge_schemas(schemas):
    """
    Merge together subschemas.

    Parameters
    ----------
    node: Derek
        Root node of tree.
    strategy:
        Schema extraction strategy.

        Must be one of "permissive" (default), "restricted", or "inner_join".

    Returns
    -------
    subschemas: List[Dict]
        Subschemas, returned as a list of dictionaries.
    """
    schemas_split = _split_schemas_by_type(schemas)

    merged = []
    objects = schemas_split.get("object", [])
    non_objects = [
        s for k, schemas in schemas_split.items() for s in schemas if k != "object"
    ]

    if len(objects) > 0:
        merged.append(_merge_objects(objects))
    if len(non_objects) > 0:
        merged.extend(_unique_schemas(non_objects, ordered=True))

    return merged


def _merge_objects(schemas):
    """
    Merge together object subschemas.

    With a "direct subschema" refering to an element of :code:`schemas`:
    * If a property name appears in each direct subschema, label it as required.
    * If a property name appears in more than one direct subschema, for each
      direct subschema the name appears in:
      * If the property value is different across the direct subschemas,
        list each unique type in a "oneOf" in the result. That is to say, for
        input:

        .. code-block:: python

           [
             {
               "type": "object",
               "properties": {
                 "a": {
                   "type": "integer"
                 }
               }
             },
             {
               "type": "object",
               "properties": {
                 "a": {
                   "type": "text"
                 }
               }
             }
           ]

         return:

         .. code-block:: python

            {
              "type": "object",
              "properties": {
                "a": {
                  "oneOf": [
                    {"type": "integer"},
                    {"type": "text"}
                  ]
                },
              "required": ["a"]
            }

      * If the property value is the same in all direct subschemas, declare
        the value directly in the merged result. That is to say, for
        input:

        .. code-block:: python

           [
             {
               "type": "object",
               "properties": {
                 "a": {
                   "type": "integer"
                 }
               }
             },
             {
               "type": "object",
               "properties": {
                 "a": {
                   "type": "integer"
                 }
               }
             }
           ]

         return:

         .. code-block:: python

            {
              "type": "object",
              "properties": {
                "a": {
                  "type": "integer"
                },
              "required": ["a"]
            }

    Parameters
    ----------
    schemas: List[Dict]
        Subschemas, specified as a list of dictionaries.

    Returns
    -------
    subschemas: List[Dict]
        Subschemas, returned as a list of dictionaries.
    """
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
    """
    Compress schemas using oneOf.

    Parameters
    ----------
    schemas: List[Dict]
        Subschemas, specified as a list of dictionaries.

    Returns
    -------
    Dict
        schemas[0] if all schemas are the same.
    """
    unique = _unique_schemas(schemas, ordered=True)
    return unique[0] if len(unique) <= 1 else {"oneOf": unique}


def _unique_schemas(schemas, ordered=False):
    """
    Compress schemas using oneOf.

    Parameters
    ----------
    schemas: List[Dict]
        Subschemas, specified as a list of dictionaries.
    ordered: bool
        If True, return schemas in the same order as represented in schemas.

        If False, return schemas in any order. Set False to get a slight
        speedup.

    Returns
    -------
    Dict
        schemas[0] if all schemas are the same.
    """
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
    Sort schemas by type.

    Parameters
    ----------
    schemas: List[Dict]
        Subschemas, specified as a list of dictionaries.

    Returns
    -------
    Dict
        A dictionary containing key-value pairs referring to each
        schema type.

    Examples
    --------

    For input:

    .. code-block:: python

       [
         {
           "type": "integer"
         },
         {
           "type": "string"
         },
         {
           "type": "integer"
         }
       ]

    return:

    .. code-block:: python

       {
         "integer": [
           {
             "type": "integer"
           },
           {
             "type": "integer"
           }
         ],
         "string": [
           {
             "type": "string"
           }
         ]
       }
    """

    collection = {}
    for s in schemas:
        subschema_type = s["type"]
        if subschema_type not in collection:
            collection[subschema_type] = []
        collection[subschema_type].append(s)
    return collection
