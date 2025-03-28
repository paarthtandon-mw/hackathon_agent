# /search

See the [Getting Started](index.md) page for information on how to express queries and view requests.

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

