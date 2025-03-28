# Keyword Query Type

The Search API V2 adds a new `keyword` rune query type.

A keyword can be included in the query by adding a query type `keyword` and the optional and desired values for `allKeywords`, `anyKeywords` or `notKeywords`.

```json
{
  "type": "keyword",
  "allKeywords": [
    "test"
  ],
  "anyKeywords": [
    "test2"
  ],
  "notKeywords": [
    "notTest"
  ]
}
```

The `keyword` query is substituted with the corresponding runes before executing the search query.

#### Example: Using a keyword query type

##### Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "keyword",
                "allKeywords": [
                    "bmw"
                ],
                "anyKeywords": [
                    "toyota"
                ],
                "notKeywords": [
                    "honda"
                ]
            },
            {
                "type": "range",
                "field": "body.publishDate.date",
                "from": "2020-01-23T23:00:00.000Z",
                "to": "2020-12-23T23:00:00.000Z"
            }
        ]
    },
    "viewRequests": {
        "documentCount": {
            "type": "count"
        },
        "list": {
            "type": "resultList",
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```
