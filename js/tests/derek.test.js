const { Derek } = require("../src/cjs/derek");
const { Parser } = require("../src/cjs/parse/parser");

describe("initialization", () => {
  test("defaults", () => {
    const node = new Derek();

    expect(node.parent).toBe(null);
    expect(node.children).toBe(null);
    expect(node.value).toBe(null);
    expect(node.name).toBe(null);
  });

  test("with arguments", () => {
    const parent = new Derek();
    const attributes = {
      parent: parent,
      children: [1, 2, 3],
      values: [1, 2, 3],
      name: "some_node",
    };
    const node = new Derek(...Object.values(attributes));

    expect(node.parent).toBe(attributes.parent);
    expect(node.children).toBe(attributes.children);
    expect(node.value).toBe(attributes.values);
    expect(node.name).toEqual(attributes.name);
  });
});

describe("tree", () => {
  const check = (obj, parent, name) => {
    const node = Derek.tree(obj, parent, name);

    if ((obj instanceof Array) | (obj instanceof Object)) {
      expect(node.value).toBe(obj);
    }

    if (typeof name != "undefined") {
      expect(node.name).toEqual(name);
    }
    if (typeof parent != "undefined") {
      expect(node.parent).toBe(parent);
    }

    // TODO: check child nodes
  };

  test("name", () => {
    check(3141, null, "some_node_name");
  });

  test("no name", () => {
    check(3141);
  });

  test("parent", () => {
    check(3141, new Derek());
  });

  test("no parent", () => {
    check(3141);
  });

  test("non iterable", () => {
    check(3141);
  });

  test("simple Array", () => {
    check([1, 2, 3]);
  });

  test("Array in Array", () => {
    check([
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ]);
  });

  test("Array in Object", () => {
    check({
      a: [1, 2, 3],
      b: [4, 5, 6],
      c: [7, 8, 9],
    });
  });

  test("simple Object", () => {
    check({
      a: 1,
      b: 2,
      c: 3,
    });
  });

  test("Object in Object", () => {
    check({
      a: {
        d: 1,
        e: 2,
        f: 3,
      },
      b: {
        g: 4,
        h: 5,
        i: 6,
      },
      c: {
        j: 7,
        k: 8,
        l: 9,
      },
    });
  });

  test("Object in Array", () => {
    check([
      { d: 1, e: 2, f: 3 },
      { g: 4, h: 5, i: 6 },
      { j: 7, k: 8, l: 9 },
    ]);
  });
});

describe("example", () => {
  test("non iterable", () => {
    const obj = 3141;
    const node = Derek.tree(obj);
    expect(node.example()).toEqual(obj);
  });

  test("null", () => {
    const node = new Derek();
    expect(node.example()).toBe(null);
  });

  test("unusual value", () => {
    class Unusual {
      constructor() {
        this.a = [1];
        this.b = { 4: 5 };
      }
    }

    const obj = new Unusual();
    const node = new Derek(null, null, obj);
    let example;

    example = node.example();
    expect(example).toBeInstanceOf(Unusual);
    for (let k of Object.keys(Unusual)) {
      expect(example[k]).toEqual(example[k]);
      expect(example[k]).not.toBe(example[k]);
    }
  });

  test("empty Array", () => {
    const obj = [];
    const node = new Derek(null, null, obj);
    let example;

    example = node.example();
    expect(example).toEqual(obj);
    expect(example).not.toBe(obj);
  });

  test("simple Array", () => {
    const obj = [1, 2, 3];
    const node = Derek.tree(obj);
    expect(node.example()).toEqual([1]);
  });

  test("simple Array", () => {
    const obj = [1, 2, 3];
    const node = Derek.tree(obj);
    expect(node.example()).toEqual([1]);
  });

  test("Array in Array", () => {
    const obj = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ];
    const node = Derek.tree(obj);
    expect(node.example()).toEqual([[1]]);
  });

  test("empty Object", () => {
    const obj = {};
    const node = new Derek(null, null, obj);
    let example;

    example = node.example();
    expect(example).toEqual(obj);
    expect(example).not.toBe(obj);
  });

  test("simple Object", () => {
    const obj = {
      a: 1,
      b: 2,
      c: 3,
    };
    const node = Derek.tree(obj);
    expect(node.example()).toEqual({ a: 1, b: 2, c: 3 });
  });

  test("Object in Object", () => {
    const obj = {
      a: { d: 1, e: 2, f: 3 },
      b: { g: 4, h: 5, i: 6 },
      c: { j: 7, k: 8, l: 9 },
    };
    const node = Derek.tree(obj);
    expect(node.example()).toEqual({
      a: { d: 1, e: 2, f: 3 },
      b: { g: 4, h: 5, i: 6 },
      c: { j: 7, k: 8, l: 9 },
    });
  });

  test("Object in Array", () => {
    const obj = [
      { d: 1, e: 2, f: 3 },
      { g: 4, h: 5, i: 6 },
      { j: 7, k: 8, l: 9 },
    ];
    const node = Derek.tree(obj);
    expect(node.example()).toEqual([{ d: 1, e: 2, f: 3 }]);
  });
});

describe("parser", () => {
  test("parser class", () => {
    let parser = new Derek().parser;

    expect(parser).toBe(Parser);
  });
});

describe("parse", () => {
  const testState = {};

  beforeEach(() => {
    const obj = [
      { d: 1, e: 2, f: 3 },
      { g: 4, h: 5, i: 6 },
      { j: 7, k: 8, l: 9 },
    ];
    testState.node = Derek.tree(obj);
  });

  test("format not implemented", () => {
    expect(() => {
      testState.node.parse("not_a_real_format");
    }).toThrow();
  });

  test("parse oas3", () => {
    let j = testState.node.parse();

    expect(j).toEqual({
      untitled: {
        example: [{ d: 1, e: 2, f: 3 }],
        items: {
          additionalProperties: { type: "number" },
          type: "object",
        },
        type: "array",
      },
    });
  });

  test("parse with name", () => {
    let node = new Derek(null, null, 1, "test");
    expect(node.parse()).toEqual({
      test: {
        example: 1,
        type: "number",
      },
    });
  });
});
