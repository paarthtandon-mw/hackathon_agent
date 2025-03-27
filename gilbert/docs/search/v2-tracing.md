# Trace Your Logs across V2 APIs

## Getting + Setting a `traceId`

We use a `traceId` field in our V2 APIs to help troubleshoot individual requests in the logs and to correlate logs across services.

### Setting your `traceId`

You can set a `traceId` on your requests as a request parameter, by adding a `traceId` query parameter.

Example:
https://mi.content.fairhair.ai/v2/search?traceId=my_unique_trace_id_1234

### No `traceId`? No problem!

If no `traceId` is supplied in the request, we will generate a unique `traceId` for you.

### Finding your `traceId`

Whether you supply your own `traceId` or you use the auto-generated `traceId`, it will be returned as a response header, named `platform-trace-id`.

![platform-trace-id.png](assets/platform-trace-id.png)

## Viewing Logs

### Using a `traceId` to view logs for your request

Once you have a `traceId` you can view all logs for that request (assuming the traceId is unique for a request) in [this Kibana dashboard](https://kibana-prod.meltwater.io/s/platypus/app/r/s/yHT2e). Pick the date range and search for `trace.id: "my-unique-trace-id-1234"`

E.g.: https://kibana-prod.meltwater.io/s/platypus/app/r/s/yHT2e
![kibana-trace-id-logs.png](assets/kibana-trace-id-logs.png)

### TRACE Logs 

For each HTTP Call, both internal API calls and the request itself, we include a `TRACE` (`log.level: "TRACE"`) request log message.

These logs are in message format:
`{statusCode} {statusMessage} {httpMethod} {url}`

An example:

![successful-response.png](assets/successful-response.png)
The `http` field of these log events contain additional information about the request, such as:
* `request duration`
* `Search-Credits-Consumed`
* `X-RateLimit-Credits`
* `X-Search-Memory-Allocated-Bytes`

![http-extra-info.png](assets/http-extra-info.png)
### Error logs

Error logs can be found by searching for `log.level: "ERROR" OR "WARN" OR http.status >= 400` in Kibana.

#### Error source

The `error.source` field denotes the source of the error. It can be helpful to identify the team responsible for the service that caused the error. 

| error.source                            | team          | details                                             |
|-----------------------------------------|---------------|-----------------------------------------------------|
| `ALERTING_API_V2`                       | Platypus      | Alerting API V2 error                               |
| `ALERTING_API`                          | Horace        | Alerting API V1 error                               |
| `BOOLEAN_QUERY_CONVERTER_API`           | Flamingo      | Error converting the boolean query                  |
| `CUSTOM_CATEGORY_API`                   | Flamingo      | Error fetching the custom category                  |
| `DOCUMENT_API_V2`                       | Platypus      | Document API V2 error                               |
| `DOCUMENT_API`                          | Horace        | Document API V1 error                               |
| `DOCUMENT_CATEGORIZER_API`              | Horace        | Resolving custom categories error                   |
| `DOCUMENT_MODIFICATION_API`             | Flamingo      | Fetching document modifications (user tags) error   |
| `DOCUMENT_TRANSFORMATION_RULES_API`     | Platypus      | Document Transformation Rules API error             |
| `EXPORT_API_V2`                         | Platypus      | Export API V2 error                                 |
| `EXPORT_API`                            | Horace        | Export API V1 error                                 |
| `GEONAMES_API`                          | Haven         | Resolving geo IDs error                             |
| `KEYWORD_QUERY_CONVERTER_API`           | Flamingo      | Error resolving keyword query                       |
| `KLEAR_API`                             | Klear         | Error calling Klear API                             |
| `LINKFLUENCE_API`                       | Linkfluence   | Error calling Linkfluence API                       |
| `NODE_COMPANY_API`                      | Carlito's Way | Error fetching company details                      |
| `NODE_ENTITLEMENT_API`                  | Carlito's Way | Error fetching entitlement details                  |
| `RAW_DOCUMENT_TRANSFORMATION_RULES_API` | Horace        | Internal Document Transformation Rules API error    |
| `RESTRICTION_API`                       | Platypus      | Error applying legal restrictions                   |
| `SAVED_SEARCH_API`                      | Flamingo      | Error resolving saved search query                  |
| `SEARCH_API_V2`                         | Platypus      | Search API V2 error                                 |
| `SEARCH_API`                            | Horace        | Search API V1 error                                 |
| `SUBSCRIPTION_CREDIT_API`               | Platypus      | Error fetching/decrementing premium content credits |
| `SUBSCRIPTION_SERVICE`                  | Platypus      | Alerting API V2 Subscription error                  |
| `UNKNOWN`                               | Platypus      | Unknown error source                                |
| `USER_IDENTITY`                         | Carlito's Way | Error fetching user details                         |

#### Request/Response payloads

When a request fails with a 5xx response code, we include the request and response object in the TRACE logs to help debug the failed request. Request payloads, when present will be logged to the `http.body` field.

## Debugging use-cases

Given the information above, how can you use it to debug issues with your requests?

### _My request failed with a `500` response code_

You're making a call to the Search API V2, but receive a `500` error response. 

1. Check your response headers to get the `platform-trace-id` for the request.
2. Use Kibana to search for logs with the `trace.id` matching `platform-trace-id` you found in the response headers.
3. Find the error in the upstream service logs
4. Check the `http.body` field in the logs to find the request and response bodies from that service.
5. Check the `error.source` to identify the team responsible for that service for further assistance.

### _My search query is failing_

The V2 APIs build on the existing functionality of Team Horace's V1 APIs but with some augmentations to the request language. Following some pre-processing, the request is passed to Team Horace's Search Service (Search API V1), where the query is executed. 

In the case of a failing search, the error response `errorSource` will have the value `"SEARCH_API"`, denoting that the error occurred in the Horace's Search Service (V1 API).

```json
{
    "error": {
        "code": 500,
        "message": "The search query failed"
    },
    "errorSource": "SEARCH_API"
}
```

In this scenario, you can use the `TRACE` logs to see the request and response logs made to Horace's V1 Search API:

![error-case.png](assets/error-case.png)
### _You receive 500 from V1 upstream API_

1) Search API V1 request: `http.body` field shows Search API V1 request body
2) Search API V1 response. `http.body` field shows Search API V1 response body
3) Search API V2 request. `http.body` field shows Search API V2 request body
4) Search API V2 response. `http.body` field shows Search API V2 response body

In case of an error caused by V1 APIs, it is recommended to contact team [**#horace**](https://meltwater.slack.com/archives/CABNB5AJY), the maintainers of the Search Service ES cluster. 

### _You want to debug the journey of a successful response_

**Example use case**: _I'm missing a document in my Newsletter, but it shows up in Explore_

Suppose a document is missing from a newsletter but appears in Explore. In that case, it may be because we apply some rules on the fly in the middleware that are not simple to find, causing different results in different components.

In this scenario, you can reach out to team [**#platypus**](https://meltwater.slack.com/archives/CAJKZ9RDE), and we can enable request/response body logging for that company's subsequent requests. This will allow you to locate the corresponding bodies in the `http.body` field, similar to the error case described above.
