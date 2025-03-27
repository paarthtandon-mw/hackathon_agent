# Special Queries

* [Near](#near-query)
* [Nested](#nested-query)
* [Literal Not](#literal-not)
* [Frequency](#frequency-query)


## Near Query

The *near* query matches when a set of nested queries match within a certain distance within the text of the field.

**Parameters**:

- **queries**: The nested queries which should be near each other.
- **inOrder** (default *false*): If the nested queries must appear in the specified order for the query to match.
- **slop** (default *4*): How many words or tokens that are allowed to appear between the specified queries.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](ref:search-sorting).

```json
{
  "type": "near",
  "queries": [
    {
      "type": "word",
      "field": "body.content.text",
      "value": "meltwater"
    },
    {
      "type": "word",
      "field": "body.content.text",
      "value": "social media"
    }
  ]
}
```

## Nested Query

The *nested* query searches inside nested objects. [Nested Objects](terminology#nested-object.md) are list of objects contained within the document, for example a list of authors or named entities. Without the nested query, an AND/OR query could match the entity name on one nested object, and match the entity type on another item in the list.

**Note:** the field names of the inner query are rooted at the nested object. For example the full field path *enrichments.namedEntities.name* would become a nested query on *enrichments.namedEntities* and an inner query for *name*.

**Parameters**:

- **field**: The field name for the array of nested objects.
- **query**: A query to match against each nested object.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "nested",
  "field": "enrichments.namedEntities",
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "term",
        "field": "name",
        "value": "Meltwater"
      },
      {
        "type": "term",
        "field": "type",
        "value": "organization"
      }
    ]
  }
}
```

## Literal Not

The *literal not* query is intended for excluding words with special characters and spaces that could otherwise not be excluded. The definition of special characters can be found [here](https://github.com/meltwater/elasticsearch-plugins/blob/main/custom-shingles-plugin/src/main/resources/special_characters.txt) 

In the normal case a query for ```&Brand``` and ```& Brand``` are the same thing since they are being tokenized to the same two tokens: ```[&,Brand]```

That means that its normally not possible to search for ```&Brand``` and exclude ```& Brand```, however, the literal not feature enables you to do this

Note: This feature does not work with exact case

**Parameters**:

- **value**: The excluded value that must not match.
- **fields**: The fields name where the value should be excluded
- **matchQuery**: The nested query that must match.

```json
{
  "value": "& Brand",
  "type": "literal_not",
  "fields": [
    "body.title.text",
    "body.content.text"
  ],
  "matchQuery": {
    "anyQueries": [
      {
        "value": "&Brand",
        "type": "word",
        "field": "body.title.text"
      },
      {
        "value": "&Brand",
        "type": "word",
        "field": "body.content.text"
      }
    ],
    "type": "any"
  }
}
```

**Note:** You can only do this for one special character at once. You can not use it to exclude ```& Brand-a-b-c``` since that contains more special characters

In that case you can still exclude ```& Brand``` and search for ```&Brand-a-b-c``` in the *matchQuery* as such:
```json
{
  "value": "& Brand",
  "type": "literal_not",
  "fields": [
    "body.title.text",
    "body.content.text"
  ],
  "matchQuery": {
    "anyQueries": [
      {
        "value": "&Brand-a-b-c",
        "type": "word",
        "field": "body.title.text"
      },
      {
        "value": "&Brand-a-b-c",
        "type": "word",
        "field": "body.content.text"
      }
    ],
    "type": "any"
  }
}
```



## Frequency Query

It's possible to require that words/phrases appearing a certain amount of times, see usage of the `minFreq`/`maxFreq` parameter in the [Word(s) query](../queries/field-queries.md#word-query).

If you require many words/phrases appear the same number of time, **Frequency Query** enables a simpler and more efficient syntax. It is also more performant in the backend systems.

Note: The sub queries in `frequencyQuery` are only allowed to be from the types `any`, `term`/`terms`, `near`, `word`/`words` (without minFreq/maxFreq set).

**Parameters**:

- **frequencyQuery**: A query (e.g. [Any Query](../queries/boolean-queries.md#any-query) with a list of words, or a [Near query](#near-query))
- **minFreq**: The _minimum_ number of occurrences any of the frequencyQuery's query should occur.
- **maxFreq**: The _maximum_ number of occurrences any of the frequencyQuery's query should occur.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

### Example 1
```json
 {
  "frequencyQuery": {
    "anyQueries": [
      {
        "field": "body.content.text",
        "type": "word",
        "value": "snake"
      }
    ],
    "type": "any"
  },
  "minFreq": 1,
  "maxFreq": 3,
  "type": "frequency"
}
```

### Example 2
```json 
{
    "frequencyQuery": {
      "fields": [
        "body.content.text"
      ],
      "values": [
        "Tree",
        "Saw",
        "Axe"
      ],
      "flags": [
        "EXACT_CASE"
      ],
      "type": "words"
    },
    "minFreq": 2,
    "type": "frequency"
  }
```

