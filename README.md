# derek

Tools for converting data into schema.

(Still very much pre-alpha!)

1. [Installation](#installation)
2. [What is Derek?](#what)
    1. [Document data structures](#document)
    2. [Extract schemas from APIs](#extract)
    3. [Really lightweight](#really)
    4. [Extensible](#extensible)
    5. [KISS](#kiss)
3. [Specification](docs/spec.md)
3. [API](docs/api.md)

## Installation

This isn't available on pip yet, but you can install this directly from
the GitHub repo:

```bash
pip install "git+https://github.com/benjaminwoods/derek.git@0.0.1#egg=derek_0.0.1&subdirectory=python"
```

## What is Derek? <a name="what"></a>
### Derek documents data structures. <a name="data"></a>

Load some data into a tree of nodes:

```python
# Import the main class
from derek import Derek

# Suppose that you have some JSON-compatible data
obj = [
  {
    'some': [1.0, 3.0, 4.5],
    'data': [3.4, 4.5]
  },
  {
    'some': [2.0, 4.0, 1.5],
    'data': [1.4]
  }
]

# Feed this data into Derek.tree
root_node = Derek.tree(obj, name='MyDataStructure')
```

You can use `.example()` to see a simple example item of data:

```python
>>> root_node.example()
[{'some': [1.0, 3.0, 4.5], 'data': [3.4, 4.5]}]
```

You can produce an OAS2/OAS3 JSON schema from this data, too:

```python
>>> root_node.serialize(format='oas3')
{
  "MyDataStructure": {
    "type": "array",
    "items": {
      "type": "object",
      "additionalProperties": {
        "type": "array",
        "items": {
          "type": "number"
        }
      }
    },
    "example": [
      {
        "some": [
          1.0
        ],
        "data": [
          3.4
        ]
      }
    ]
  }
}
```

### Derek extracts schemas from APIs.

Quickly extract schemas from APIs, by feeding the returned JSON into Derek.

```python
from derek import Derek

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# Get all coins from CoinGecko
root_node = Derek.tree(cg.get_coins_list(), name='GetCoins')
```

Serialize to get your schema:

```python
>>> root_node.serialize(format='oas3')
{
  "GetCoins": {
    "type": "array",
    "items": {
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    },
    "example": [
      {
        "id": "01coin",
        "symbol": "zoc",
        "name": "01coin"
      }
    ]
  }
}
```

### Derek is really lightweight.

**No required dependencies. Always.**

### Derek is extensible.

Use libraries like `pywhat` and `yaml` to quickly extend `Derek`:

```python
import json, yaml

from derek import Derek, Parser

from pywhat import Identifier

class PywhatDerek(Derek):
    @property
    def parser(self):
        return PywhatParser()

    def serialize_to_yaml(self, *args, **kwargs):
        return yaml.dump(
            json.loads(
                self.serialize(*args, **kwargs)
            )
        )

class PywhatParser(Parser):
    @classmethod
    def oas2(cls, node):
        # Call the superclass parser for the current node:
        #   _sup = cls.__mro__[PywhatParser.__mro__.index(int):]
        #   j = _sup.oas2(cls, node)
        # All calls to the oas2 method in the superclass therefore re-route
        # back to this class method, automatically handling all recursive calls
        # here.
        j = super(PywhatParser, cls).oas2(node)

        # The rest of this function simply patches in results from a call
        # to the pywhat API.
        identifier = Identifier()

        if all(map(lambda t: not isinstance(node.value, t), [list, dict])):
            result = identifier.identify(str(node.value))

            if result['Regexes'] is not None:
                matches = [entry for entry in result['Regexes']['text']]

                # Select the match as the longest string
                map_func = lambda d: (d['Matched'], d['Regex Pattern']['Name'])
                max_func = lambda tup: len(tup[0])
                _, match = max(
                    map(map_func, matches),
                    key=max_func
                )

                j = {
                    **j,
                    'description': match
                }

        return j
```

Allowing for functionality like:

```python
root_node = PywhatDerek.tree({
    'data': ['17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem']
}, name='Addresses')
root_node.serialize_to_yaml()
```

returning:

```yaml
Addresses:
  additionalProperties:
    items:
      description: "Bitcoin (\u20BF) Wallet Address"
      type: string
    type: array
  example:
    data:
    - 17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem
  type: object
```

## Derek is straightforward. <a name="kiss"></a>

Derek is designed for ease of use. If you're trying to use Derek functionality
in a workflow and it feels like it should be easier to get your desired result,
please make an issue.
