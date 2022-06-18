import { oas2 } from "./oas2.mjs";

class Parser {
  static oas2 = oas2;

  static oas3(node) {
    return oas2(node);
  }
}

export { Parser };
