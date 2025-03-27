# Sorting

The *sortDirectives* parameter accepts a list of sort directives, each one containing a field name or script and sort order. The directives are applied in the same order they're declared. See the [Script DSL](../advanced-usage/script-dsl.md) for more information on script sorting.

Please note that when sorting on fields, you can only sort on fields that are non-nested. Sorting on the fields of [Nested Objects](docs/default/component/mi-information-model/Dataset/terminology/#nested-object.md) is not supported.

```json
// Result list sorted on reach and publish time
{
  "type": "sortedResultList",
  "fields": ["metaData.url", "body.title.text"],
  "sortDirectives": [
    {
      "sortField": "enrichments.comscoreUniqueVisitors",
      "sortOrder": "DESC"
    },
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    }
  ]
}

// Sorting on a simple relevance rank and publish time
{
  "type": "sortedResultList",
  "fields": ["metaData.url", "body.title.text"],
  "sortDirectives": [
    {
      "script": "_score * log(.enrichments.comscoreUniqueVisitors)",
      "sortOrder": "DESC"
    },
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    } 
  ]
}
```



## Lexical Relevance

Many queries support an optional *boost* parameter, which adjust how hits from that statement is scored compared to other queries. This is used when ordering by lexical relevancy (see the magic *_score* variable described in [Script DSL](../advanced-usage/script-dsl.md)).

```json
// Boost relevance for documents that mention meltwater in the title or ingress
{
  "type": "any",
  "anyQueries": [
    {
      "type": "word",
      "field": "body.title.text",
      "value": "meltwater",
      "boost": 10.0
    },
    {
      "type": "word",
      "field": "body.ingress.text",
      "value": "meltwater",
      "boost": 2.5
    },
    {
      "type": "word",
      "field": "body.content.text",
      "value": "meltwater"
    }
  ]
}
```

