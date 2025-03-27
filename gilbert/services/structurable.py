import json
from abc import ABC, abstractmethod
from typing import Self

import cattrs


class Structurable(ABC):
    """Base class for attrs class with defined cattrs converter.

    The class is a wrapper to provide unstructure/structure serialize/deserialize functions.
    """

    @classmethod
    @abstractmethod
    def converter(cls) -> cattrs.Converter:
        """Class converter"""

    def unstructure(self) -> dict:
        """Convert the object to a dict."""
        return self.converter().unstructure(self)

    @classmethod
    def structure(cls, obj: dict) -> Self:
        """Convert a dict to an object."""
        return cls.converter().structure(obj, cls)

    def to_json(self) -> str:
        """Convert the object to a JSON string."""
        return json.dumps(self.unstructure())

    @classmethod
    def from_json(cls, s: str) -> Self:
        """Convert a JSON string to an object."""
        return cls.structure(json.loads(s))
