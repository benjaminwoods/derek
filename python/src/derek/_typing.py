from typing import *
from sys import version_info

if version_info >= (3, 10):
    JSON = List[Dict[str, "JSON"]] | Dict[str, "JSON"]
    "Static type for JSON-serializable list/dict."
else:
    JSON = Union[List[Dict[str, "JSON"]], Dict[str, "JSON"]]
    "Static type for JSON-serializable list/dict."

if version_info >= (3, 7, 4):
    DerekType = ForwardRef("derek.Derek")
    "Static type for Derek."

    ParserType = ForwardRef("derek.Parser")
    "Static type for Parser."
else:
    DerekType = "derek.Derek"
    "Static type for Derek."

    ParserType = "derek.Parser"
    "Static type for Parser."
