# derek [Documentation](index.md) / Features

- Convert data structure to OAS2 or OAS3 compliant schema

  (use `Derek.tree(input_json).parse(format="oas3")`)

  - If elements in a list or values in a dictionary differ in type,
    Derek will automatically use `oneOf`, with each of the subschemas.
  - The following data types are supported for elements/values in your
    data structure:
    - List and dictionary
    - String, integer, float, and bool

- Get simplified, reduced JSON (for testing and examples) from a JSON

  (use `Derek(input_json).example()`)

## Python implementation

- Install straight from the git repository:
  ```bash
  pip install "git+https://github.com/benjaminwoods/derek.git@0.0.1#egg=derek"
  ```
