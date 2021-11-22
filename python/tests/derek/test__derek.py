from derek import _derek

class TestDerek:
    def test_initialization(self):
        """
        Try making a Derek node.
        """

        node = _derek.Derek()
        assert node.parent is None
        assert node.children is None
        assert node.value is None
        assert node.name is None

        parent = node
        attributes = {
            "parent": parent,
            "children": [1, 2, 3],
            "value": [1, 2, 3],
            "name": "some_node"
        }
        node = _derek.Derek(**attributes)
        for k,v in attributes.items():
            assert getattr(node, k) == v
