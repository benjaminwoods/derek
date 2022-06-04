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
