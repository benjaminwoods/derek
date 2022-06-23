const { Derek } = require("../../../src/cjs/derek");
const _oas2 = require("../../../src/cjs/parse/oas2");

let node;
beforeAll(() => {
  const obj = [{ a: 1, b: "b1", c: 3.0 }, { a: 4, b: ["b2"] }, [1, 2, 3.0]];

  node = Derek.tree(obj);
});

let schemas;
beforeAll(() => {
  schemas = [
    {
      additionalProperties: {
        oneOf: [{ type: "integer" }, { type: "number" }, { type: "string" }],
      },
      type: "object",
    },
    { type: "string" },
    {
      additionalProperties: {
        oneOf: [
          { items: { type: "string" }, type: "array" },
          { type: "integer" },
        ],
      },
      type: "object",
    },
    {
      items: { oneOf: [{ type: "number" }, { type: "integer" }] },
      type: "array",
    },
    { type: "string" },
  ];
});

describe("_oas2_array", () => {
  test("permissive", () => {
    const result = _oas2._oas2_array(node, "permissive");

    expect(result).toEqual({
      type: "array",
      items: {
        oneOf: [
          {
            type: "object",
            additionalProperties: {
              oneOf: [{ type: "number" }, { type: "string" }],
            },
          },
          {
            type: "object",
            additionalProperties: {
              oneOf: [
                { type: "number" },
                { type: "array", items: { type: "string" } },
              ],
            },
          },
          {
            items: { type: "number" },
            type: "array",
          },
        ],
      },
    });
  });

  test("restricted", () => {
    const result = _oas2._oas2_array(node, "restricted");

    expect(result).toEqual({
      type: "array",
      items: {
        oneOf: [
          {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "string" },
              c: { type: "number" },
            },
          },
          {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "array", items: { type: "string" } },
            },
          },
          {
            items: { type: "number" },
            type: "array",
          },
        ],
      },
    });
  });

  test.only("inner_join", () => {
    const result = _oas2._oas2_array(node, "inner_join");
    expect(result).toEqual({
      type: "array",
      items: {
        oneOf: [
          {
            type: "object",
            properties: {
              a: { type: "number" },
              b: {
                oneOf: [
                  { type: "string" },
                  { type: "array", items: { type: "string" } },
                ],
              },
              c: { type: "number" },
            },
            required: ["a", "b"],
          },
          {
            items: { type: "number" },
            type: "array",
          },
        ],
      },
    });
  });
});

describe("_oas2_object", () => {
  let node;
  beforeAll(() => {
    const obj = { a: 1, b: "b1", c: 3.0 };

    node = Derek.tree(obj);
  });

  test("permissive", () => {
    const result = _oas2._oas2_object(node, "permissive");

    expect(result).toEqual({
      type: "object",
      additionalProperties: {
        oneOf: [{ type: "number" }, { type: "string" }],
      },
    });
  });

  test("restricted", () => {
    const result = _oas2._oas2_object(node, "restricted");

    expect(result).toEqual({
      type: "object",
      properties: {
        a: { type: "number" },
        b: { type: "string" },
        c: { type: "number" },
      },
    });
  });

  test("inner_join", () => {
    const result = _oas2._oas2_object(node, "inner_join");

    expect(result).toEqual({
      type: "object",
      properties: {
        a: { type: "number" },
        b: { type: "string" },
        c: { type: "number" },
      },
    });
  });
});

describe("_get_subchemas", () => {
  test("permissive", () => {
    const result = _oas2._get_subschemas(node, "permissive");

    expect(result).toEqual([
      {
        additionalProperties: {
          oneOf: [{ type: "number" }, { type: "string" }],
        },
        type: "object",
      },
      {
        additionalProperties: {
          oneOf: [
            { type: "number" },
            { items: { type: "string" }, type: "array" },
          ],
        },
        type: "object",
      },
      {
        items: { type: "number" },
        type: "array",
      },
    ]);
  });

  test("restricted", () => {
    const result = _oas2._get_subschemas(node, "restricted");

    expect(result).toEqual([
      {
        properties: {
          a: { type: "number" },
          b: { type: "string" },
          c: { type: "number" },
        },
        type: "object",
      },
      {
        properties: {
          a: { type: "number" },
          b: { items: { type: "string" }, type: "array" },
        },
        type: "object",
      },
      {
        items: { type: "number" },
        type: "array",
      },
    ]);
  });

  test("inner_join", () => {
    const result = _oas2._get_subschemas(node, "inner_join");

    expect(result).toEqual([
      {
        properties: {
          a: { type: "number" },
          b: { type: "string" },
          c: { type: "number" },
        },
        type: "object",
      },
      {
        properties: {
          a: { type: "number" },
          b: { items: { type: "string" }, type: "array" },
        },
        type: "object",
      },
      {
        items: { type: "number" },
        type: "array",
      },
    ]);
  });
});

test("_merge_schemas", () => {
  const merged = _oas2._merge_schemas(schemas);

  expect(merged).toEqual([
    { type: "object" },
    { type: "string" },
    {
      items: { oneOf: [{ type: "number" }, { type: "integer" }] },
      type: "array",
    },
  ]);
});

test("_merge_objects", () => {
  const merged = _oas2._merge_objects(schemas);

  expect(merged).toEqual({ type: "object" });
});

test("_oneOf", () => {
  const merged = _oas2._oneOf(schemas);

  expect(merged).toEqual({
    oneOf: [
      {
        additionalProperties: {
          oneOf: [{ type: "integer" }, { type: "number" }, { type: "string" }],
        },
        type: "object",
      },
      { type: "string" },
      {
        additionalProperties: {
          oneOf: [
            { items: { type: "string" }, type: "array" },
            { type: "integer" },
          ],
        },
        type: "object",
      },
      {
        items: { oneOf: [{ type: "number" }, { type: "integer" }] },
        type: "array",
      },
    ],
  });
});

test("_unique_schemas", () => {
  const unique = _oas2._unique_schemas(schemas);

  expect(unique).toEqual([
    {
      additionalProperties: {
        oneOf: [{ type: "integer" }, { type: "number" }, { type: "string" }],
      },
      type: "object",
    },
    { type: "string" },
    {
      additionalProperties: {
        oneOf: [
          { items: { type: "string" }, type: "array" },
          { type: "integer" },
        ],
      },
      type: "object",
    },
    {
      items: { oneOf: [{ type: "number" }, { type: "integer" }] },
      type: "array",
    },
  ]);
});

test("_split_schemas_by_type", () => {
  const split = _oas2._split_schemas_by_type(schemas);
  expect(split).toEqual({
    array: [
      {
        items: { oneOf: [{ type: "number" }, { type: "integer" }] },
        type: "array",
      },
    ],
    object: [
      {
        additionalProperties: {
          oneOf: [{ type: "integer" }, { type: "number" }, { type: "string" }],
        },
        type: "object",
      },
      {
        additionalProperties: {
          oneOf: [
            { items: { type: "string" }, type: "array" },
            { type: "integer" },
          ],
        },
        type: "object",
      },
    ],
    string: [{ type: "string" }, { type: "string" }],
  });
});
