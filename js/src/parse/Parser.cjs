const { oas2 } = require("./oas2.cjs");

class Parser {
  static oas2 = oas2;

  static oas3(node) {
    return oas2(node);
  }
}

module.exports = {
  Parser,
};
