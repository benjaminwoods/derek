derek
=====

*(Python implementation)*

|License| |Python code coverage|

Tools for converting data into schema.

(Still very much pre-alpha!)

1. `Installation <installation_>`_
2. `What is Derek? <what_>`_

   1. `Document data structures <document_>`_
   2. `Extract schemas from APIs <extract_>`_
   3. `Really lightweight <really_>`_
   4. `Extensible <extensible_>`_
   5. `KISS <kiss_>`_

3. `Specification <https://github.com/benjaminwoods/derek/blob/v0.0.1/docs/spec.md>`_
4. `API <https://github.com/benjaminwoods/derek/blob/v0.0.1/docs/api.md>`_

.. _installation:

Installation
------------

Using ``pip``
~~~~~~~~~~~~~~~~~

.. code:: bash

   pip install derek

Build from source
~~~~~~~~~~~~~~~~~

.. code:: bash

   git clone https://github.com/benjaminwoods/derek.git
   pip install python/requirements/build.txt
   python -m build python
   pip install python/dist/derek_

.. _what:

What is Derek?
--------------

.. _document:

Derek documents data structures.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load some data into a tree of nodes:

.. code:: python

   # Import the main class
   from derek import Derek

   # Suppose that you have some JSON-compatible data
   obj = [
     {
       'some': [1.0, 3, "4.5"],
       'data': [3.4, 4.5]
     },
     {
       'some': [2, "4.0", 1.5],
       'data': [1.4]
     }
   ]

   # Feed this data into Derek.tree
   root_node = Derek.tree(obj, name='MyDataStructure')

You can use ``.example()`` to see a simple example item of data:

.. code:: python

   >>> root_node.example()
   [{'some': [1.0], 'data': [3.4]}]

You can produce an OAS2/OAS3 JSON schema from this data, too:

.. code:: python

   j = root_node.parse(format='oas3')
   import json
   print(json.dumps(j, indent=2))

.. code:: json

   {
     "MyDataStructure": {
       "type": "array",
       "items": {
         "type": "object",
         "additionalProperties": {
           "oneOf": [
             {
               "type": "array",
               "items": {
                 "oneOf": [
                   {
                     "type": "string"
                   },
                   {
                     "type": "integer"
                   },
                   {
                     "type": "number"
                   }
                 ]
               }
             },
             {
               "type": "array",
               "items": {
                 "type": "number"
               }
             }
           ]
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

Install and use the `yaml <https://github.com/yaml/pyyaml>`_ package to
convert this structure to an OAS3-compliant data schema.

.. code:: json

   import yaml
   print(yaml.dump(j))

.. code:: yaml

   MyDataStructure:
     example:
     - data:
       - 3.4
       some:
       - 1.0
     items:
       additionalProperties:
         oneOf:
         - items:
             type: number
           type: array
         - items:
             oneOf:
             - type: number
             - type: integer
             - type: string
           type: array
       type: object
     type: array

.. _extract:

Derek extracts schemas from APIs.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quickly extract schemas from APIs, by feeding the returned JSON into
Derek.

.. code:: python

   from derek import Derek

   from pycoingecko import CoinGeckoAPI
   cg = CoinGeckoAPI()

   # Get all coins from CoinGecko
   root_node = Derek.tree(cg.get_coins_list(), name='GetCoins')

Parse to get your schema:

.. code:: python

   j = root_node.parse(format='oas3')
   import json
   print(json.dumps(j, indent=2))

.. code:: json
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

.. _really:

Derek is really lightweight.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**No required dependencies. Always.**

.. _extensible:

Derek is extensible.
~~~~~~~~~~~~~~~~~~~~

Use libraries like `pywhat <https://github.com/bee-san/pyWhat>`_ and
`yaml <https://github.com/yaml/pyyaml>`_ to quickly extend ``Derek``:

.. code:: python

   import json, yaml

   from derek import Derek, Parser

   from pywhat import Identifier

   class PywhatDerek(Derek):
       @property
       def parser(self):
           return PywhatParser()

       def parse_to_yaml(self, *args, **kwargs):
           return yaml.dump(
               self.parse(*args, **kwargs)
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

Allowing for functionality like:

.. code:: python

   root_node = PywhatDerek.tree({
       'data': ['17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem']
   }, name='Addresses')
   root_node.get_oas3_yaml()

returning:

.. code:: yaml

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

.. _kiss:

Derek is straightforward.
-------------------------

Derek is designed for ease of use. If you’re trying to use Derek
functionality in a workflow and it feels like it should be easier to get
your desired result, please make an issue.

.. |License| image:: https://github.com/benjaminwoods/derek/blob/v0.0.1/.badges/license.svg
.. |Python code coverage| image:: https://github.com/benjaminwoods/derek/blob/v0.0.1/.badges/coverage/python.svg
