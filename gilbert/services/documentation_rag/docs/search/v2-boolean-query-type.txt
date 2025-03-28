# Boolean Query type

The Search API V2 adds a new `boolean` query type.

A boolean can be included in the query by adding a boolean query type

```json
{
  "type": "boolean",
  "booleanQuery": "hello AND title:world",
  "caseSensitive": "no"
}
```
The `boolean` query is substituted with the corresponding runes before executing the search query.

#### Example: Using a boolean query type

##### Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "boolean",
                "booleanQuery": "\"Platypus\" AND \"wild\""
            },
            {
                "type": "range",
                "field": "body.publishDate.date",
                "from": "2023-12-01T23:00:00.000Z",
                "to": "2023-12-07T23:00:00.000Z"
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

##### Boolean query containing special characters

If your boolean query contains special characters such as quotes, you need to escape them as in the example provided below. For example, imagine you have created a tag called `"My Tag With Quotes"`.
If you want to execute a search for all documents tagged with this tag, the boolean query that you would use in the MI app looks like this

```text
metaData.userTags:"\"My Tag With Quotes\""
```

However, when sending this inside a search request, since the entire boolean query needs to be passed as a string, it gets surrounded with one more layer of quotes and therefore all the special characters enclosed in it, need to be escaped again.
This is what we expect the search request to look like

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "boolean",
                "booleanQuery": "metaData.userTags:\"\\\"My Tag With Quotes\\\"\""
            },
            {
                "type": "range",
                "field": "body.publishDate.date",
                "from": "2023-12-01T23:00:00.000Z",
                "to": "2023-12-07T23:00:00.000Z"
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

If you use a javascript client, `JSON.stringify()` should handle this for you. Sample code

```javascript
const booleanQueryValue = `metaData.userTags:"\"My Tag With Quotes\""`;

const jsonPayload = JSON.stringify({
    booleanQuery: booleanQueryValue
});

console.log(jsonPayload);
```