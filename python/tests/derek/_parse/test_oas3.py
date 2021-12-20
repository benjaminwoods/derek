import json

import pytest

from derek._parse import Parser
from derek._derek import Derek


class OAS3BaseTest:
    def JSON(self, obj, **kwargs):
        node = Derek.tree(obj, **kwargs)

        return Parser.oas3(node)

        # TODO: check child nodes


class Test_OAS3(OAS3BaseTest):
    def test_integer(self):
        """
        Try making a Derek tree from an integer,
        then convert to OAS3 dictionary.
        """
        # TODO: upgrade to monkey test

        args = (3141,)

        j = self.JSON(*args)
        assert j == {"type": "integer"}

    def test_string(self):
        """
        Try making a Derek tree from a string,
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ("abc",)

        j = self.JSON(*args)
        assert j == {"type": "string"}

    def test_float(self):
        """
        Try making a Derek tree from a float,
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = (3.141,)

        j = self.JSON(*args)
        assert j == {"type": "number"}

    def test_bool(self):
        """
        Try making a Derek tree from a bool,
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = (True,)

        j = self.JSON(*args)
        assert j == {"type": "boolean"}

    def test_empty_list(self):
        """
        Try making a Derek tree from an empty list,
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ([],)

        j = self.JSON(*args)
        assert j == {"type": "array", "items": {}, "maxItems": 0}

    def test_simple_list(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ([1, 2, 3],)

        j = self.JSON(*args)
        assert j == {"type": "array", "items": {"type": "integer"}}

    def test_list_in_list(self):
        """
        Try making a Derek tree from a list in list (depth 2),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]],)

        j = self.JSON(*args)
        assert j == {
            "type": "array",
            "items": {"type": "array", "items": {"type": "integer"}},
        }

    def test_list_in_dict(self):
        """
        Try making a Derek tree from a list in dict (depth 2),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]},)

        j = self.JSON(*args)
        assert j == {
            "type": "object",
            "additionalProperties": {"type": "array", "items": {"type": "integer"}},
        }

    def test_empty_dict(self):
        """
        Try making a Derek tree from an empty dict,
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ({},)

        with pytest.raises(NotImplementedError):
            j = self.JSON(*args)

    def test_simple_dict(self):
        """
        Try making a Derek tree from a simple list (depth 1),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = ({"a": 1, "b": 2, "c": 3},)

        j = self.JSON(*args)
        assert j == {"type": "object", "additionalProperties": {"type": "integer"}}

    def test_dict_in_dict(self):
        """
        Try making a Derek tree from a dict in dict (depth 2),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = (
            {
                "a": {"d": 1, "e": 2, "f": 3},
                "b": {"g": 4, "h": 5, "i": 6},
                "c": {"j": 7, "k": 8, "l": 9},
            },
        )

        j = self.JSON(*args)
        assert j == {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"type": "integer"},
            },
        }

    def test_dict_in_list(self):
        """
        Try making a Derek tree from a dict in list (depth 2),
        then convert to OAS3 dictionary.
        """
        # TODO: monkey testing

        args = (
            [
                {"d": 1, "e": 2, "f": 3},
                {"g": 4, "h": 5, "i": 6},
                {"j": 7, "k": 8, "l": 9},
            ],
        )

        j = self.JSON(*args)
        assert j == {
            "type": "array",
            "items": {"type": "object", "additionalProperties": {"type": "integer"}},
        }

    def test_unparseable_type(self):
        """
        Make a Derek instance with value as a bespoke instance, then try to
        convert to OAS3 dictionary.
        """

        class Unusual:
            def __init__(self):
                self.a = [1]
                self.b = {4: 5}

        args = (Unusual(),)
        with pytest.raises(NotImplementedError):
            j = self.JSON(*args)
