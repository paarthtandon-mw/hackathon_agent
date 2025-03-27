# Search with User Tags

## How user tagging works

Customer have the ability to add tags to documents. Documents are usually tagged through the content stream. "User tags" are specific to the company (they should probably be called "company" tags), i.e. When a customer tags a document in the content stream, only users for that company will see the tag.

When a document is tagged, two things happen:

1. The document is copied to the companies private index, and a tag is written to `metaData.userTags` on the private copy of the document.

```json
"metaData": {
  "userTags": [ "My Sample Tag"]
}
```

2. An entry for the document ID and tag is stored in the "Document Modification" database. This entry also stores the matchSentence and keywords for the document, to keep context for the tag.
```json
{
  "documentMetadata": {
    "someDocumentID": [
      {
        "tagId": 123456,
        "tagName": "My Sample Tag",
        "matchSentence": "... said.\n\nThrough the Home for Good project, <em>Some Keyword</em> - and other members of the <em>another keyword</em> family - have donated ...",
        "keywords": [
          "Some Keyword",
          "another keyword"
        ]
      }
    ]
  }
}
```

## How User Tags are used in V2 Search

When returning documents with userTags from V2 Search/Export/etc. we include the matchSentence and keywords stored in the Document Modification Service if none are returned as part of search results. This depends on a few things:

### Keywords/Match Sentence already present

For each document returned in search results - the match Sentence and keywords are only overridden by those stored in the Document Modification Service _if they are not already present_. For most search requests keywords and matchSentence will be taken from [highlights](https://backstage.meltwater.io/docs/default/api/search-api-v1/results/highlighting/#highlighting) applied based on the search query. 

Common cases where there are no match sentence or keywords from highlights:

* searching by a specific tag 
```json
{
  "type": "term",
  "field": "metaData.userTags",
  "value": "My Sample Tag"
}
```
* searching by a specific document field
```json
{
  "type": "term",
  "field": "id",
  "value": "someDocumentID"
}
```

### User Tag Highlights

As mentioned in the previous section, the [highlights](https://backstage.meltwater.io/docs/default/api/search-api-v1/results/highlighting/#highlighting) determine the  match sentence and keywords for search results. User tags are usually included in `highlightOptions` to ensure tags are highlighted in the search results. It is important to disable keywords for these userTag highlights, or the tags will be added as keywords in the result instead of the keywords from the Document Modification Service.

The example of valid a highlight option for user tags is:

```json
{
  "highlightOptions": {
    // ..
    // other highlight options
    // ...
    "metaData.userTags": {
      "numberOfFragments": 1,
      "preTag": "<em>",
      "postTag": "</em>",
      "strictFragmentSize": false,
      "keywords": false
    }
  }
}
``` 
