__all__ = [
    "IrRequestConverter",
    "validate_query",
    "serialize_query",
    "validate_knn_query",
    "serialize_knn_query",
]

from typing import Any

import attrs
import cattrs
from cattrs import gen, strategies

from gilbert.services.ir.ir_queries import KNNQuery, Query
from gilbert.services.ir.ir_view_requests import ViewRequest


def _bypass_reserved_keyword(s: str) -> str:
    if s.endswith("_"):
        return s[:-1]
    else:
        return s


class IrRequestConverter(cattrs.Converter):
    """Converter for IrRequest.

    * Attributes with default values are omitted when serialization.
    * Support bypassing reserved keywords by using attributes ending with an underscore.
    """

    def __init__(self):
        super().__init__()

        # Global hooks
        def unstructure_hook(cls):
            return gen.make_dict_unstructure_fn(
                cls,
                self,
                _cattrs_omit_if_default=True,
                **{
                    a.name: cattrs.override(rename=_bypass_reserved_keyword(a.name))
                    for a in attrs.fields(cls)
                },
            )

        def structure_hook(cls):
            return gen.make_dict_structure_fn(
                cls,
                self,
                _cattrs_omit_if_default=True,
                **{
                    a.name: cattrs.override(rename=_bypass_reserved_keyword(a.name))
                    for a in attrs.fields(cls)
                },
            )

        self.register_unstructure_hook_factory(attrs.has, unstructure_hook)
        self.register_structure_hook_factory(attrs.has, structure_hook)

        # Allow union bool | int | str
        strategies.configure_union_passthrough(bool | int | str, self)

        # The following lines override the previously set (global) hooks for three classes Query, ViewRequest, and KNNQuery.
        # That's why we need to define the overrides again (e.g., _cattrs_omit_if_default).
        strategies.include_subclasses(
            Query,
            self,
            overrides={
                "_cattrs_omit_if_default": True,
                "_cattrs_include_init_false": True,
                "type": cattrs.override(omit_if_default=False),
                "from_": cattrs.override(rename="from"),
                "to_": cattrs.override(rename="to"),
            },
        )
        strategies.include_subclasses(
            ViewRequest,
            self,
            overrides={
                "_cattrs_omit_if_default": True,
                "_cattrs_include_init_false": True,
                "type": cattrs.override(omit_if_default=False),
            },
        )
        strategies.include_subclasses(
            KNNQuery,
            self,
            overrides={
                "_cattrs_omit_if_default": True,
                "_cattrs_include_init_false": True,
                "filter_": cattrs.override(rename="filter"),
            },
        )


_query_validator = IrRequestConverter()


def serialize_query(query: Query | None) -> dict | None:
    """Serialize (unstructure) a query into a dict."""
    if query is None:
        return None

    return _query_validator.unstructure(query)


def validate_query(raw: Any) -> Query:
    """Validate and / or construct a query from an unstructured object."""
    if isinstance(raw, Query):
        return raw

    if not isinstance(raw, dict):
        raise ValueError("Cannot deserialize a query from non-dict")

    try:
        return _query_validator.structure(raw, Query)
    except cattrs.BaseValidationError as e:
        raise ValueError("Invalid query") from e


def serialize_knn_query(knn_query: KNNQuery | None) -> dict | None:
    """Serialize (unstructure) a KNNQuery into a dict."""
    if knn_query is None:
        return None
    return _query_validator.unstructure(knn_query)


def validate_knn_query(raw: Any) -> KNNQuery:
    """Validate and / or construct a KNNQuery from an unstructured object."""
    if isinstance(raw, KNNQuery):
        return raw
    if not isinstance(raw, dict):
        raise ValueError("Cannot deserialize a KNNQuery from non-dict")
    try:
        return _query_validator.structure(raw, KNNQuery)
    except cattrs.BaseValidationError as e:
        raise ValueError("Invalid KNNQuery") from e
