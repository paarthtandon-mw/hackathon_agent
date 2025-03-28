__all__ = ["MAX_DATE_RANGE", "async_ir_client"]

import os

from gilbert.services.rest_api import ConfiguredAsyncRestApi

MAX_DATE_RANGE = 370
"""Max allowed date range in queries (days)"""


def async_ir_client(**kwargs):
    """
    Instantiate an IR API client.
    This does not establish a connection, it just pre-configures parameters.
    """

    return ConfiguredAsyncRestApi(
        url=os.environ["IR_API"],
        headers={
            "Content-Type": "application/json",
            "apikey": os.environ["IR_API_KEY"],
        },
        **kwargs,
    )
