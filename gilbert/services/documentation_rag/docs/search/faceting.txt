# Faceting

Faceting means breaking apart the matched documents into multiple *buckets*, and counting or applying child aggregations onto the documents that fall in each bucket. For example faceting over country code, and counting unique influencers from each country.

The faceting views will return the value that each bucket was created from, for example two buckets could be *us* or *se* when faceting over country codes.

When faceting over nested objects like sources, authors and named entities it may be desirable to return additional fields from the nested object. For example faceting over the source id, but also retrieve source name and URL. In these cases the [Top Hits](../results/retrieving-hits.md#top-hits) view will help retrieve these additional fields.

## Terms Facet

Bucket and count the top occurrences of distinct values in a specified field. Terms facets can accept a set of sub views which are applied on a per bucket basis. This can then be used to perform correlation requests, for example counting unique influencers or reach per country.

The buckets are sorted by the number of document occurrences by default, but can also be sorted by numeric sub views. At the moment, only certain **statistics** subviews are supported for sorting. Specifically, the fields used may not be a nested field, e. g. authors.

*Note:* These are approximate counts, the precision and exact value of the result may vary slightly between different queries and requests.

**Parameters**:

- **termsField**: The field to facet on.
- **size** (default *10*): The number of values to get counts for.
- **subViewRequests**: A mapping of strings to nested analytics aggregations. See [Sub view requests](#sub-view-requests) for which aggregations that can be used as sub view requests.
- **sortDirectives**: Sort the facets according to these directives. By default the facets will be sorted according to the count of documents that fall in each bucket. Currently only values from the *statistics* aggregation can be used for sorting. Sorting on values based on nested fields are currently not supported and is a [known issue](https://jira.meltwater.com/browse/IR-1545).
- **nestedPath**: If specified, evaluate the terms facet in a nested context. This can be used when working with sub views applied to nested documents. E.g. while faceting on authorInfo.handle, calculating statistics for twitter followers of authors can be done by specifying “metaData.authors” as the nestedPath and “twitterInfo.followers” as the field in a Statistics sub view request. The nestedPath parameter can be set either on the parent (Terms Facet) or sub (Statistics etc.) view request. Setting nestedPath to be an empty string “”, causes the facet to be evaluated in the root context. The use case for this is when multiple nested values match the search but the root document should only be counted once.
- **includeDocErrorUpperBound** (default *false*): If set to true the response will include upper bounds on the potentially missed documents in the approximate response. For more details, see the Elasticsearch documentation [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#terms-agg-doc-count-error).

```json
// Count documents for the top 10 countries
{
  "type": "termsFacet",
  "termsField": "metaData.source.location.countryCode",
  "size": 10
}

// Count unique influencers per top country
{
  "type": "termsFacet",
  "termsField": "metaData.source.location.countryCode",
  "size": 10,
  "subViewRequests": {
    "uniqueInfluencers": {
      "type": "cardinality",
      "field": "metaData.authors.authorInfo.externalId"
    }
  }
}

// Top publications by social echo
{
  "type": "termsFacet",
  "termsField": "metaData.source.id",
  "size": 10,
  "subViewRequests": {
    "socialEcho": {
      "type": "statistics",
      "field": "enrichments.socialScores.tw_shares",
      "measures": ["SUM"]
    },
    "sourceInfo": {
      "type": "topHits",
      "fields": ["metaData.source"]
    }
  },
  "sortDirectives": [
    {
      "sortBy": "socialEcho.statistics.SUM",
      "sortOrder": "DESC"
    }
  ]
}
```



## Significant Terms Facet

Bucket and count the most significant occurrences of distinct values in a specified field. Significance is characterized by values that stand out in search when compared to all documents in general. This enables a search to find values that are highly relevant and stand out for a particular search. In contrast the *termsFacet* will find values that are frequent in the search, but which may be equally frequent in all document in general.

Terms facets can accept a set of sub views which are applied on a per bucket basis. This can then be used to perform correlation requests.

The buckets are sorted by the number of document occurrences by default. 

*Note:* These are approximate counts, the precision and exact value of the result may vary slightly between different queries and requests.

**Parameters**:

- **termsField**: The field to facet on.
- **size** (default *10*): The number of values to get counts for.
- **subViewRequests**: A mapping of strings to nested analytics aggregations. See [Sub view requests](#sub-view-requests) for which aggregations that can be used as sub view requests.
- **nestedPath**: If specified, evaluate the significant terms facet in a nested context. This can be used when working with sub views applied to nested documents. E.g. while faceting on authorInfo.handle, calculating statistics for twitter followers of authors can be done by specifying “metaData.authors” as the nestedPath and “twitterInfo.followers” as the field in a Statistics sub view request. The nestedPath parameter can be set either on the parent (Significant Terms Facet) or sub (Statistics etc.) view request.

```json
// Find the most significant keyphrases for this search
{
  "type": "significantTerms",
  "termsField": "enrichments.keyPhrases.phrase",
  "size": 10
}

// Find the most significant hashtags for this search
{
  "type": "significantTerms",
  "termsField": "body.contentTags",
  "size": 10
}

// Find the most significant Kermit authors for this search
{
  "type": "significantTerms",
  "termsField": "metaData.authors.id",
  "size": 10
}

// Most significant publications for this search. This mostly makes sense for editorial news searches
{
  "type": "significantTerms",
  "termsField": "metaData.source.url",
  "size": 10
}

```



## Filter Facet

Use the filter view to further restrict and subdivide the documents that matched the main query, and selectively apply sub view requests on only the documents matching the filter. For example to categorize and classify documents at query time using a Boolean filter.

**Note**: For performance reasons the queries in filters are heavily restricted, eg how many wildcards are allowed. Also note that we don't support nested queries inside filters.  

**Parameters**:

- **query**: The filter to further restrict the main query. Uses the same query syntax as the main query.
- **subViewRequests**: A mapping of strings to nested analytics aggregations. See [Sub view requests](#sub-view-requests) for which aggregations that can be used as sub view requests.

```json
// Count the unique influencers in the search that are expressing the "happiness" emotion. Using a simple keyword classifier with words "happy", "joy" and "cheery"
{
  "type": "filter",
  "query": {
    "type": "any",
    "anyQueries": [
      {
      	"type": "word",
      	"field": "body.title.text",
      	"value": "happy"
      },
      {
      	"type": "word",
      	"field": "body.title.text",
      	"value": "joy"
      },
      {
      	"type": "word",
      	"field": "body.title.text",
      	"value": "cheery"
      }
    ]
  },
  "subViewRequests": {
    "uniqueInfluencers": {
      "type": "cardinality",
      "field": "metaData.authors.authorInfo.externalId"
    }
  }
}
```

## Sub view requests

Only some view requests can be sub view requests, these are:

- [Terms Facets](#terms-facet)
- [Date Histograms](histograms.md#date-histogram)
- [Percentile](statistics.md#percentiles)
- [Statistics](statistics.md)
- [Cardinality](statistics.md#cardinality)
- [TopHits](../results#top-hits)
