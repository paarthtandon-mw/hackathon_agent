# Clustering


## Grouped Result List

Use the grouped result list view to retrieve and cluster results based on text similarity. The response consists of a list of groups, and each group consists of all the documents that fell within that group.

*Note that the groups are not deterministic, if you change the underlying result list by paginating the groups might change.*

**Basic algorithm:**

1. An underlying result list is retrieved based on *groupFrom*, *numToGroup* parameters, and sorted by [lexical relevancy](sorting.md).
2. The underlying result list is clustered into groups based on document similarity as defined by *similarityType*.
3. The *start* and *size* parameters determines which groups to return.

**Parameters**:

* **start** (default *0*): Used for paginating the groups; the start parameter specifies the offset from the first group to include in the response list.
* **size** (default 10): Specifies how many group to return.
* **fields** (default *all fields*): Subset of document fields to retrieve. Please note that it's not possible to retrieve fields from [Nested Objects](docs/default/component/mi-information-model/Dataset/terminology/#nested-object.md).
* **highlightOptions**: Extract some document snippets that matched the query, see [Highlighting](highlighting.md) for more information.
* **threshold** (default *0.0*): Similarity threshold that documents must exceed to be grouped together. The threshold value should be between 0.0 and 1.0, the higher the value the more similar the documents need to be.
* **groupFrom** (default *0*): The starting point for the underlying result list that is grouped as a post-processing step. It can be used in conjunction with numToGroup to page through the entire document set.
* **numToGroup** (default *1000*): The size of the underlying result list that is grouped as a post-processing step.
* **similarityType**: Specifies how to measure document similarity, see [Deduplicating](deduping.md) for more details.

**Example**, cluster on exact title match or 92% similarity of the body. The charikarLSH field calculated over `body.content.text as a document enrichment.
```json
{
  "type": "groupedResultList",
  "fields": ["metaData.url", "body.title.text"],
  "threshold": 0.92,
  "start": 0,
  "size": 10,
  "groupFrom": 0,
  "numToGroup": 1000,
  "similarityType": {
    "type": "max",
    "similarities": [
      {
        "field": "body.title.text",
        "type": "exact"
      },
      {
        "field": "enrichments.charikarLSH",
        "type": "charikarHamming"
      }
    ]
  }
}
```



## Sorted Grouped Result List

Use the sorted grouped result list view to retrieve and cluster results based on text similarity. Groups are sorted according to the sort directives. The response consists of a list of groups, and each group consists of all the documents that fell within that cluster.

**Basic algorithm:**

1. An underlying result list is retrieved based on *groupFrom*, *numToGroup* parameters, and sorted according to *baseSortDirectives*
2. The underlying result list is clustered into N groups based on document similarity as defined by *similarityType*.
3. The documents within each group is sorted according to optional *hitSortDirectives* (defaults to *baseSortDirectives* otherwise)
4. The groups are sorted based on *groupSortDirectives*, by comparing the first document in each group.
5. The *start* and *size* parameters determines which groups to return.

**Parameters**:

* **start** (default *0*): Used for pagination; the start parameter specifies the offset from the first cluster to include in the response list.
* **size** (default 10): Specifies how many clusters to return.
* **fields** (default *all fields*): Subset of document fields to retrieve. Please note that it's not possible to retrieve fields from [Nested Objects](docs/default/component/mi-information-model/Dataset/terminology/#nested-object.md).
* **highlightOptions**: Extract some document snippets that matched the query, see [Highlighting](highlighting.md) for more information.
* **threshold** (default *0.0*): Similarity threshold that documents must exceed to be grouped together. The threshold value should be between 0.0 and 1.0, the higher the value the more similar the documents need to be.
* **groupFrom** (default *0*): The starting point for the underlying result list that is clustered as a post-processing step. It can be used in conjunction with numToGroup to page through the entire document set. A request with groupFrom 50 and numToGroup 100 fetches results 50 to 99 (out of 0 to 99) and groups them among themselves.
* **numToGroup** (default *1000*): The size of the underlying result list that is clustered as a post-processing step.
* **similarityType**: Specifies how to measure document similarity, see [Deduplicating](deduping.md) for more details.
* **baseSortDirectives**: Sort directives for the underlying result list that is clustered as a post-processing step
* **hitSortDirectives**: Sort directives for documents within each group. If absent, defaulting to **baseSortDirectives**
* **groupSortDirectives**: Sort directives for the final list of groups, compared on the first document in each group. For most use cases this should be set to the same value as `baseSortDirectives`.
* **showSortValues** (default *false*): Return the field values and script results that were used when sorting each document. *Note:* This property is for debugging purposes only, the *sortValues* response format is subject to change without notice.

**Example**, cluster and sort according to publish date, picking the document with the most reach group from each group.
```json
{
  "type": "sortedGroupedResultList",
  "fields": ["metaData.url", "body.title.text"],
  "threshold": 0.92,
  "start": 0,
  "size": 10,
  "groupFrom": 0,
  "numToGroup": 1000,
  "similarityType": {
    "type": "max",
    "similarities": [
      {
        "field": "body.title.text",
        "type": "exact"
      },
      {
        "field": "enrichments.charikarLSH",
        "type": "charikarHamming"
      }
    ]
  },
  "baseSortDirectives": [
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    }
  ],
  "hitSortDirectives": [
    {
      "sortField": "enrichments.comscoreUniqueVisitors",
      "sortOrder": "DESC"
    }
  ],
  "groupSortDirectives": [
    {
      "sortField": "body.publishDate.date",
      "sortOrder": "DESC"
    }
  ]
}
```

