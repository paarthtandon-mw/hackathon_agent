# /search/sample
_**Note**: this endpoint is under development and may change without notice. Please share your use-case with Horace so we can make we capture what is important to you._ 

This endpoint yields **approximate but fast** search results. It is limited to a basic set aggregations (see below). Further, it may only be used for a limited date range.

The performance of this endpoint is estimated to be between 40-60 % faster than [/search](api-post-search.md), while only using a fifth (20 %) of the resource usage. It could be used when only approximate results are required, and when search times are important, e.g. when presenting a user with search results as they iterate on a Search Boolean.


## Request body
Like the `/search` endpoint, this accepts a JSON body with a query, view requests and other (optional) parameters.

See the [Getting Started](index.md) page for more information on how to express queries and view requests.

**Example**:
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
        "type": "word",
        "field": "body.title.text",
        "value": "acquired"
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
        "metaData.url"
      ]
    }
  }
}
```

## Supported aggregations 

* [Result List](./results/retrieving-hits.md#result-list)
* [Sorted Result List](./results/retrieving-hits.md#sorted-result-list)
* [Grouped Result List](./results/clustering.md#grouped-result-list)
* [Sorted Grouped Result List](./results/clustering.md#sorted-grouped-result-list)
* [TermsFacet](./analytics/faceting.md#terms-facet)
* [DateHistogram](./analytics/histograms.md#date-histogram)

