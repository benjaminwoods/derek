import json

import pytest

from derek import Derek

from derek._parse import _oas2


@pytest.fixture
def node():
    obj = [{"a": 1, "b": "b1", "c": 3.0}, {"a": 4, "b": ["b2"]}, [1, 2, 3.0]]

    return Derek.tree(obj)


@pytest.fixture
def schemas():
    return [
        {
            "additionalProperties": {
                "oneOf": [
                    {"type": "integer"},
                    {"type": "number"},
                    {"type": "string"},
                ]
            },
            "type": "object",
        },
        {"type": "string"},
        {
            "additionalProperties": {
                "oneOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "integer"},
                ]
            },
            "type": "object",
        },
        {
            "items": {"oneOf": [{"type": "number"}, {"type": "integer"}]},
            "type": "array",
        },
        {"type": "string"},
    ]


def test__oneOf(schemas):
    result = _oas2._oneOf(schemas)

    assert result == {
        "oneOf": [
            {
                "additionalProperties": {
                    "oneOf": [
                        {"type": "integer"},
                        {"type": "number"},
                        {"type": "string"},
                    ]
                },
                "type": "object",
            },
            {"type": "string"},
            {
                "additionalProperties": {
                    "oneOf": [
                        {"items": {"type": "string"}, "type": "array"},
                        {"type": "integer"},
                    ]
                },
                "type": "object",
            },
            {
                "items": {"oneOf": [{"type": "number"}, {"type": "integer"}]},
                "type": "array",
            },
        ]
    }


def test__unique_schemas(schemas):
    not_ordered = _oas2._unique_schemas(schemas, ordered=False)
    ordered = _oas2._unique_schemas(schemas, ordered=True)

    for element in not_ordered:
        assert element in ordered
    assert len(not_ordered) == len(ordered)

    assert ordered == [
        {
            "additionalProperties": {
                "oneOf": [
                    {"type": "integer"},
                    {"type": "number"},
                    {"type": "string"},
                ]
            },
            "type": "object",
        },
        {"type": "string"},
        {
            "additionalProperties": {
                "oneOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "integer"},
                ]
            },
            "type": "object",
        },
        {
            "items": {"oneOf": [{"type": "number"}, {"type": "integer"}]},
            "type": "array",
        },
    ]


class Test__oas2_dict:
    @pytest.fixture(scope="class")
    def node(self):
        obj = {"a": 1, "b": "b1", "c": 3.0}

        return Derek.tree(obj)

    def test_permissive(self, node):
        result = _oas2._oas2_dict(node, strategy="permissive")

        assert result == {
            "type": "object",
            "additionalProperties": {
                "oneOf": [
                    {"type": "integer"},
                    {"type": "string"},
                    {"type": "number"},
                ]
            },
        }

    def test_restricted(self, node):
        result = _oas2._oas2_dict(node, strategy="restricted")

        assert result == {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "string"},
                "c": {"type": "number"},
            },
        }

    def test_inner_join(self, node):
        result = _oas2._oas2_dict(node, strategy="inner_join")

        assert result == {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "string"},
                "c": {"type": "number"},
            },
        }


class Test__oas2_list:
    @pytest.fixture(scope="class")
    def node(self):
        obj = [{"a": 1, "b": "b1", "c": 3.0}, {"a": 4, "b": ["b2"]}, [1, 2, 3.0]]

        return Derek.tree(obj)

    def test_permissive(self, node):
        result = _oas2._oas2_list(node, strategy="permissive")

        assert result == {
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
                    {
                        "items": {
                            "oneOf": [
                                {"type": "integer"},
                                {"type": "number"},
                            ]
                        },
                        "type": "array",
                    },
                ]
            },
        }

    def test_restricted(self, node):
        result = _oas2._oas2_list(node, strategy="restricted")

        assert result == {
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
                    {
                        "items": {
                            "oneOf": [
                                {"type": "integer"},
                                {"type": "number"},
                            ]
                        },
                        "type": "array",
                    },
                ]
            },
        }

    def test_inner_join(self, node):
        result = _oas2._oas2_list(node, strategy="inner_join")

        assert result == {
            "type": "array",
            "items": {
                "oneOf": [
                    {
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
                    {
                        "items": {
                            "oneOf": [
                                {"type": "integer"},
                                {"type": "number"},
                            ]
                        },
                        "type": "array",
                    },
                ]
            },
        }
