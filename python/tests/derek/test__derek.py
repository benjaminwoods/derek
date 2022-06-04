import pytest

from derek._derek import Derek
from derek._parse import Parser


class Test_Initialization:
    def test_defaults(self):
        """
        Try making a Derek node, using defaults.
        """

        node = Derek()
        assert node.parent is None
        assert node.children is None
        assert node.value is None
        assert node.name is None

    def test_with_arguments(self):
        """
        Try making a Derek node, specifying arguments.
        """

        parent = Derek()
        attributes = {
            "parent": parent,
            "children": [1, 2, 3],
            "value": [1, 2, 3],
            "name": "some_node",
        }
        node = Derek(**attributes)
        for k, v in attributes.items():
            assert getattr(node, k) == v


class TreeBaseTest:
    def check(self, obj, **kwargs):
        node = Derek.tree(obj, **kwargs)
        if any(map(lambda t: isinstance(obj, t), [list, dict])):
            # If obj is a subclass of any out of [list, dict]
            assert node.value is obj

        if "name" in kwargs:
            assert node.name == kwargs["name"]
        elif "parent" in kwargs:
            assert node.parent is kwargs["parent"]

        # TODO: check child nodes


class Test_Tree(TreeBaseTest):
    def test_name(self):
        """
        Try making a Derek tree from an integer,
        specifying the name of the root node.
        """
        # TODO: upgrade to monkey test

        args = (3141,)
        kwargs = {"name": "some_node_name"}

        self.check(*args, **kwargs)

    def test_no_name(self):
        """
        Try making a Derek tree from an integer,
        without specifying the name of the root node.
        """
        # TODO: upgrade to monkey test

        args = (3141,)

        self.check(*args)

    def test_parent(self):
        """
        Try making a Derek subtree from an integer,
        specifying the parent node.
        """

        args = (3141,)
        kwargs = {"parent": Derek()}

        self.check(*args, **kwargs)

    def test_no_parent(self):
        """
        Try making a Derek tree from an integer,
        without specifying the name of the root node.
        """

        args = (3141,)

        self.check(*args)

    def test_non_iterable(self):
        """
        Try making a Derek tree from a non-iterable object,
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = (3141,)

        self.check(*args)

    def test_simple_list(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = ([1, 2, 3],)

        self.check(*args)

    def test_list_in_list(self):
        """
        Try making a Derek tree from a list in list (depth 2),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]],)

        self.check(*args)

    def test_list_in_dict(self):
        """
        Try making a Derek tree from a list in dict (depth 2),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = ({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]},)

        self.check(*args)

    def test_simple_dict(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = ({"a": 1, "b": 2, "c": 3},)

        self.check(*args)

    def test_dict_in_dict(self):
        """
        Try making a Derek tree from a dict in dict (depth 2),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = (
            {
                "a": {"d": 1, "e": 2, "f": 3},
                "b": {"g": 4, "h": 5, "i": 6},
                "c": {"j": 7, "k": 8, "l": 9},
            },
        )

        self.check(*args)

    def test_dict_in_list(self):
        """
        Try making a Derek tree from a dict in list (depth 2),
        without specifying the name of the root node.
        """
        # TODO: monkey testing

        args = (
            [
                {"d": 1, "e": 2, "f": 3},
                {"g": 4, "h": 5, "i": 6},
                {"j": 7, "k": 8, "l": 9},
            ],
        )

        self.check(*args)


