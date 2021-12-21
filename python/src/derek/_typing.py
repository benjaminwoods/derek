from typing import *
from sys import version_info

if version_info >= (3, 10):
    JSON = List[Dict[str, "JSON"]] | Dict[str, "JSON"]
    "Static type for JSON-serializable list/dict."
else:
    JSON = Union[List[Dict[str, "JSON"]], Dict[str, "JSON"]]
    "Static type for JSON-serializable list/dict."

DerekType = ForwardRef("derek.Derek")
"Static type for Derek."

ParserType = ForwardRef("derek.Parser")
"Static type for Parser."
