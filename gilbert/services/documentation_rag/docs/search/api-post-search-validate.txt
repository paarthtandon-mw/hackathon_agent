# /search/validate

The */validate* endpoint allows for validating the correctness of requests and calculate their credit usage, without executing them. This endpoints accepts the same payload and parameters as the [/search](api-post-search.md) endpoint, but will have a different response. 

*Note*: All these validations will also be enforced every time you use the  [/search](api-post-search.md) endpoint. So there's no need to pre-validate requests, unless you also want to further limit the complexity of searches used in your application in order to avoid a single user from exhausting your credit limit.

```json
{
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "word",
        "field": "body.title.text",
        "value": "meltwater"
      },
      {
        "type": "range",
        "field": "body.publishDate.date",
        "from": 1546300800000,
        "to": 1546905599999
      }
    ]
  },
  "viewRequests": {
    "documentCount": {
      "type": "count"
    }
  }
}
```



## Validation

Validation performs a number of checks on the search request, for example:

* Static syntax and parameter checking
* Complexity and execution cost analysis

## Validation Response
The validate response contains these fields:

* **status**: Validation status for this request, currently one of [*OK*, *WARNING*, *INVALID*], see [status codes](validation/error-codes.md#section-status-codes) below.
* **errors**: A list of the specific problems that was found in this request.
* **credits**: The number of API credits that would be consumed by this request.

### Status Codes
* An *OK* request would execute without problems
* A request with *WARNING* status would execute, but may have very bad response times and will use up a lot of search credits. Such requests should not be persistently used or saved, since the underlying constraints can change and they'd become *INVALID* and would then be completely blocked.
* A request with *INVALID* status would be blocked from executing.

**Examples**,
```json
// A request that doesn't produce any warnings
{
  "status": "OK",
  "credits": 87.0
}

// A request that produces warnings but will still execute. This request should not be used or saved, as it may be completely blocked at a later point without notice.
{
  "status": "WARNING",
  "credits": 151514.0,  
  "errors": [
    {
      "status": "WARNING",
      "message": "The view request will generate too many buckets"
    },
    {
      "status": "WARNING",
      "message": "The request is too resource intensive"
    }
  ]
}

// A request that will not execute because of query complexity constraints.
{
  "status": "INVALID",
  "credits": 564644.0,
  "errors": [
    {
      "status": "INVALID",
      "message": "Single character wildcards '?' are not allowed"
    }
  ]
}
```

