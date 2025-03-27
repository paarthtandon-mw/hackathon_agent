import asyncio
import copy
import logging
from typing import Any, AsyncContextManager, Callable
from urllib.parse import urljoin

import aiohttp

# Common client name used by all services
GLOBAL_CLIENT_HEADERS = {"X-Client-Name": "mw_copilot_chatbot"}
_DEFAULT_STATUS_FORCELIST = [429, 500, 502, 503, 504]
_DEFAULT_HEADER = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)


class AsyncRestApi:
    """
    A simple class to connect to a REST API with GET and POST methods asynchronously.

    HTTP connection are set up with basic retry and timeout parameters.
    The default numbers of retry is 3 with a backoff factor of 2.
    The default connect timeout is 2 seconds and read timeout is 10 seconds.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        auth: Any = None,
        headers: dict | None = None,
        max_retry: int = 3,
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=60),
        backoff_factor: int = 2,
        status_forcelist: list[int] | None = None,
    ):
        self.session = session
        self.url = url
        self.auth = auth
        self.headers = (
            headers if headers is not None else copy.deepcopy(_DEFAULT_HEADER)
        )
        self.status_forcelist = (
            status_forcelist
            if status_forcelist is not None
            else _DEFAULT_STATUS_FORCELIST
        )
        self.max_retry = max_retry
        self.backoff_factor = backoff_factor
        self.timeout = timeout

    def get_backoff_time(self, turn: int):
        # We want to consider only the last consecutive errors sequence (Ignore redirects).
        BACKOFF_MAX = 60
        if turn <= 1:
            return 0

        backoff_value = self.backoff_factor * (2 ** (turn - 1))
        return float(max(0, min(BACKOFF_MAX, backoff_value)))

    def _extract_error_message(self, response_data: Any) -> str:
        """Extract an error message from an error response"""

        if not response_data:
            return "No error message"

        if not isinstance(response_data, dict):
            return str(response_data)

        error_struct = response_data.get("error", {})
        if isinstance(error_struct, str):
            return error_struct
        elif isinstance(error_struct, dict):
            # in some APIs, we get a structure with an error reason back
            if (reason := error_struct.get("reason")) is not None:
                return reason
            else:
                return str(error_struct)
        return str(error_struct)

    async def _make_request(
        self,
        path: str | None,
        params: dict | None,
        additional_headers: dict | None,
        response_func: Callable[
            [str, dict, dict], AsyncContextManager[aiohttp.ClientResponse]
        ],
    ):
        """
        Generic wrapper for making an API request including path construction, retries,
        and error handling. Requires a function that returns the aiohttp response context.
        """
        headers = self.headers | (additional_headers or {})
        if params is None:
            params = {}

        url = self.url
        if path is not None:
            url = self.url if self.url.endswith("/") else self.url + "/"
            url = urljoin(url, path)

        for turn in range(0, self.max_retry + 1):
            retries_left = self.max_retry - turn
            return_directly = False
            error_reason = ""
            try:
                async with response_func(url, headers, params) as response:
                    status = response.status

                    if status in [200, 201]:
                        return await response.json()

                    # error status that cannot be retried
                    if status not in self.status_forcelist:
                        return_directly = True

                    # try to get an error reason
                    try:
                        response_data = await response.json()
                    except aiohttp.ContentTypeError as e:
                        response_data = str(e)
                        pass

                    error_reason = self._extract_error_message(response_data)
                    response.raise_for_status()

            except aiohttp.ClientError as exception:
                if isinstance(exception, aiohttp.SocketTimeoutError):
                    logger.warning("Get request to %s timed out: %s", url, exception)

                if isinstance(exception, aiohttp.ClientResponseError):
                    exception = aiohttp.ClientResponseError(
                        request_info=exception.request_info,
                        history=exception.history,
                        status=exception.status,
                        message=error_reason if error_reason else exception.message,
                        headers=exception.headers,
                    )

                if return_directly:
                    raise exception

                if not retries_left:
                    raise aiohttp.ClientError("Retries exhausted") from exception

            await asyncio.sleep(self.get_backoff_time(turn))

        assert False, "This should be unreachable"

    async def get(
        self,
        path: str | None = None,
        params: dict | None = None,
        additional_headers: dict | None = None,
    ) -> Any:
        """Send a GET request."""

        def _get_request(
            url: str, headers: dict, params: dict
        ) -> AsyncContextManager[aiohttp.ClientResponse]:
            return self.session.get(
                url,
                headers=headers,
                params=params,
                auth=self.auth,
                timeout=self.timeout,
            )

        return await self._make_request(path, params, additional_headers, _get_request)

    async def delete(
        self,
        path: str | None = None,
        params: dict | None = None,
        additional_headers: dict | None = None,
    ) -> Any:
        """Send a DELETE request."""

        def _delete_request(
            url: str, headers: dict, params: dict
        ) -> AsyncContextManager[aiohttp.ClientResponse]:
            return self.session.delete(
                url,
                headers=headers,
                params=params,
                auth=self.auth,
                timeout=self.timeout,
            )

        return await self._make_request(
            path, params, additional_headers, _delete_request
        )

    async def post(
        self,
        payload: dict | list,
        path: str | None = None,
        params: dict | None = None,
        additional_headers: dict | None = None,
    ) -> Any:
        """Send a POST request."""

        def _post_request(
            url: str, headers: dict, params: dict
        ) -> AsyncContextManager[aiohttp.ClientResponse]:
            return self.session.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                auth=self.auth,
                timeout=self.timeout,
            )

        return await self._make_request(path, params, additional_headers, _post_request)


class ConfiguredAsyncRestApi(AsyncRestApi):
    """Pre-configured timeout REST API (asynchronous version)."""

    # a single, global connection pool is recommended by aiohttp:
    # https://docs.aiohttp.org/en/stable/client_reference.html
    # If we connect to many different servers, we can also partition connections
    # into different pools here.
    _global_session_instance: aiohttp.ClientSession | None = None

    @classmethod
    def global_session(cls) -> aiohttp.ClientSession:
        """
        Get the global connection pool.
        This needs to be initialized lazily when already in an asyncio event loop.

        Notes:
            Since the `global_session` is cached `globally`, it requires async unit tests to run in the same loop
            (loop scope set to `session`) and do not close the loop in between.
            Otherwise, there will be the error `Event loop is closed`.
            If running in the same loop is not possible, the session object should be explicitly created and shared
            between tests.
        """
        # To create a new session when running tests, one can check for:
        # is_testing = 'pytest' in sys.modules
        # but this is inefficient.

        if cls._global_session_instance is None:
            cls._global_session_instance = aiohttp.ClientSession()

        return cls._global_session_instance

    def __init__(
        self,
        url: str,
        auth: Any = None,
        headers: dict | None = None,
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=60),
        **kwargs,
    ):
        headers = GLOBAL_CLIENT_HEADERS | (headers or {})
        if (session := kwargs.pop("session", None)) is None:
            session = self.global_session()

        super().__init__(
            session=session,
            url=url,
            auth=auth,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )
