/**
 * Convert a data structure, with :code:`node` as the root node,
 * into OAS2 schema.
 *
 * @param {Derek} node - Root node of tree.
 * @param {string} strategy - Schema extraction strategy.
 * @returns {Object} - OAS2 schema, as JSON-serializable object.
 */
function oas2(node, strategy = "permissive") {
  let j;

  if (node.value.constructor == Array && node.value.length == 0) {
    j = {
      type: "array",
      items: {},
      maxItems: 0,
    };
  } else if (
    node.value.constructor == Object &&
    Object.keys(node.value).length == 0
  ) {
    j = {
      type: "object",
      properties: {},
    };
  } else if (node.value.constructor == String) {
    j = {
      type: "string",
    };
  } else if (node.value.constructor == Number) {
    if (node.value % 1 == 0) {
      console.warn(
        `Unable to detect if value ${node.value} is integer or float. Defaulting to float.`
      );
    }
    j = {
      type: "number",
    };
  } else if (node.value.constructor == Boolean) {
    j = {
      type: "boolean",
    };
  } else if (node.value.constructor == Array) {
    j = _oas2_array(node, strategy);
  } else if (node.value.constructor == Object) {
    j = _oas2_object(node, strategy);
  } else {
    throw "Not yet implemented.";
  }

  return j;
}

/**
 * Parse an Array node with a given strategy, and return an OAS2 JSON
 * schema
 *
 * @param {Derek} node - Root node of tree.
 * @param {string} strategy - Schema extraction strategy.
 * @returns {Object} - OAS2 schema, as JSON-serializable object.
 */
function _oas2_array(node, strategy) {
  let j;
  let schema;

  if (["permissive", "restricted"].includes(strategy)) {
    let subschemas = _get_subschemas(node, strategy);
    subschemas = _unique_schemas(subschemas);
    schema = _oneOf(subschemas);

    j = { type: "array", items: schema };
  } else if (strategy === "inner_join") {
    let subschemas = _get_subschemas(node, strategy);
    subschemas = _merge_schemas(subschemas);
    schema = _oneOf(subschemas);

    j = { type: "array", items: schema };
  } else {
    throw strategy;
  }

  return j;
}

/**
 * Parse an Object node with a given strategy, and return an OAS2 JSON
 * schema.
 *
 * @param {Derek} node - Root node of tree.
 * @param {string} strategy - Schema extraction strategy.
 * @returns {Object} - OAS2 schema, as JSON-serializable object.
 */
function _oas2_object(node, strategy) {
  let j;
  let schema;

  if (strategy === "permissive") {
    let subschemas = _get_subschemas(node, strategy);
    schema = _oneOf(subschemas);

    j = { type: "object", additionalProperties: schema };
  } else if (["restricted", "inner_join"].includes(strategy)) {
    let subschemas = _get_subschemas(node, strategy);
    schema = Object.fromEntries(
      Object.keys(node.value).map((k, i) => [k, subschemas[i]])
    );
    j = { type: "object", properties: schema };
  }

  return j;
}

/**
 * Get subschemas for each of the node's children.
 *
 * @param {Derek} node - Root node of tree.
 * @param {string} strategy - Schema extraction strategy.
 * @returns {Array} - Subschemas, returned as an array of objects.
 */
function _get_subschemas(node, strategy) {
  const subschemas = node.children.map((c) => oas2(c, strategy));

  return subschemas;
}

/**
 * Merge together subschemas.
 *
 * @param {Derek} node - Root node of tree.
 * @param {string} strategy - Schema extraction strategy.
 * @returns {Array} - Subschemas, returned as an array of objects.
 */
function _merge_schemas(schemas) {
  const schemas_split = _split_schemas_by_type(schemas);
  let merged = [];
  const objects = schemas_split.object || [];
  const non_objects = Object.entries(schemas_split)
    .filter(([k, v]) => k !== "object")
    .map(([k, v]) => v)
    .flat();

  if (objects.length > 0) {
    merged.push(_merge_objects(objects));
  }
  if (non_objects.length > 0) {
    merged.push(..._unique_schemas(non_objects));
  }

  return merged;
}

/**
 * Merge together object subschemas.
 *
 * @param {Array} schemas - Subschemas, specified as an array of objects.
 * @returns {Array} - Subschemas, returned as an array of objects.
 */
function _merge_objects(schemas) {
  const merged = { type: "object" };

  const count = {};
  const properties = {};

  schemas.forEach((s) => {
    Object.entries(s.properties || {}).forEach(([k, v]) => {
      if (!Object.keys(properties).includes(k)) {
        count[k] = 0;
        properties[k] = [];
      }
      count[k] += 1;
      if (!properties[k].map(JSON.stringify).includes(JSON.stringify(v))) {
        properties[k].push(v);
      }
    });
  });

  if (Object.keys(properties).length > 0) {
    merged.properties = Object.fromEntries(
      Object.entries(properties).map(([k, v]) => [k, _oneOf(v)])
    );
  }
  const required = Object.keys(properties).filter(
    (k) => count[k] == schemas.length
  );
  if (required.length > 0) {
    merged.required = required;
  }

  Object.entries(merged).forEach(([k, v]) => {
    if (v.length == 0) {
      delete merged[k];
    }
  });

  return merged;
}

/**
 * Compress schemas using oneOf.
 *
 * @param {Array} schemas - Subschemas, specified as an array of objects.
 * @returns {Object} - schemas[0] if all schemas are the same.
 */
function _oneOf(schemas) {
  const unique = _unique_schemas(schemas);
  return unique.length <= 1 ? unique[0] : { oneOf: unique };
}

/**
 * Get subset of unique schemas from an array of schemas.
 *
 * @param {Array} schemas - Subschemas, specified as an array of objects.
 * @returns {Array} - Unique schemas.
 */
function _unique_schemas(schemas) {
  return Array.from(new Set(schemas.map((s) => JSON.stringify(s)))).map((S) =>
    JSON.parse(S)
  );
}

/**
 * Sort schemas by type.
 *
 * @param {Array} schemas - Subschemas, specified as an array of objects.
 * @returns {Object} - Object with key-value pairs that refer to each schema type.
 */
function _split_schemas_by_type(schemas) {
  const collection = {};
  schemas.forEach((s) => {
    const subschema_type = s.type;
    if (!Object.keys(collection).includes(subschema_type)) {
      collection[subschema_type] = [];
    }
    collection[subschema_type].push(s);
  });
  return collection;
}

module.exports = {
  oas2,
  _oas2_array,
  _oas2_object,
  _get_subschemas,
  _merge_schemas,
  _merge_objects,
  _oneOf,
  _unique_schemas,
  _split_schemas_by_type,
};
