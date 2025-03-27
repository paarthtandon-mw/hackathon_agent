# Validation

In order to protect our service there is a validation system in place for our API's. It validates the correctness and predicted resource usage of all queries before executing them, and enforces rate and credit limits per API consumer. 

There's no need to pre-validate requests for the search systems sake, but you may still want to do that to avoid the case where a single one of your users are allowed to exhaust your credit limit by submitting a very expensive search. For example you may want to only allow searches to be used in your application if they're well within your per-second credit limit. 

You can use the [/search/validate endpoint](/docs/default/API/search-api-v1/api-post-search-validate/) to validate and calculate the cost for a request without executing it. See [Rate Limits](search-limits.md) for a discussion on how to monitor your rate and credit limits.

## Validation Flow

The validation is done on several levels. In order to get processed by the backend, it must pass the below checks;

1. The HTTP request must have valid body and headers according to [the reference](api-post-search)
2. The JSON payload must contain a valid [rune](search-getting-started).
3. The query cannot be in a 'deny list', which may be the result of it being too resource intensive.
4. Rules & limits
4.1 The rune is validated against a set of rules, which define what searches are supported
4.2 The rune is validated against a set of limits on quantities derived from the rune itself, see [search request limits](/docs/default/API/search-api-v1/validation/request-rules-and-limits/#search-request-limits) 

