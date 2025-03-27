# Getting Started

The Search API allows you to execute Boolean queries against all the Meltwater content and retrieve aggregated analytics and result lists. It's a low-latency synchronous API where you execute requests and receive analytics and matches.

To request acces to this API, please follow the instructions for [Creating a Content API Consumer](docs/default/domain/information-retrieval/api-access/consumers/), and specify `v2-search` as the API.

## Search API V2 Features

This API delivers legally compliant search content. It builds on the existing functionality of Search API V1, but with some augmentations to the request language.

It aims to replicate the full functionality of the Search API V1 but also provide some helpful enhancements to translate the media intelligence domain of companies and saved searches into runes queries and legally compliant results.

Already familiar with the [Search API V1](/docs/default/API/search-api-v1/)? Check our [Migrating from Search API V1](v2-search-migrating-from-v1.md) to see what's different in the Search API V2.

Some areas the Search API V2 can help are:

#### Small synchronous search queries

The Search API V2 works well for small amounts of data (ideally less than 1000 results). It is not designed of large result sets. The [Export API V2](/docs/default/API/export-api-v2) works well for exporting large amounts of search results. See the [Search Use Cases Guide](/docs/default/domain/information-retrieval/api_access/search-use-cases/) to help determine what the right API is for your use case.

#### Showing documents to an end-user

Documents that we show to an end-user have to undergo scrutiny to make sure they adhere to Meltwaters agreements with content providers. Some documents may need to be redacted due to geographical restrictions, others may need to be reported as viewed by an end-user. By default, all content returned by this API is legally compliant.

#### Media Intelligence enhancements

The Search API V2 provides some enhancements specific to the Media Intelligence domain. It supports [Saved Search Query Types](v2-saved-search-query-type.md), [Custom Category Query Types](v2-custom-category-query-type.md), [Keyword Query Types](v2-keyword-query-type.md), different [Document formats](v2-document-formats.md) and other enhancements such as paywall Urls in search results.

#### Reporting compliance

Meltwater has contractual agreements with many different content providers. For each content provider we have different requirements on reporting — for some we report each document consumed both for internal and external use, for others, we only report documents consumed by external users.

This API is fully compliant with Meltwater's reporting requirements, ensuring all documents consumed are reported to their corresponding content providers in a compliant manner.


## 1. The anatomy of search requests

A search request consists of a Boolean query and a number of different view requests to execute over the matched documents.

The search query parameter express the Boolean conditions that documents must match, for example the search terms to find. It must contain a time range filter that restricts the publish time of documents to match.

The view requests express one or more aggregations and result lists that should be calculated from the matched documents. View requests are typically a mix of multiple aggregations, nested aggregations and result lists.

**Parameters:**

