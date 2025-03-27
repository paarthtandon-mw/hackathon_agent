__all__ = ["Modifiers", "IrRequest"]

from typing import Optional

import attrs
import cattrs

from gilbert.services.ir import IrRequestConverter
from gilbert.services.ir.ir_queries import KNNQuery, Query
from gilbert.services.ir.ir_view_requests import ViewRequest
from gilbert.services.structurable import Structurable

converter = IrRequestConverter()


@attrs.define
class Modifiers:
    requestorCompanyId: str = attrs.field()
    productType: str = attrs.field()
    enableLegalRestrictions: bool = attrs.field(default=True)


@attrs.define
class IrRequest(Structurable):
    """IR search request."""

    viewRequests: dict[str, ViewRequest] = attrs.field()
    query: Optional[Query] = attrs.field(default=None)
    knn: Optional[KNNQuery] = attrs.field(default=None)
    modifiers: Optional[Modifiers] = attrs.field(default=None)

    def __attrs_post_init__(self):
        if self.query and self.knn:
            raise ValueError("'query' and 'knn' cannot both be provided.")
        if not (self.query or self.knn):
            raise ValueError("Either 'query' or 'knn' must be provided.")

    @classmethod
    def converter(cls) -> cattrs.Converter:
        return converter
