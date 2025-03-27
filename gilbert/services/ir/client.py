__all__ = ["MAX_DATE_RANGE", "async_client"]

import os

from gilbert.services.rest_api import ConfiguredAsyncRestApi

MAX_DATE_RANGE = 370
"""Max allowed date range in queries (days)"""


def async_client(**kwargs):
    """
    Instantiate an IR API client.
    This does not establish a connection, it just pre-configures parameters.
    """
    os.environ()

    return ConfiguredAsyncRestApi(
        url=os.getenv("IR_API"),
        headers={"Content-Type": "application/json", "apikey": os.getenv("IR_API_KEY")},
        **kwargs,
    )
