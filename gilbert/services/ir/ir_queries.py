__all__ = [
    "Query",
    "BooleanQuery",
    "AllQuery",
    "AnyQuery",
    "NotQuery",
    "FieldQuery",
    "TermQuery",
    "TermsQuery",
    "WordQuery",
    "WordsQuery",
    "WildcardQuery",
    "RangeQuery",
    "ExistsQuery",
    "SpecialQuery",
    "NearQuery",
    "NestedQuery",
    "LiteralNotQuery",
    "PydanticIrQuery",
    "KNNQuery",
]

from abc import ABC
from typing import Annotated, Literal, Optional

import attrs
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema


@attrs.define
class Query(ABC):
    """Abstract class for a query in IR."""

    type: Literal[None] = attrs.field()
    boost: float = attrs.field(default=1.0)

    @staticmethod
    def validate(val):
        from gilbert.services.ir import validate_query

        return validate_query(val)

    @staticmethod
    def serialize(val) -> dict | None:
        from gilbert.services.ir import serialize_query

        return serialize_query(val)


PydanticIrQuery = Annotated[
    Query,
    AfterValidator(Query.validate),
    PlainSerializer(Query.serialize),
    WithJsonSchema(
        {
            "type": "object",
            "examples": [{"type": "term", "field": "id", "value": "abc"}],
        }
    ),
]


@attrs.define(kw_only=True)
class BooleanQuery(Query):
    type: Literal["boolean"] = attrs.field(default="boolean", init=False)  # type: ignore[assignment]
    booleanQuery: str = attrs.field()
    caseSensitive: Literal["yes", "no"] = attrs.field(default="no")


@attrs.define(kw_only=True)
class AllQuery(Query):
    type: Literal["all"] = attrs.field(default="all", init=False)  # type: ignore[assignment]
    allQueries: list[Query] = attrs.field(factory=list)


@attrs.define(kw_only=True)
class AnyQuery(Query):
    type: Literal["any"] = attrs.field(default="any", init=False)  # type: ignore[assignment]
    anyQueries: list[Query] = attrs.field(factory=list)


@attrs.define(kw_only=True)
class NotQuery(Query):
    type: Literal["not"] = attrs.field(default="not", init=False)  # type: ignore[assignment]
    matchQuery: Query = attrs.field()
    notMatchQuery: Query = attrs.field()


@attrs.define(kw_only=True)
class FieldQuery(Query):
    pass


@attrs.define(kw_only=True)
class TermQuery(FieldQuery):
    type: Literal["term"] = attrs.field(default="term", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    value: str | bool | int = attrs.field()


@attrs.define(kw_only=True)
class TermsQuery(FieldQuery):
    type: Literal["terms"] = attrs.field(default="terms", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    values: list[str | bool | int] = attrs.field()


@attrs.define(kw_only=True)
class WordQuery(FieldQuery):
    type: Literal["word"] = attrs.field(default="word", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    value: str = attrs.field()
    flags: Optional[list[str]] = attrs.field(default=None)
    minFreq: Optional[int] = attrs.field(default=None)
    maxFreq: Optional[int] = attrs.field(default=None)


@attrs.define(kw_only=True)
class WordsQuery(FieldQuery):
    type: Literal["words"] = attrs.field(default="words", init=False)  # type: ignore[assignment]
    fields: list[str] = attrs.field()
    values: list[str] = attrs.field()
    flags: Optional[list[str]] = attrs.field(default=None)
    minFreq: Optional[int] = attrs.field(default=None)
    maxFreq: Optional[int] = attrs.field(default=None)


@attrs.define(kw_only=True)
class WildcardQuery(FieldQuery):
    type: Literal["wildcard"] = attrs.field(default="wildcard", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    value: str = attrs.field()
    flags: Optional[list[str]] = attrs.field(default=None)


@attrs.define(kw_only=True)
class RangeQuery(FieldQuery):
    type: Literal["range"] = attrs.field(default="range", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    from_: int | str = attrs.field(default=None)
    to_: int | str = attrs.field(default=None)
    includeFrom: bool = attrs.field(default=True)
    includeTo: bool = attrs.field(default=False)

    def __attrs_post_init__(self):
        if self.from_ is None and self.to_ is None:
            raise ValueError("Either from_ or to_ must be set")


@attrs.define(kw_only=True)
class ExistsQuery(FieldQuery):
    type: Literal["exists"] = attrs.field(default="exists", init=False)  # type: ignore[assignment]
    field: str = attrs.field()


@attrs.define(kw_only=True)
class SpecialQuery(Query):
    pass


@attrs.define(kw_only=True)
class NearQuery(SpecialQuery):
    type: Literal["near"] = attrs.field(default="near", init=False)  # type: ignore[assignment]
    queries: list[Query] = attrs.field()
    inOrder: Optional[bool] = attrs.field(default=None)
    slop: Optional[int] = attrs.field(default=None)


@attrs.define(kw_only=True)
class NestedQuery(SpecialQuery):
    type: Literal["nested"] = attrs.field(default="nested", init=False)  # type: ignore[assignment]
    field: str = attrs.field()
    query: Query = attrs.field()


@attrs.define(kw_only=True)
class LiteralNotQuery(SpecialQuery):
    type: Literal["literal_not"] = attrs.field(default="literal_not", init=False)  # type: ignore[assignment]
    value: str = attrs.field()
    fields: list[str] = attrs.field()
    matchQuery: Query = attrs.field()


@attrs.define
class KNNQuery:
    """
    Represents the 'knn' parameter in the search request for k-NN search.
    Creates a top level key named 'knn' instead of the normal 'query' key.
    Accepts a Query object in the filter_ parameter which limits the k-NN search.
    """

    k: int = attrs.field()
    field: str = attrs.field()
    vector: list[float] = attrs.field()
    filter_: Optional[Query] = attrs.field(default=None)

    def __attrs_post_init__(self):
        if self.k <= 0:
            raise ValueError("'k' must be a positive integer.")
        if not self.field:
            raise ValueError("'field' must be a non-empty string.")
        if not self.vector or not all(isinstance(x, float) for x in self.vector):
            raise ValueError("'vector' must be a non-empty list of floats.")
        if self.filter_ is not None and not isinstance(self.filter_, Query):
            raise ValueError("'filter_' must be a Query object.")

    @staticmethod
    def validate(val):
        from gilbert.services.ir import validate_knn_query

        return validate_knn_query(val)

    @staticmethod
    def serialize(val) -> dict | None:
        from gilbert.services.ir import serialize_knn_query

        return serialize_knn_query(val)
