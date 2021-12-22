# derek API

### `class derek.Derek(parent=None, children=None, value=None, name=None)`

A node in a data structure.

Contains information about itself, its parent node, and any child nodes.

- **Parameters**

  - **parent** (`Optional[derek.Derek]`) – Parent node.

  If specified, the Derek instance stores a reference to the parent
  node.

  The Derek instance is _not_ added to the `children` of the
  parent node.

  If not specified, the Derek instance has `parent`
  set to `None`.

  - **children** (`Optional[Iterable[derek.Derek]]`) – Child nodes.

  If specified, the Derek instance stores a reference to the children
  nodes.

  The Derek instance is _not_ added as a `parent` for any of the
  child nodes.

  If not specified, the Derek instance has `children`
  set to `None`.

  - **value** (`derek._typing.JSON`) – A JSON-serializable dictionary/list.

  - **name** (`Optional[str]`) – Name of the returned Derek instance.

#### `example()`

Generate example JSON-serializable dictionary from self.

The example yields the same schema as a tree created
with self.value.

- **Returns**

  **j** – Example, as a JSON-serializable dictionary.

- **Return type**

  `derek._typing.JSON`

#### `parse(format='oas3')`

Convert a tree of Derek nodes to a given format.

- **Parameters**

  **format** (`str`) – Output format.

- **Returns**

  **j** – A JSON-serializable dictionary/list.

- **Return type**

  `derek._typing.JSON`

#### `property parser`

Return an instance of the parser class.

- **Returns**

  Instance of the parser class.

- **Return type**

  `derek.Parser`

#### `classmethod tree(obj, parent=None, name=None)`

Create a tree representation of `obj`.

- **Parameters**

  - **obj** (`derek._typing.JSON`) – A JSON-serializable dictionary/list.

  - **parent** (`Optional[derek.Derek]`) – Parent node to attach subtree to.

  If specified, the returned Derek instance is attached as a child
  of the node.

  If not specified, the returned Derek instance has `parent`
  set to `None`.

  - **name** (`Optional[str]`) – Name of the returned Derek instance.

- **Returns**

  - Tree representation of `obj`, as a Derek instance.

  - `obj` is identical (same `id`) to self.value.

- **Return type**

  `derek.Derek`

### `class derek.Parser()`

#### `classmethod oas2(node)`

Convert a data structure, with `node` as the root node,
into OAS2 schema.

- **Parameters**

  **node** (`Derek`) – Root node of tree.

- **Returns**

  **j** – OAS2 schema, as JSON-serializable dictionary.

- **Return type**

  `derek._typing.JSON`

#### `classmethod oas3(node)`

Convert a data structure, with `node` as the root node,
into OAS3 schema. (Alias for OAS2.)

- **Parameters**

  **node** (`Derek`) – Root node of tree.

- **Returns**

  **j** – OAS2 schema, as JSON-serializable dictionary.

- **Return type**

  `derek._typing.JSON`

### `derek._typing.JSON()`

Static type for JSON-serializable list/dict.

alias of `Union[List[Dict[str, JSON]], Dict[str, JSON]]`