class Test_Example:
    def test_non_iterable(self):
        """
        Try making a Derek tree from a non-iterable object,
        then return an example.
        """
        # TODO: upgrade to monkey test

        obj = 3141
        node = Derek.tree(obj)
        assert node.example() == obj

    def test_none(self):
        """
        Make a Derek instance with value as None, then return an example.
        """

        node = Derek()
        assert node.example() is None

    def test_unusual_value(self):
        """
        Make a Derek instance with value as a bespoke instance, then return an
        example.
        """

        class Unusual:
            def __init__(self):
                self.a = [1]
                self.b = {4: 5}

        obj = Unusual()
        node = Derek(value=obj)
        example = node.example()
        assert isinstance(example, Unusual)
        for k in example.__dict__.keys():
            assert example.__dict__[k] == obj.__dict__[k]
            assert example.__dict__[k] is not obj.__dict__[k]

    def test_empty_list(self):
        """
        Make a Derek instance with value as [], then return an example.
        """

        obj = []
        node = Derek(value=obj)
        example = node.example()
        assert example == obj
        assert example is not obj

    def test_simple_list(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        then return an example.
        """
        # TODO: upgrade to monkey test

        obj = [1, 2, 3]
        node = Derek.tree(obj)
        assert node.example() == [1]

    def test_list_in_list(self):
        """
        Try making a Derek tree from a list in list (depth 2),
        then return an example.
        """
        # TODO: monkey testing

        obj = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        node = Derek.tree(obj)
        assert node.example() == [[1]]

    def test_list_in_dict(self):
        """
        Try making a Derek tree from a list in dict (depth 2),
        then return an example.
        """
        # TODO: monkey testing

        obj = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}
        node = Derek.tree(obj)
        assert node.example() == {"a": [1], "b": [4], "c": [7]}

    def test_empty_dict(self):
        """
        Make a Derek instance with value as {}, then return an example.
        """

        obj = {}
        node = Derek(value=obj)
        example = node.example()
        assert example == obj
        assert example is not obj

    def test_simple_dict(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        then return an example.
        """
        # TODO: monkey testing

        obj = {"a": 1, "b": 2, "c": 3}
        node = Derek.tree(obj)
        assert node.example() == {"a": 1, "b": 2, "c": 3}

    def test_dict_in_dict(self):
        """
        Try making a Derek tree from a dict in dict (depth 2),
        then return an example.
        """
        # TODO: monkey testing

        obj = {
            "a": {"d": 1, "e": 2, "f": 3},
            "b": {"g": 4, "h": 5, "i": 6},
            "c": {"j": 7, "k": 8, "l": 9},
        }
        node = Derek.tree(obj)
        assert node.example() == {
            "a": {"d": 1, "e": 2, "f": 3},
            "b": {"g": 4, "h": 5, "i": 6},
            "c": {"j": 7, "k": 8, "l": 9},
        }

    def test_dict_in_list(self):
        """
        Try making a Derek tree from a dict in list (depth 2),
        then return an example.
        """
        # TODO: monkey testing

        obj = [
            {"d": 1, "e": 2, "f": 3},
            {"g": 4, "h": 5, "i": 6},
            {"j": 7, "k": 8, "l": 9},
        ]
        node = Derek.tree(obj)
        assert node.example() == [{"d": 1, "e": 2, "f": 3}]


class Test_Parser:
    def test_parser_class(self):
        """
        Check if Derek.parser returns a Parser.
        """

        parser = Derek().parser
        assert parser is Parser


class Test_Parse:
    @pytest.fixture
    def node(self):
        obj = [{"a": 1, "b": "b1", "c": 3.0}, {"a": 4, "b": ["b2"]}]
        return Derek.tree(obj)

    def test_format_not_implemented(self, node):
        """
        Check if an unimplemented format raises correct Exception.
        """
        with pytest.raises(NotImplementedError):
            node.parse(format="not_a_real_format")

    def test_parse_oas3_permissive(self, node):
        """
        Check if Derek().parse (OAS3) produces expected result for
        "permissive" strategy
        """

        j = node.parse("oas3", strategy="permissive")

        assert j == {
            "untitled": {
                "type": "array",
                "items": {
                    "oneOf": [
                        {
                            "type": "object",
                            "additionalProperties": {
                                "oneOf": [
                                    {"type": "integer"},
                                    {"type": "string"},
                                    {"type": "number"},
                                ]
                            },
                        },
                        {
                            "type": "object",
                            "additionalProperties": {
                                "oneOf": [
                                    {"type": "integer"},
                                    {"type": "array", "items": {"type": "string"}},
                                ]
                            },
                        },
                    ]
                },
                "example": [{"a": 1, "b": "b1", "c": 3.0}],
            }
        }

    def test_parse_oas3_restricted(self, node):
        """
        Check if Derek().parse (OAS3) produces expected result for
        "restricted" strategy
        """

        j = node.parse("oas3", strategy="restricted")
        assert j == {
            "untitled": {
                "type": "array",
                "items": {
                    "oneOf": [
                        {
                            "type": "object",
                            "properties": {
                                "a": {"type": "integer"},
                                "b": {"type": "string"},
                                "c": {"type": "number"},
                            },
                        },
                        {
                            "type": "object",
                            "properties": {
                                "a": {"type": "integer"},
                                "b": {"type": "array", "items": {"type": "string"}},
                            },
                        },
                    ]
                },
                "example": [{"a": 1, "b": "b1", "c": 3.0}],
            }
        }

    def test_parse_oas3_inner_join(self, node):
        """
        Check if Derek().parse (OAS3) produces expected result for
        "inner_join" strategy
        """

        j = node.parse("oas3", strategy="inner_join")
        assert j == {
            "untitled": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "array", "items": {"type": "string"}},
                            ]
                        },
                        "c": {"type": "number"},
                    },
                    "required": ["a", "b"],
                },
                "example": [{"a": 1, "b": "b1", "c": 3.0}],
            }
        }

    def test_parse_with_name(self):
        node = Derek(value=1, name="test")
        assert node.parse() == {"test": {"example": 1, "type": "integer"}}
