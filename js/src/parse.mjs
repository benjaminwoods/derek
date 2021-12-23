class Parser {
  static oas2(node) {
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
    } else if (
      (node.value.constructor == Array) |
      (node.value.constructor == Object)
    ) {
      // OAS3 list/dict
      let subschemas, unique, internals;

      // Parse each of the children
      // NOTE: Must explicitly call this.oas2(c) to correctly bind this.
      subschemas = node.children.map((c) => this.oas2(c));

      // Convert subschemas to string to make them hashable,
      // then use set to find unique strings
      unique = new Set(subschemas.map(JSON.stringify));

      // TODO: add a switch to use a "hash" approach for speed, instead

      if (unique.size > 1) {
        // If multiple unique subschemas exists, use oneOf

        internals = { oneOf: Array.from(unique.values(), JSON.parse) };
      } else {
        // Just use the first one
        internals = subschemas[0];
      }

      if (node.value.constructor == Array) {
        j = {
          type: "array",
          items: internals,
        };
      } else {
        j = {
          type: "object",
          additionalProperties: internals,
        };
      }
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
    } else {
      throw "Not yet implemented.";
    }

    return j;
  }

  static oas3(node) {
    return this.oas2(node);
  }
}

export { Parser };
