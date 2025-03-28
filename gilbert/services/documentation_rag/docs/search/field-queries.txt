# Field Queries

This page list different queries that that enables content search and filtering.

* [Term](#term-query)
* [Terms](#terms-query)
* [Word](#word-query)
* [Words](#words-query)
* [Wildcard](#wildcard-query)
* [Range](#range-query)
* [Exists](#exists-query)




## Term Query

Matches an exact value in a field. Should be used to search in non-analyzed categorical fields, for example media type, source id and country code.

**Parameters**:

- **field**: The field to search in.
- **value**: The value to match exactly.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "term",
  "field": "metaData.mediaType",
  "value": "news"
}
```

## Terms Query

Matches any of the exact values in a field. Should be used to search in non-analyzed categorical fields, for example
media type, source id and country code.

**Parameters**:

- **field**: The field to search in.
- **values**: Any of the values to match exactly.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "terms",
  "field": "metaData.mediaType",
  "values": [
    "news",
    "md",
    "cm"
  ]
}
```

## Word Query

Matches words or phrases in a text field. Should be used to perform full text search in analyzed fields, for example
document title and body. The match is case-insensitive by default, which can be changed by setting the *flags* parameter
accordingly.

**Parameters**:

- **field**: The field to search in.
- **value**: The word to look for in the specified field.
- **minFreq**: The minimum number of occurrences of this word/phrase in this field. Allows filtering for documents where a word is mentioned at least *minFreq* times. Note that this setting has no effect when the query is used inside a Near query
- **maxFreq**: The maximum number of occurrences of this word/phrase in this field. Allows filtering for documents where a word is mentioned no more than *maxFreq* times. Note that this setting has no effect when the query is used inside a Near query
- **flags**: Optional property that is a list of flags. Currently, the only valid flag is EXACT_CASE. Applying this flag forces the search engine to be case sensitive when matching.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).


**Example**, Match for a single word in the document title and a phrase in the document title
```json
{
  "type": "word",
  "field": "body.title.text",
  "value": "meltwater"
},
{
  "type": "word",
  "field": "body.title.text",
  "value": "meltwater media monitoring"
}
```

## Words Query

Matches a list of words or phrases in a list of  text fields. Should be used to perform full text search in analyzed fields, for example
document title and body. The matching will always be with OR, meaning that it is enough to have a match of one of the values in one of the fields.
The match is case insensitive by default, which can be changed by setting the *flags* parameter
accordingly.

**Parameters**:

- **fields**: The fields to search in.
- **values**: The words to look for in the specified fields.
- **minFreq**: The minimum number of occurrences of this word/phrase in this field. Allows filtering for documents where a word is mentioned at least *minFreq* times. Note that this setting has no effect when the query is used inside a Near query
- **maxFreq**: The maximum number of occurrences of this word/phrase in this field. Allows filtering for documents where a word is mentioned no more than *maxFreq* times. Note that this setting has no effect when the query is used inside a Near query
- **flags**: Optional property that is a list of flags. Currently, the only valid flag is EXACT_CASE. Applying this flag forces the search engine to be case sensitive when matching.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).


**Example**, Match for a list of words in a list of fields
```json
{
  "type": "words",
  "fields": ["body.title.text", "body.ingress.text", "body.content.text"],
  "values": ["meltwater", "elasticsearch"]
}
```

## Wildcard Query

Matches words or phrases in an text field and allows expanding \* and ? wildcard characters. Should be used to perform full text search in analyzed fields, for example document title and body. The match is case insensitive by default, which can be changed by setting the *flags* parameter accordingly.

**CJK characters:** wildcards in a word in Japanese Katakana alphabet (which is used mainly for foreign words) work as usual, whereas wildcards with Kanji, Hiragana, Chinese and Korean characters are stripped off as individual characters are tokenized separately.

**Note:** the performance of *wildcard* queries are usually significantly less than *word* queries, as such *use them sparingly*.

**Parameters**:

- **field**: The field to search in.
- **value**: The word to look for in the specified field.
- **flags**: Optional property that is a list of flags. Currently, the only valid flag is EXACT_CASE. Applying this flag forces the search engine to be case sensitive when matching.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

**Example**
```json

{
  "type": "wildcard",
  "field": "body.title.text",
  "value": "meltwater?"
}

// Match for a phrase in the document title with an optional suffix, for example matching words "monitor", "monitors" and "monitoring".
{
  "type": "wildcard",
  "field": "body.title.text",
  "value": "meltwater media monitor*"
}

// Match Katakana text in the document title with an optional suffix, for example matching words "オリンピック" and "オリンピックオ".
{
  "type": "wildcard",
  "field": "body.title.text",
  "value": "オリンピック*"
}

// Useless wildcard to match CJK (non Katakana) text in the document title containing "天然水". This gives the same results as without the wildcard.
{
  "type": "wildcard",
  "field": "body.title.text",
  "value": "天然水*"
}
```

## Range Query

Matches values within a specified range in a numeric or date field. 

Date fields are stored in milliseconds since the start of 1970 and are always in UTC. This means that if your users expect dates to be split by their time zone, you need to convert that date into UTC. For convenience, dates can also be expressed in ISO8601 format, e.g. "2015-08-25T13:23:10.69Z" instead of 1440508990690. 

When performing date queries both upper and lower bounds must be specified. When performing range queries on other numeric fields you can optionally specify only one of the bounds.

**Parameters**:

- **field**: The field to filter on.
- **from**: The lower bound.
- **to**: The upper bound.
- **includeFrom** (default *true*): If the *from* value should be included in the range.
- **includeTo** (default *false*): If the 'to' value should be included in the range.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
// Restrict the time range of the query
{
  "type": "range",
  "field": "body.publishDate.date",
  "from": 1548248713000,
  "to": 1548853515000
}

// Find articles that've gone viral on Twitter
{
  "type": "range",
  "field": "metaData.socialScores.tw_shares",
  "from": 10000
}
```

## Exists Query

Matches when a document contains an indexed value for a field. That is, matches if the value is _not_ null and _not_ ´[]´.

**Parameters**:

- **field**: The field to search in.
- **boost** (default *1.0*): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "exists",
  "field": "metaData.applicationTags"
}
```
