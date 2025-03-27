__all__ = [
    "SortDirective",
    "ViewRequest",
    "CountViewRequest",
    "CardinalityViewRequest",
    "StatisticsViewRequest",
    "TopHitsViewRequest",
    "TermsFacetViewRequest",
    "ResultListViewRequest",
    "SortedResultListViewRequest",
    "FilterFacetViewRequest",
    "DateHistogramViewRequest",
]

from abc import ABC
from typing import Literal, Optional

import attrs

from gilbert.services.ir.ir_queries import Query


@attrs.define
class SortDirective:
    """Sort directive for a view request in IR."""

    script: Optional[str] = attrs.field(default=None)
    scriptName: Optional[str] = attrs.field(default=None)
    sortField: Optional[str] = attrs.field(default=None)
    sortBy: Optional[str] = attrs.field(default=None)
    sortOrder: Literal["ASC", "DESC"] = attrs.field(default="ASC")

    def __attrs_post_init__(self):
        if (
            self.script is None
            and self.scriptName is None
            and self.sortField is None
            and self.sortBy is None
        ):
            raise ValueError(
                "At least one of these field must be set: script, scriptName, sortField, sortBy"
            )


@attrs.define
class ViewRequest(ABC):
    """Abstract class for a view request in IR."""

    type: Literal[""] = attrs.field()


@attrs.define
class TopHitsViewRequest(ViewRequest):
    type: Literal["topHits"] = attrs.field(default="topHits", init=False)  # type: ignore[assignment]
    fields: list[str] = attrs.field()
    nestedPath: Optional[str] = attrs.field(default=None)
    size: Optional[int] = attrs.field(default=1)
    sortDirectives: Optional[list[SortDirective]] = attrs.field(default=None)
    unredactedQuiddityFields: Optional[list[str]] = attrs.field(default=None)


@attrs.define
class CountViewRequest(ViewRequest):
    type: Literal["count"] = attrs.field(default="count", init=False)  # type: ignore[assignment]


@attrs.define
class CardinalityViewRequest(ViewRequest):
    type: Literal["cardinality"] = attrs.field(default="cardinality", init=False)  # type: ignore[assignment]
    field: str = attrs.field()


@attrs.define
class StatisticsViewRequest(ViewRequest):
    type: Literal["statistics"] = attrs.field(default="statistics", init=False)  # type: ignore[assignment]
    field: Optional[str] = attrs.field(default=None)
    script: Optional[str] = attrs.field(default=None)
    measures: Optional[list[str]] = attrs.field(default=None)


@attrs.define
class TermsFacetViewRequest(ViewRequest):
    type: Literal["termsFacet"] = attrs.field(default="termsFacet", init=False)  # type: ignore[assignment]
    termsField: str = attrs.field()
    size: int = attrs.field(default=10)
    subViewRequests: Optional[dict[str, ViewRequest]] = attrs.field(default=None)
    sortDirectives: Optional[list[SortDirective]] = attrs.field(default=None)


@attrs.define
class ResultListViewRequest(ViewRequest):
    type: Literal["resultList"] = attrs.field(default="resultList", init=False)  # type: ignore[assignment]
    start: int = attrs.field(default=0)
    size: Optional[int] = attrs.field(default=10)
    fields: Optional[list[str]] = attrs.field(default=None)
    unredactedQuiddityFields: Optional[list[str]] = attrs.field(
        default=None
    )  # allows retrieval of full body content


@attrs.define
class SortedResultListViewRequest(ResultListViewRequest):
    type: Literal["sortedResultList"] = attrs.field(
        default="sortedResultList", init=False
    )  # type: ignore[assignment]
    size: Optional[int] = attrs.field(default=None)
    fields: Optional[list[str]] = attrs.field(default=None)
    sortDirectives: Optional[list[SortDirective]] = attrs.field(default=None)
    showSortValues: bool = attrs.field(default=False)
    unredactedQuiddityFields: Optional[list[str]] = attrs.field(default=None)


@attrs.define
class FilterFacetViewRequest(ViewRequest):
    type: Literal["filter"] = attrs.field(default="filter", init=False)  # type: ignore
    query: Query = attrs.field()
    subViewRequests: dict[str, ViewRequest] = attrs.field()


@attrs.define
class DateHistogramViewRequest(ViewRequest):
    type: Literal["dateHistogram"] = attrs.field(default="dateHistogram", init=False)  # type: ignore
    dateField: str = attrs.field()
    timeZone: Optional[str] = attrs.field(default="UTC")
    granularity: Optional[
        Literal["SECOND", "MINUTE", "HOUR", "DAY", "WEEK", "MONTH"]
    ] = attrs.field(default=None)
    interval: Optional[int] = attrs.field(default=None)
    subViewRequests: Optional[dict[str, ViewRequest]] = attrs.field(default=None)
