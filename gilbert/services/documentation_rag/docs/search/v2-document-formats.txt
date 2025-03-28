# Document formats

The Search API V2, Export API V2, Alerting API V2 and Consumer Ready Document API all support returning documents in both `quiddity` and `gyda` formats.

## Background

The search service returns documents in the [General Schema](/docs/default/Component/mi-information-model/dataset/fields/) format, also known as Quiddities. Many user-facing and legacy apps use Gyda formatted documents, a simplified, flattened document format. This is the document format that [Keystone](https://github.com/meltwater/keystone) (`/documentService/v3`) returns.

To convert documents from General Schema format to Gyda format, the [document-converter](https://github.com/meltwater/document-converter) is used. With the release of the Search API V2, the document-converter has been updated to include the `consumerAttributes` additions returned by the Search API V2 when converting from General Schema (Quiddity) documents into Gyda documents.

### Quiddity Document Schema

This is the General Schema format as stored in Elasticsearch. This is the default format returned.

### Gyda Document Schema

The mapping from General Schema format to Gyda format is not entirely straight forward. The mapping can differ based on the document information type and media type. For example, editorial documents may have some fields that social documents do not have, facebook documents are not mapped the same way as reddit documents.

To complicate matters further, some fields in the Gyda document format are not mapped from the General Schema format, but are added as part of the legal restriction process, such as `isSharingDisabled`, which implies whether or not a document is allowed to be share for a particular company.

We've put together a of all Gyda document fields, and where the values are mapped from. It may not cover all fields and mappings but should deal with the most important fields.
[Gyda Document Schema](https://docs.google.com/spreadsheets/d/1DqgsemS8LvzbA2YSdlCTC2J_xHULXGLepg_kEGQNQMc/edit?usp=sharing)

## Gyda documents from the Search API V2

By default, Search API V2 returns documents as Quiddities. However, the API accepts a `modifiers.documentFormat` parameter. By explicitly setting `modifiers.documentFormat: "gyda"`, any documents returned in a `resultList` in the search response will be in Gyda format.

**Here's what a sample request would look like:**

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "savedSearch",
                "searchId" : 12345
            },
            {
                "field": "body.publishDate.date",
                "from": "2020-06-16T20:13:30.00Z",
                "to": "2020-06-20T20:13:30.00Z",
                "type": "range"
            }
        ]
    },
    "viewRequests": {
        "documentCount": {
            "type": "count"
        },
        "list": {
            "type": "resultList",
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger",
        "documentFormat": "gyda"
    }
}
```

**This request would result in the following response:**

```json
{
    "views": {
        "documentCount": {
            "totalCount": 1254,
            "type": "count"
        },
        "resultList": {
            "results": [
                {
                    "highlights": {
                        "body.contentTags": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.content.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.ingress.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.mentions": {
                            "keywords": [],
                            "fragments": []
                        },
                        "enrichments.sentences.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.title.text": {
                            "keywords": [
                                "trees"
                            ],
                            "fragments": [
                                "A forester planted a few larch <em>trees</em> in Douglas fir forest in Oregon to create a smiley face"
                            ]
                        }
                    },
                    "gyda": {
                        "documentId": "1610924400000_6tP5Sbt_yi1y4CLfKw0bJQ9hJ6I",
                        "date": "2021-01-17T23:00:00.000Z",
                        "sourceId": null,
                        "embedUrl": null,
                        "sourceUrlTransitionToken": null,
                        "country": "us",
                        "redirectUrl": null,
                        "keyPhrases": [
                            "few larch trees",
                            "forester",
                            "piece of wood",
                            "smiley face"
                        ],
                        "keywords": [],
                        "reach": null,
                        "historyEvents": null,
                        "language": "en",
                        "source": "reddit.com",
                        "body": "Time enough now for a piece of wood",
                        "sourceUrl": "https://www.reddit.com/",
                        "hostedContent": null,
                        "urlTransitionToken": null,
                        "links": null,
                        "applicationTags": [],
                        "images": [],
                        "isSentimentModified": null,
                        "disableInAppOpening": false,
                        "isTranslateDisabled": false,
                        "mediaType": "social_message_boards",
                        "informationType": "social",
                        "tags": [],
                        "paywallUrl": null,
                        "ingress": null,
                        "originalSentiment": null,
                        "providerSpecific": null,
                        "tagContextMatchSentence": null,
                        "disambiguatedSourceId": null,
                        "restriction": "NOT_RESTRICTED",
                        "region": "Undef",
                        "authors": [
                            {
                                "id": null,
                                "url": null,
                                "authorInfo": {
                                    "rawName": "Bosswarrior53"
                                },
                                "avatarUrl": null,
                                "name": "Bosswarrior53",
                                "handle": null,
                                "authority": null,
                                "bio": null
                            }
                        ],
                        "sentiment": "N",
                        "matchSentence": null,
                        "socialScores": null,
                        "title": "A forester planted a few larch trees in Douglas fir forest in Oregon to create a smiley face",
                        "potentialReach": null,
                        "charikarLSH": "KGU0vGZk8AUPtChiUBNIiHZMmRX4lfFRZkdiTaVtfkKDGhKJ6hd6UCy6IiUJgKKE",
                        "provider": "omgili",
                        "client": null,
                        "place": null,
                        "restrictionHistory": null,
                        "fetchingTime": null,
                        "adm2": null,
                        "isHosted": false,
                        "matchTags": [],
                        "providerSpecifier": "social_fetcher",
                        "adm1": null,
                        "originalUrl": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns1h5",
                        "url": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns1h5",
                        "isInternalSharingDisabled": false,
                        "isSocialSharingDisabled": false,
                        "isSharingDisabled": false
                    },
                    "consumerAttributes": {
                        "paywallUrl": null,
                        "embedUrl": null,
                        "matchSentence": "A forester planted a few larch <em>trees</em> in Douglas fir forest in Oregon to create a smiley face",
                        "disableInAppOpening": false,
                        "isInternalSharingDisabled": false,
                        "isSharingDisabled": false,
                        "isSummarizationDisabled": true,
                        "isSocialSharingDisabled": false,
                        "isTranslateDisabled": false,
                        "originalUrl": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns1h5",
                        "redirectUrl": null,
                        "restriction": "NOT_RESTRICTED",
                        "restrictionHistory": null,
                        "tagContextMatchSentence": null,
                        "urlTransitionToken": null,
                        "sourceUrlTransitionToken": null,
                        "keywords": []
                    }
                },
                {
                    "highlights": {
                        "body.contentTags": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.content.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.ingress.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.mentions": {
                            "keywords": [],
                            "fragments": []
                        },
                        "enrichments.sentences.text": {
                            "keywords": [],
                            "fragments": []
                        },
                        "body.title.text": {
                            "keywords": [
                                "trees"
                            ],
                            "fragments": [
                                "A forester planted a few larch <em>trees</em> in Douglas fir forest in Oregon to create a smiley face"
                            ]
                        }
                    },
                    "gyda": {
                        "documentId": "1610924400000_M_B5lVmUPMWl5EsJpaIw_o_Be1I",
                        "date": "2021-01-17T23:00:00.000Z",
                        "sourceId": null,
                        "embedUrl": null,
                        "sourceUrlTransitionToken": null,
                        "country": "us",
                        "redirectUrl": null,
                        "keyPhrases": [
                            "few larch trees",
                            "forester",
                            "smiley face"
                        ],
                        "keywords": [],
                        "reach": null,
                        "historyEvents": null,
                        "language": "en",
                        "source": "reddit.com",
                        "body": "I saw that I love it",
                        "sourceUrl": "https://www.reddit.com/",
                        "hostedContent": null,
                        "urlTransitionToken": null,
                        "links": null,
                        "applicationTags": [],
                        "images": [],
                        "isSentimentModified": null,
                        "disableInAppOpening": false,
                        "isTranslateDisabled": false,
                        "mediaType": "social_message_boards",
                        "informationType": "social",
                        "tags": [],
                        "paywallUrl": null,
                        "ingress": null,
                        "originalSentiment": null,
                        "providerSpecific": null,
                        "tagContextMatchSentence": null,
                        "disambiguatedSourceId": null,
                        "restriction": "NOT_RESTRICTED",
                        "region": "Undef",
                        "authors": [
                            {
                                "id": null,
                                "url": null,
                                "authorInfo": {
                                    "rawName": "Scoot240"
                                },
                                "avatarUrl": null,
                                "name": "Scoot240",
                                "handle": null,
                                "authority": null,
                                "bio": null
                            }
                        ],
                        "sentiment": "N",
                        "matchSentence": null,
                        "socialScores": null,
                        "title": "A forester planted a few larch trees in Douglas fir forest in Oregon to create a smiley face",
                        "potentialReach": null,
                        "charikarLSH": "OGU0PFRm8NQvoCAy0BEMj0RArxSo3XfBZlFibYVvXsGGCDJMQhZiQIy6AiUvoKCE",
                        "provider": "omgili",
                        "client": null,
                        "place": null,
                        "restrictionHistory": null,
                        "fetchingTime": null,
                        "adm2": null,
                        "isHosted": false,
                        "matchTags": [],
                        "providerSpecifier": "social_fetcher",
                        "adm1": null,
                        "originalUrl": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns08f",
                        "url": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns08f",
                        "isInternalSharingDisabled": false,
                        "isSocialSharingDisabled": false,
                        "isSharingDisabled": false
                    },
                    "consumerAttributes": {
                        "paywallUrl": null,
                        "embedUrl": null,
                        "matchSentence": "A forester planted a few larch <em>trees</em> in Douglas fir forest in Oregon to create a smiley face",
                        "disableInAppOpening": false,
                        "isInternalSharingDisabled": false,
                        "isSharingDisabled": false,
                        "isSummarizationDisabled": true,
                        "isSocialSharingDisabled": false,
                        "isTranslateDisabled": false,
                        "originalUrl": "https://www.reddit.com/r/pics/comments/kzdmrt/a_forester_planted_a_few_larch_trees_in_the/?sort=new#thing_t1_gjns08f",
                        "redirectUrl": null,
                        "restriction": "NOT_RESTRICTED",
                        "restrictionHistory": null,
                        "tagContextMatchSentence": null,
                        "urlTransitionToken": null,
                        "sourceUrlTransitionToken": null,
                        "keywords": []
                    }
                }
            ],
            "type": "resultList"
        }
    }
}
```

## Fields

The Search API V2 currently does not support returning specific fields for `gyda` documents. If the consumer requests documents in `gyda` format, this API will return documents with a default set of fields that the document converter currently has a mapping for.

If you request for specific fields when requesting the format to be gyda, the API throws the following validation error. In such cases, please remove the `fields` array from any viewRequests present in your search request.


```json
{
    "error": {
        "code": 400,
        "message": "requesting specific fields when modifiers.documentFormat is gyda, is not supported.",
        "errors": [
            {
                "reason": "requesting specific fields when modifiers.documentFormat is gyda, is not supported.",
                "where": "searchRequest"
            }
        ]
    },
    "errorSource": "SEARCH_API_V2"
}
```

