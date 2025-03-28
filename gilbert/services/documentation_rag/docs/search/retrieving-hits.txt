# Retrieving Hits


## Result List

Use the result list view if you want to see a list of results, sorted by [lexical relevancy](sorting.md).

**Parameters**:

* **start** (default *0*): Used for pagination; the start parameter specifies the offset from the first hit to include in the response list. Max is 50k, but not recommended to go above 10k.
* **size** (default 10): Specifies how many hits to return. Max is 10k, but not recommended to go above 1k.
* **fields** (default *all fields*): Subset of document fields to retrieve. Please note that it's not possible to retrieve fields from [Nested Objects](docs/default/component/mi-information-model/Dataset/terminology/#nested-object.md).
* **highlightOptions**: Extract some document snippets that matched the query, see [Highlighting](highlighting.md) for more information.
* **nestedFieldOptions**: Request nested objects, such as the text associated with an embedding (only applicable for k-NN requests).

```json
// Simple result list with URL and title
{
  "type": "resultList",
  "fields": ["metaData.url", "body.title.text"]
}

// Result list with pagination and match snippets from the document body
{
  "type": "resultList",
  "size": 10,
  "start": 0,
  "fields": ["metaData.url", "body.title.text"],
  "highlightOptions": {
    "body.content.text": {
      "numberOfFragments": 3,
      "fragmentSize": 140,
      "preTag": "<em>",
      "postTag": "</em>"
    }
  }
}

// Result list with fields from nested objects
{
  "type": "resultList",
  "nestedFieldOptions": {
    "enrichments.embeddings.clippyV1.contentChunks": {
      "fields": ["enrichments.embeddings.clippyV1.contentChunks.text"],
      "size": 5
    }
  }
}
```

## Sorted Result List

The sorted result list view request is like a result list view request, but also allows the caller to specify a list of fields or scripts to sort on. Sorting directives are applied in order of declaration.

If the sort field is numeric, the sorting is done in the natural order. If the field is a date field, it is sorted according to the progression of time. If the field is a text field, the sorting is done according to the Unicode code point for each character, beginning with the first. This works well for English, since the alphabet in English has the same ordering as Unicode. Other languages have different rules for how to order letters, but the search API does not currently handle such rules.

**Parameters**:

* **start** (default *0*): Used for pagination; the start parameter specifies the offset from the first hit to include in the response list. Max is 50k, but not recommended to go above 10k.
* **size** (default 10): Specifies how many hits to return. Max is 10k, but not recommended to go above 1k.
* **fields** (default *all fields*): Subset of document fields to retrieve. Please note that it's not possible to retrieve fields from [Nested Objects](terminology#nested-object.md).
* **highlightOptions**: Extract some document snippets that matched the query, see [Highlighting](highlighting.md) for more information.
* **sortDirectives**: Sort the documents according to these directives, see [Sorting](sorting.md) for more information.
* **showSortValues** (default *false*): Return the field values and script results that were used when sorting each document. *Note:* This property is for debugging purposes only, the *sortValues* response format is subject to change without notice.

```json
// Result list sorted on publish time
{
  "type": "sortedResultList",
  "fields": ["metaData.url", "body.title.text"],
  "sortDirectives": [
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    } 
  ]
}
```



## Top Hits

Retrieve fields and documents associated with a bucketing aggregation. This allows retrieval of additional fields when faceting over a common attribute, for example to 

* Retrieving the source name and URL while faceting over the source id
* Retrieving the author name, image and profile URL while faceting over the author social handle

The documents that are returned are the top <size> documents based on how well they matched the query.

**Parameters**:

* **fields**: The fields to extract from the documents in the facet.
* **size** (default *1*): The number of results to return, must be between 1 and 10.
* **nestedPath**: By default, TopHits on nested fields are evaluated in the nested context. That is, the Top nested documents are returned. Setting nestedPath to be an empty string “”, causes the TopHits to be evaluated in the root context, which means the top full documents will be returned. 
* **sortDirectives**: Sort the documents according to these directives, see [Sorting](sorting.md) for more information. **Note**: If you specify sortDirectives then you must use nestedPath: "", as sorting is only supported on the root context of the document.

```json
// Fetching source information
{
  "type": "topHits",
  "fields": ["metaData.source"]
}

// Faceting over source id, and retriving additional source info
{
  "type": "termsFacet",
  "termsField": "metaData.source.id",
  "subViewRequests": {
    "sourceInfo": {
      "type": "topHits",
      "fields": ["metaData.source"]
    }
  }
}

// Sorting tophits
{
  "type": "topHits",
  "nestedPath": "",
  "sortDirectives": [
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    }
  ]
}
```

