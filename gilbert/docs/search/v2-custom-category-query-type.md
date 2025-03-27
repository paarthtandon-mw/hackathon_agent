# Custom Category Query Type

The Search API V2 adds a new `customCategory` rune query type.

A custom category can be included in the query by including a query type `customCategory` and the `customCategoryId`.

```json
{
    "type": "customCategory",
    "customCategoryId" : 12345
}
```
Before the search query is executed, this `customCategory` query is replaced by the runes for the custom category in question.

*Note: the company specified by the `modifiers.requestorCompanyId` must have access to the `custom category` specified or a `404` response will be returned.*

Below are a some examples on how you can build queries using custom categories.

#### Example: Using the customCategory query type

##### Request

```json
{
    "query": {
      "type": "all",
      "allQueries": [
        {
          "type": "any",
          "anyQueries": [
            {
              "type": "customCategory",
              "customCategoryId": 123456
            },
            {
              "type": "customCategory",
              "customCategoryId": 654321
            }
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

### Case sensitivity

The Custom Category query has two fields that can be used to control case sensitivity: `caseSensitive`, and `caseSensitivityFromSearchId`. These fields are mutually exclusive; you can provide either of them, or none, but not both.

`caseSensitivityFromSearchId` means that the custom category will be parsed with whatever case sensitivity that referenced saved search uses.

#### Snippet: Using explicit case sensitivity

```json
{
  "type": "customCategory",
  "customCategoryId": 2691,
  "caseSensitive": "yes"
}
```


#### Snippet: Using case sensitivity from saved search

```json
{
  "type": "customCategory",
  "customCategoryId": 2691,
  "caseSensitivityFromSearchId": 2410812
}
```
