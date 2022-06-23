const { Derek } = require("../../../src/cjs/derek");
const { Parser } = require("../../../src/cjs/parse/parser");

function schema(obj, ...kwargs) {
  const node = Derek.tree(obj, ...kwargs);

  return Parser.oas3(node);
}

describe("oas3", () => {
  test("integer", () => {
    const obj = 3141;
    const j = schema(obj);
    expect(j).toEqual({ type: "number" });
  });

  test("string", () => {
    const obj = "abc";
    const j = schema(obj);
    expect(j).toEqual({ type: "string" });
  });

  test("float", () => {
    const obj = 3.141;
    const j = schema(obj);
    expect(j).toEqual({ type: "number" });
  });

  test("bool", () => {
    const obj = true;
    const j = schema(obj);
    expect(j).toEqual({ type: "boolean" });
  });

  test("empty_list", () => {
    const obj = [];
    const j = schema(obj);
    expect(j).toEqual({ type: "array", items: {}, maxItems: 0 });
  });

  test("simple_list", () => {
    const obj = [1, 2, 3];
    const j = schema(obj);
    expect(j).toEqual({ type: "array", items: { type: "number" } });
  });

  test("list_in_list", () => {
    const obj = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ];
    const j = schema(obj);
    expect(j).toEqual({
      type: "array",
      items: { type: "array", items: { type: "number" } },
    });
  });

  test("list_in_dict", () => {
    const obj = { a: [1, 2, 3], b: [4, 5, 6], c: [7, 8, 9] };
    const j = schema(obj);
    expect(j).toEqual({
      type: "object",
      additionalProperties: { type: "array", items: { type: "number" } },
    });
  });

  test("empty_dict", () => {
    const obj = {};
    const j = schema(obj);
    expect(j).toEqual({ type: "object", properties: {} });
  });

  test("simple_dict", () => {
    const obj = { a: 1, b: 2, c: 3 };
    const j = schema(obj);
    expect(j).toEqual({
      type: "object",
      additionalProperties: { type: "number" },
    });
  });

  test("dict_in_dict", () => {
    const obj = {
      a: { d: 1, e: 2, f: 3 },
      b: { g: 4, h: 5, i: 6 },
      c: { j: 7, k: 8, l: 9 },
    };
    const j = schema(obj);
    expect(j).toEqual({
      type: "object",
      additionalProperties: {
        type: "object",
        additionalProperties: { type: "number" },
      },
    });
  });

  test("dict_in_list", () => {
    const obj = [
      { d: 1, e: 2, f: 3 },
      { g: 4, h: 5, i: 6 },
      { j: 7, k: 8, l: 9 },
    ];
    const j = schema(obj);
    expect(j).toEqual({
      type: "array",
      items: {
        type: "object",
        additionalProperties: { type: "number" },
      },
    });
  });

  test("unparseable_type", () => {
    class Unusual {
      constructor() {
        this.a = [1];
        this.b = { 4: 5 };
      }
    }
    const obj = new Unusual();
    expect(() => schema(obj)).toThrow();
  });

  test("oneOf_list", () => {
    const obj = [1, "a", 3.0];
    const j = schema(obj);

    expect(j).toEqual({
      items: {
        oneOf: [{ type: "number" }, { type: "string" }],
      },
      type: "array",
    });
  });

  test("oneOf_dict", () => {
    const obj = { a: 1, b: "something", c: 4.0 };
    const j = schema(obj);

    expect(j).toEqual({
      additionalProperties: {
        oneOf: [{ type: "number" }, { type: "string" }],
      },
      type: "object",
    });
  });
});
