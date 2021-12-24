import json

from . import _typing


class Parser:
    __slots__ = tuple()

    @classmethod
    def oas2(cls, node: _typing.DerekType, strategy: str = "permissive"):
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
        elif isinstance(node.value, list) or isinstance(node.value, dict):
            # OAS3 list/dict

            # Parse each of the children
            subschemas = [cls.oas2(c, strategy) for c in node.children]

            if strategy in ["permissive", "restricted"]:
                # Convert subschemas to string to make them hashable,
                # then use set to find unique strings
                unique = sorted(set(json.dumps(s) for s in subschemas))

                # TODO: add a switch to use a "hash" approach for speed, instead

                if len(unique) > 1:
                    # If multiple unique subschemas exist, use oneOf

                    internals = {"oneOf": [json.loads(s) for s in unique]}
                else:
                    # Just use the first one
                    internals = subschemas[0]

                if isinstance(node.value, list):
                    j = {"type": "array", "items": internals}
                else:
                    if strategy == "permissive":
                        j = {"type": "object", "additionalProperties": internals}
                    else:
                        j = {
                            "type": "object",
                            "properties": dict(zip(node.value.keys(), subschemas)),
                        }
            elif strategy == "inner_join":
                if isinstance(node.value, list):
                    merging = {}
                    count = {}
                    for s in subschemas:
                        if s["type"] == "object":
                            for k, v in s["properties"].items():
                                if k not in merging:
                                    count[k] = 1
                                    merging[k] = [v]
                                else:
                                    count[k] += 1
                                    if v not in merging[k]:
                                        merging[k].append(v)

                    items = []
                    properties = {
                        k: (v if len(v) == 1 else {"oneOf": v})
                        for k, v in merging.items()
                    }
                    if len(properties) > 0:
                        merged_objects = {
                            "type": "object",
                            "properties": {
                                k: (v if len(v) == 1 else {"oneOf": v})
                                for k, v in merging.items()
                            },
                        }
                        required = [
                            k for k in merging.keys() if count[k] == len(node.children)
                        ]
                        if len(required) > 0:
                            merged_objects["required"] = required
                        items.append(merged_objects)

                    other_unique = set(
                        json.dumps(s) for s in subschemas if s["type"] != "object"
                    )

                    if len(other_unique) > 0:
                        items.extend(json.loads(s) for s in other_unique)

                    if len(items) > 1:
                        j = {"type": "array", "items": {"oneOf": items}}
                    else:
                        j = {"type": "array", "items": items[0]}
                else:
                    # Convert subschemas to string to make them hashable,
                    # then use set to find unique strings
                    unique = set(json.dumps(s) for s in subschemas)

                    # TODO: add a switch to use a "hash" approach for speed, instead

                    if len(unique) > 1:
                        # If multiple unique subschemas exist, use oneOf

                        internals = {"oneOf": [json.loads(s) for s in unique]}
                    else:
                        # Just use the first one
                        internals = subschemas[0]

                    j = {
                        "type": "object",
                        "properties": dict(zip(node.value.keys(), subschemas)),
                    }
            else:
                raise NotImplementedError
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
