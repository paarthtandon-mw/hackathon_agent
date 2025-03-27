# Error codes

The Search API may encounter errors while executing a request, either caused by internal issues or by a bad search request. An error response always contains a response-body with a description of the error(s).

```json
{
  "error": {
    "code": 400,
    "message": "Request validation failed",
    "errorCode": 1002,
    "errors": [
      {
        "reason": "Query date range (1166 days) exceeds the maximum 370 days allowed",
        "where": "query",
        "errorCode": 1002
      }
    ]
  }
}
```



## HTTP codes

- **4xx Client Error**
Catch all for client-side errors (details is given through errorCode and message)

- **500 Internal Server Error**
Catch all for server-side errors that are unknown.

- **503 Service Unavailable**
Triggered when the the maximum number of concurrent search requests have already been reached. Expected client behavior is to backoff and retry.

See also https://en.wikipedia.org/wiki/List_of_HTTP_status_codes.

## Detailed Error Codes



| Error code | HTTP status | Description                                                                                                                                                                                                                                                                                          |
|------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000       | 400         | Multiple errors were encountered in the same request.                                                                                                                                                                                                                                                |
| 1001       | 400         | Required parameter missing.                                                                                                                                                                                                                                                                          |
| 1002       | 400         | A provided parameter has an incorrect value.                                                                                                                                                                                                                                                         |
| 1004       | 400         | Unknown and unsupported parameter provided in the request.                                                                                                                                                                                                                                           |
| 1005       | 400         | An unknown field was used in the request. Known fields are the ones described in the schema for the specific tenant, for example [Fields](docs/default/component/mi-information-model/Dataset/search-fields/) documentation.                                                                         |
| 1006       | 400         | Triggered when a field has been used in an illegal way. Examples of this is requesting field statistics for a non-numeric field or performing a nested query on a non-nested field, see [Fields](docs/default/component/mi-information-model/Dataset/search-fields/) for an explanation.             |
| 2000       | 400/405     | An unknown request is received. Typically this is caused by an ill-formatted request (invalid json).                                                                                                                                                                                                 |
| 2001       | 400         | Request was invalidated because of performance issues, see [Validation](index.md) and [Rate Limits](request-rules-and-limits.md) for details.                                                                                                                                                        |
| 2002       | 400         | The consumer sending the request is not permitted to access the search API.
| 3000       | 500         | Service is disconnected                                                                                                                                                                                                                                                                              |
| 3001       | 500         | The request took too long to complete. Usually caused by the search backend being under too much stress at the moment.                                                                                                                                                                               |
| 3002       | 500         | The search backend is currently overloaded. The request has been rejected without making any attempt to execute it.                                                                                                                                                                                  |
| 9000       | 400/500/503 | An error of an unknown type occurred. Catch-all for unknown errors. Usually contains a description which can be used to track down the underlying problem. <br><br>If these errors are encountered then please to report them to @horace in the #horace channel and provide a sample of the request. |

