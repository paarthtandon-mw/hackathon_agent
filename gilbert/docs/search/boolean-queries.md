# Boolean Queries


## All Query

The *all* query requires all of the nested queries to match. It can be thought of as the Boolean *AND* operator.
The *all* query represent an *AND* statement. It requires all the nested conditions to match. If **allQueries** is an empty list, no filter is applied, i.e., all documents match.

**Parameters**:

- **allQueries**: The nested queries which must all match.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

**Example**, find documents that mention a "meltwater" in the title, and within a certain time range
```json
{
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
      "from": 1548248713000,
      "to": 1548853515000
    }
  ]
}
```



## Any Query

The *any* query requires at least one of the nested queries to match. It can be thought of as the Boolean *OR* operator. If **anyQueries** is an empty list, no filter is applied, i.e., all documents match.

**Parameters**:

- **anyQueries**: The nested queries of which at least one must match.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

**Example**, find documents that mention a "meltwater" in the title, ingress or body
```json
{
  "type": "any",
  "anyQueries": [
    {
      "type": "word",
      "field": "body.title.text",
      "value": "meltwater"
    },
    {
      "type": "word",
      "field": "body.ingress.text",
      "value": "meltwater"
    },
    {
      "type": "word",
      "field": "body.content.text",
      "value": "meltwater"
    }
  ]
}
```



## Not Query

The *not* query has one nested query that needs to match, and another nested query that must not match. It can be thought of as a Boolean *AND NOT* operator.

**Note:** The reason why you can't make a 'not' query on its own is to prevent unbounded expensive searches.

**Parameters**:

- **matchQuery**: The nested query that must match.
- **notMatchQuery**: The nested query that must not match.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

**Example**, find documents that mention "meltwater", but exclude documents about glaciers
```json
{
  "type": "not",
  "matchQuery": {
    "type": "word",
    "field": "body.content.text",
    "value": "meltwater"
  },
  "notMatchQuery": {
    "type": "word",
    "field": "body.content.text",
    "value": "glacier"
  }
}
```
