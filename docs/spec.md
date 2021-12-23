# derek [Documentation](index.md) / Specification

## How Derek works

### Derek as a graph

When you use `Derek.tree()`, you make a directed graph, where each node knows:

- it's parent node (if any)
- it's child nodes (if any)

This graph is traversable using the root node, which is returned by `Derek.tree()`.

Each node in the tree contains the following information:

- the parent node (as a Derek instance)
- the child nodes (each as Derek instances, too)
- a data structure

That data structure is the data structure assuming that the node is the root node of a tree.

## How parsing works

Parsing works by walking along the tree using a pre-order walk.

1. Start at the root node.
2. For the given node, go to the first child node.
   1. If there are no children, parse the data in the current node, and return a JSON representation of the schema. (End.)
   2. If there are children, check what the data type of the node is.
      1. For non-optimized data types:
         - parse each child node (go to 2), and store the results in an array
         - do some operation on that array to determine how to construct the JSON representation for the current node
         - return that representation
      2. For optimized data types:
         - run a callback that parses each child node (going to 2)
         - run an operation using that callback to determine how to consturct the JSON representation for the current node
         - return that representation.