- **query**: The filter to match documents against, see [Queries](/docs/default/API/search-api-v1/queries/) and [Fields](/docs/default/Component/mi-information-model/Dataset/search-fields/).
- **viewRequests**: The aggregations and result lists to calculate, see [Analytics](/docs/default/API/search-api-v1/analytics/statistics/) and [Results](/docs/default/API/search-api-v1/results/retrieving-hits/).
- **modifiers**: This contains attributes that are required to perform legal compliance restrictions and reporting e. g. `requestorCompanyId`. For details of all modifier parameters, take a look at the [Request Modifiers](v2-request-modifiers.md) page.
- **scope** (*optional*): Scope allows searching on specific document states, see [Scopes](/docs/default/API/search-api-v1/advanced-usage/overlays/#scopes).
- **metaData** (*optional*): Used to help identify requests. Search API V2 only accepts `metaData.savedSearchIds`, a list of search IDs that the search request is based upon


```json
// Searching for "meltwater" in the document title and executing 2 views
// - Counting total matches
// - Retrieving a sample of search results
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
    },
    "searchResults": {
      "type": "resultList",
      "start": 0,
      "size": 2,
      "fields": [
        "body.title.text",
        "body.publishDate.date",
        "metaData.url"
      ]
    }
  },
  "modifiers": {
    "requestorCompanyId": "59103b0662eb71f944d99b05",
    "requestorUserId": "59103b0762eb71f944d99b06",
    "productType": "swagger"
  },   
  "metaData": {
    "savedSearchIds": ["123456","7891011"]
  }
}
```



## 2. Formulating a Boolean query

Queries use something called the *Runes* query syntax, which takes the form of a tree of JSON objects with multiple nesting levels. It has a number of query constructs and allows expressing complicated Boolean logic.

The [Queries](/docs/default/API/search-api-v1/queries/) page contains a full specification of the Runes query types.

## 3. Analytics aggregations

There's many aggregations for different types of analytics, statistics, faceting and histograms. Many of the aggregations can be nested within each other, for example to calculate aggregate statistics for each day.

A single [Search API](/catalog/default/api/search-api-v2/definition#/default/v2-api-post-search) request would typically contain all the view requests that needs to be executed for the query. It's more cost effective to execute several aggregations in one go, compared to sending separate requests for each aggregation which is much more expensive.

The [Analytics](/docs/default/API/search-api-v1/analytics/statistics/) page contains a full specification of the available analytics aggregations.

For contractual reasons, aggregations from Search v2 do not include numbers from YouTube.

## 4. Result lists

Result lists retrieve a sample of matching documents from the query. There's support for many typical features like pagination, sorting, relevancy ranking, match sentence extraction, similarity clustering and de-duplication.

The [Results](/docs/default/API/search-api-v1/results/retrieving-hits/) page contains a full specification of the available result lists.

The [Response Consumer Attributes](v2-consumer-attributes.md) page contains details of the enhanced response data provided by the Search API V2.

## 5. Validation

All requests sent to the Search API are always validated, and if an error occurs you'll receive an [error code](/docs/default/API/search-api-v1/validation/error-codes/) in the response payload. You can also explicitly ask for a validation through the [/search/validate endpoint](/catalog/default/api/search-api-v2/definition#/default/v2-api-post-search-validate) and receive warnings and detailed explanations of potential problems. See [Validation](/docs/default/API/search-api-v1/validation/) for more details.

## 6. Search Load

Information about the cluster load generated by a search can be found in [Kibana](https://kibana-prod.meltwater.io/goto/83aaf6d4a0328ca70b662fa1f301e8b2)
Replace "123*"  with the trace_id that you want to trace.
**msg_totalEsProcessingTime**: the total time taken in CPU milliseconds of the search in the ES cluster
**msg_serviceTime**: the wall clock time of the search
**msg_totalHits**: the number of documents matched by the search

Some related dashboards:
[IR Cluster Load Breakdown](https://kibana-prod.meltwater.io/goto/c9640141d3c9045695a62da23834513e)
[Search Transparency](https://kibana-prod.meltwater.io/goto/066e614e1bb5aa04c391051729075dbd)

## 7. Troubleshooting

It's recommended to provide a **traceId** query param with a unique id identifying your request. That way, if you have a failing search request, error logs can be found in [Kibana](https://kibana-prod.meltwater.io/goto/9786f20a92c5913458d163dd82efba4e). Replace
"123*"  with the traceId.

## 8. Error Responses

Where possible, the Search API V2 passes on errors from upstream services and with an identifier helping consumers find the source of the problem.

Some sample error responses:

=== "JSON"
    ```json
        {
            "error": {
                "code": 404,
                "message": "Entitlements for company not found"
            },
            "errorSource": "NODE_ENTITLEMENT_API"
        }
    ``` 
=== "Search API V2 validation error"
    ```json
    {
        "error": {
            "code": 400,
            "message": "Both overlayGroups and requestorCompanyId cannot exist!",
            "errors": [
                {
                    "reason": "Both overlayGroups and requestorCompanyId cannot exist!",
                    "where": "searchRequest"
                }
            ]
        },
        "errorSource": "SEARCH_API_V2"
    }
    ```

The `errorSource` identifies the service returning the error. Some possible sources may be:

* `SEARCH_API` - an error may have occurred validating or executing the search query
* `NODE_COMPANY_API` - an error may have retrieving the company details for the ` "requestorCompanyId"`
* `NODE_ENTITLEMENT_API` - an error may have retrieving the entitlements for the ` "requestorCompanyId"`
* `SEARCH_API_V2` - an error may have processing the request or response
* `RESTRICTION_API` - an error may have occurred while applying legal restrictions to the search results
