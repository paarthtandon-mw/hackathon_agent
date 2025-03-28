# Search API
The Search API allows you to execute Boolean queries against all the Meltwater content and retrieve aggregated analytics and result lists. 
It is a low-latency synchronous API where you execute requests and receive analytics and matches.

!!! warning "Note, before starting development, please refer to the [API guide](/docs/default/Domain/information-retrieval) to ensure you pick the right API for your particular use case.<br /> <br/>Different APIs have different limitations and constraints, and you'll need to ensure that your use case can be supported in a production setting while doing your software design. You can always and quickly get advice and architecture review from @horace in #horace, we're here to help!"


## Getting Started

The Search API allows you to execute Boolean queries against all the Meltwater content and retrieve aggregated analytics and result lists. It's a low-latency synchronous API where you execute requests and receive analytics and matches.


### 1. The anatomy of search requests

A search request consists of a Boolean query **or** a k-NN configuration, and a number of different view requests to execute over the matched documents.

The search query parameter express the Boolean conditions that documents must match, for example the search terms to find. It must contain a time range filter that restricts the publish time of documents to match.

The k-NN parameter controls how to do k-nearest neighbor search. It includes which embedding field to match, the query embedding itself and a Boolean query limiting the result set.

The view requests express one or more aggregations and result lists that should be calculated from the matched documents. View requests are typically a mix of multiple aggregations, nested aggregations and result lists.

**Parameters**:

- **query** (*required unless `knn` is set*): The filter to match documents against, see [Queries](queries/index.md) and [Fields](https://backstage.meltwater.io/docs/default/Component/mi-information-model/dataset/fields/document/).
- **knn** (*required unless `query` is set*): Configuration for k-nearest neighbor search.
- **viewRequests**: The aggregations and result lists to calculate, see e.g. [Analytics#Faceting](analytics/faceting.md) and [Results#Clustering](results/clustering.md).
- **overlayGroups** (*optional*): List of namespaces to include customer private documents and modifications from, see [Overlays](advanced-usage/overlays.md)
- **scope** (*optional*): Scope allows searching on specific document states, see [Overlays](advanced-usage/overlays.md).
- **restrictions** (*optional*): Restrictions is used to determine what results are legal to show to the requestor, see [Restrictions](validation/restrictions.md). If not specified, all results with any restriction will be omitted. **Note**: Not all kind of restrictions are applied via the search API.
- **metaData** (*optional*): MetaData is used for tracking information about the origin of a search request. Although optional, we highly recommend setting it to enable us to quickly identify the source of problematic requests. Partial metadata, e.g. only productType and companyId is also accepted.

Example: Searching for "meltwater" in the document title and executing 2 views (count total matches; and retrieve sample of search results)

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
  "restrictions": {
    "requestorCountry": "se"
  },
  "metaData": {
    "userId": "my-user",
    "companyId": "5e00abcd1234efgh5678",
    "savedSearchIds": [
      "123456",
      "7891011"
    ],
    "productType": "Explore"
  }
}
```

Example: k-nearest neighbor search (remember to replace `vector` with a float array of the correct length)

```json
{
  "knn": {
    "k": 10,
    "field": "enrichments.embeddings.clippyV1.contentChunks.vector",
    "vector": [0.1, 0.2, 0.3], // Replace this float array with a high-dimensional vector of the correct length.
    "filter": {
      "type": "all",
      "allQueries": [
        {
          "type": "term",
          "field": "metaData.provider.type",
          "value": "mw"
        },
        {
          "type": "range",
          "field": "body.publishDate.date",
          "from": 1729382400000,
          "to": 1729468800000
        }
      ]
    }
  },
  "viewRequests": {
    "hits": {
      "type": "resultList",
      "nestedFieldOptions": {
        "enrichments.embeddings.clippyV1.contentChunks": {
          "fields": ["enrichments.embeddings.clippyV1.contentChunks.text"],
          "size": 5
        }
      }
    }
  }
}
```

### 2. Formulating a Boolean query

Queries use something called the *Runes* query syntax, which takes the form of a tree of JSON objects with multiple nesting levels. It has a number of query constructs and allows expressing complicated Boolean logic.

The [Queries](queries/index.md) page contains a full specification of the Runes query types.

### 3. k-nearest neighbor search

In order to do k-NN search, the following parameters have to be provided as part of the `knn` section:

**Parameters**:

- **k**: The number of nearest neighbors to find.
- **field**: The document field containing an embedding.
- **vector**: The embedding for which you want to find documents with similar embeddings. The type is a float array, where the number of dimensions must align with the field. In order to generate a query vector/embedding, you need to use the same embedding model as when indexing. You should use [`clippy-api-embedding`](/catalog/default/api/linkfluence-clippy-api-embedding/definition) when querying `enrichments.embeddings.clippyV1.contentChunks.vector`.
- **filter**: A rune limiting the search space, see [Queries](queries/index.md) for more information.

Note 1: Support for k-NN search is currently experimental.

Note 2: The only view requests applicable to k-NN search are the result list and the sorted result list. See [Results#Retrieving Hits](results/retrieving-hits.md) for more information.

### 4. Analytics aggregations

There's many aggregations for different types of analytics, statistics, faceting and histograms. Many of the aggregations can be nested within each other, for example to calculate aggregate statistics for each day.

A single [Search API](api-post-search.md) request would typically contain all the view requests that needs to be executed for the query. It's more cost effective to execute several aggregations in one go, compared to sending separate requests for each aggregation which is much more expensive.

The [Analytics](analytics/index.md) page contains a full specification of the available analytics aggregations.

### 5. Result lists
Result lists retrieve a sample of matching documents from the query. There's support for many typical features like pagination, sorting, relevancy ranking, match sentence extraction, similarity clustering and de-duplication.

The [Results](results/index.md) page contains a full specification of the available result lists.

### 6. Validation

All requests sent to the Search API are always validated, and if an error occurs you'll receive an [error code](validation/error-codes.md) in the response payload. You can also explicitly ask for a validation through the [/search/validate endpoint](api-post-search-validate.md) and receive warnings and detailed explanations of potential problems. See [Validation](validation/index.md) for more details.

### 7. Search Load

Information about the cluster load generated by a search can be found in [Kibana](https://kibana-prod.meltwater.io/goto/83aaf6d4a0328ca70b662fa1f301e8b2)
Replace "123*"  with the trace_id that you want to trace.
**msg_totalEsProcessingTime**: the total time taken in CPU milliseconds of the search in the ES cluster
**msg_serviceTime**: the wall clock time of the search
**msg_totalHits**: the number of documents matched by the search

Some related dashboards:
[IR Cluster Load Breakdown](https://kibana-prod.meltwater.io/goto/c9640141d3c9045695a62da23834513e)
[Search Transparency](https://kibana-prod.meltwater.io/goto/066e614e1bb5aa04c391051729075dbd)

### 8. Troubleshooting

It's recommended to provide a **traceId** query param with a unique id identifying your request. That way, if you have a failing search request, error logs can be found at https://kibana-prod.meltwater.io/goto/9786f20a92c5913458d163dd82efba4e. Replace
"123*"  with the traceId.

