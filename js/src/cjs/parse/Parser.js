const { oas2 } = require("./oas2");

class Parser {
  static oas2 = oas2;

  /**
   * Convert a data structure, with :code:`node` as the root node,
   * into OAS3 schema. (Alias for OAS2.)
   * @param {Derek} node - Root node of tree.
   * @param {string} strategy - Schema extraction strategy.
   * @returns {Object} - OAS3 schema, as JSON-serializable object.
   */
  static oas3(node) {
    return oas2(node);
  }
}

module.exports = {
  Parser,
};
