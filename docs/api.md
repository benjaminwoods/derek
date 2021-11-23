# derek API


### class derek.Derek(parent=None, children=None, value=None, name=None)
A node in a data structure.

Contains information about itself, its parent node, and any child nodes.


#### example()
Generate example JSON from self.


#### parse(format='oas3')
Convert a tree of Derek nodes to a given format.


#### property parser()
Return an instance of the parser class.


#### serialize(format='oas3')
Convert tree to a string.


#### classmethod tree(obj, parent=None, name=None)
Create a tree.


### class derek.Parser()

#### classmethod oas3(node)
Convert a data structure, with `node` as the root node,
into OAS3 schema. (Alias for OAS2.)

#### classmethod oas2(node)
Convert a data structure, with `node` as the root node,
into OAS2 schema. (Alias for OAS3.)

# Indices and tables


* Index


* Module Index


* Search Page
