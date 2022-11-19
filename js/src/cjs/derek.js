const { Parser } = require("./parse/");

/**
 * A node in a data structure.
 *
 * Contains information about itself, its parent node, and any child nodes.
 */
class Derek {
  /**
   * Create a node.
   *
   * @param parent - Parent node.
   * @param children - Child nodes.
   * @param value - A JSON-serializable object/array.
   * @param name - Name of the returned Derek instance.
   */
  constructor(parent = null, children = null, value = null, name = null) {
    this.parent = parent;
    this.children = children;
    this.value = value;
    this.name = name;
  }

  /**
   * Return the parser class.
   *
   * @returns {function} Parser class.
   */
  get parser() {
    return Parser;
  }

  /**
   * Create a tree representation of obj.
   *
   * @static
   * @param obj - A JSON-serializable dictionary/list.
   * @param parent - Parent node to attach subtree to.
   * @param name - Name of the returned Derek instance.
   * @returns {Derek} Tree representation of obj, as a Derek instance.
   */
  static tree(obj, parent = null, name = null) {
    // TODO: return DerekTree (a subclass of Derek) instead of Derek.
    let children;
    const self = new this();

    if (obj instanceof Array) {
      // Make child nodes
      children = obj.map((item) => this.tree(item, self));
    } else if (obj instanceof Object) {
      // Make child nodes
      children = Object.values(obj).map((item) => this.tree(item, self));
    } else {
      // Not iterable
      children = null;
    }

    self.parent = parent;
    self.children = children;
    self.value = obj;
    self.name = name;

    return self;
  }

  /**
   * Create a tree representation of obj.
   *
   * @param format - Output format.
   * @returns {(Object|Array)} Tree representation of obj, as a Derek instance.
   */
  parse(format = "oas3") {
    let parser, result;

    format = format.toLowerCase();

    if (typeof this.parser[format] == "undefined") {
      throw "Not yet supported.";
    }

    result = this.parser[format](this);
    result.example = this.example();

    return {
      [this.name || "untitled"]: result,
    };
  }

  /**
   * Generate example JSON-serializable dictionary from self.
   *
   * @returns {Object} Example, as a JSON-serializable dictionary.
   */
  example() {
    let result = null;
    if (this.value === null) {
    } else if (this.value.constructor == Array) {
      if (this.value.length == 0) {
        result = [];
      } else {
        let c, v;

        c = this.children[0];
        v = c.example();
        result = [c instanceof Derek ? c.example() : c];
      }
    } else if (this.value.constructor == Object) {
      if (Object.keys(this.value).length == 0) {
        result = {};
      } else {
        let keys, values;
        (keys = Object.keys(this.value)),
          (values = this.children.map((c) =>
            c instanceof Derek ? c.example() : c
          ));

        result = Object.fromEntries(keys.map((e, i) => [e, values[i]]));
      }
    } else if (this.value instanceof Object) {
      result = Object.assign(
        new this.value.constructor(),
        JSON.parse(JSON.stringify(this.value))
      );
    } else {
      // NOTE: This won't handle custom subclasses of non-Object
      // JavaScript builtins
      result = JSON.parse(JSON.stringify(this.value));
    }
    return result;
  }
}

module.exports = { Derek };
