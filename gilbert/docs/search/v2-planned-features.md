# Planned & Beta Features

These features are in the early development stage for the Search API V2. If anything here seems useful to you, please let us know either through [our Slack channel](https://meltwater.slack.com/archives/CAJKZ9RDE), or [by sending us an email](mailto:platypus@meltwater.com).

## Author Enrichments (Beta)

The Search API V2 (and Export API V2) now has Klear and Linkfluence author enrichments as an experimental feature. It can be enabled by setting the parameter `modifiers.enableAuthorEnrichments` to `true` and is applied to twitter results only.

To use this feature you'll also need to ensure that the view request fields includes `"metaData.authors"` and `"metaData.source.socialOriginType"`.

When enabled, any twitter documents returned in a `resultList` will contain two new attributes in the per-document `consumerAttributes`.

* `klearAuthors` will contain the author profile from Klear. An empty list will be returned if no information is found
* `linkfluenceAuthors` will contain the author profile from Linkfluence. An empty list will be returned if no information is found

This is currently an experimental feature which **we do not advise using in a customer facing product in its current format**. We're providing the enrichments to help see what twitter author information is available from these integrations and how it might be used.

**Note: **The response format *will* change and the `klearAuthors` and `linkfluenceAuthors` will be consolidated into a single authors object once a final schema has been agreed.

```json
{
    "resultList": {
        "results": [
            {
                "quiddity": {...},
                "highlights": {...},
                "consumerAttributes": {
                    "embedUrl": "https://emded-url-paywall.com/redirect",
                    "paywallUrl": "https://paywall-url.com/redirect",
                    "matchSentence": "this is a match sentence",
                    "disableInAppOpening": true,
                    "isInternalSharingDisabled": false,
                    "isSharingDisabled": false,
                    "isTranslateDisabled": true,
                    "originalUrl": "https://example.com",
                    "redirectUrl": "https://example.com",
                    "restrictionHistory": [],
                    "tagContextMatchSentence": "this is tag context match sentence",
                    "klearAuthors": [
                        {
                            "name": "Security Testing",
                            "skills": {
                                "Security": 57
                            },
                            "influenceScore": "71.09",
                            "youtubeChannelId": null,
                            "klearId": 154652563,
                            "locationCountry": "India",
                            "blogUrl": null,
                            "followersCount": 36490,
                            "networks": {
                                "hasBlog": false,
                                "hasTiktok": false,
                                "hasTwitch": false,
                                "hasTwitter": true,
                                "hasYoutube": false,
                                "hasFacebook": false,
                                "hasInstagram": false
                            },
                            "profileImageUrl": "http://pbs.twimg.com/profile_images/710735123876982784/GjV7JWMk_normal.jpg",
                            "followersHighlights": {
                                "avgAge": 31.65199999999999,
                                "topCountry": {
                                    "countryCode": "US",
                                    "countryName": "United States",
                                    "countryPercentage": 39.8
                                },
                                "gendersPercentage": {
                                    "male": 73,
                                    "female": 27
                                }
                            }
                        }
                    ],
                    "linkfluenceAuthors": [
                        {
                            "id": 130225,
                            "occupation": [],
                            "gender": "F",
                            "scores": {
                                "resonance": 5,
                                "audience": 61,
                                "totalFollowers": 240,
                                "followersByPlatforms": {
                                    "twitter": 240,
                                    "instagram": 0,
                                    "sinaweibo": 0,
                                    "youtube": 0,
                                    "twitch": 0
                                }
                            },
                            "hasChildren": true,
                            "favourites-count": 4309,
                            "inRelationship": null,
                            "listed-count": 2,
                            "description": "testt",
                            "screenName": "test",
                            "platform": "twitter",
                            "uid": "r3_prod-tw-123",
                            "statuses-count": 1842,
                            "followers-count": 240,
                            "email": null,
                            "idStr": "130225",
                            "verified": false,
                            "followings-count": 234,
                            "tags": [],
                            "followers": 240,
                            "name": "44:44",
                            "reconcilations": [
                                "twitter_1302253"
                            ],
                            "timeline": {
                                "ngrams": [],
                                "scoredStatusesTerms": "",
                                "entities": {},
                                "entitiesList": [
                                    "test"
                                ],
                                "scoredEntitiesList": [],
                                "scoredEntities": "",
                                "scoredCategories": "entertainment.video-games|1",
                                "scoredContentClassifications": "",
                                "scoredContentClassificationsList": [],
                                "categories": {
                                    "entertainment.video-games": 1
                                },
                                "categoriesList": [
                                    "entertainment.video-games"
                                ],
                                "contentClassifications": {},
                                "contentClassificationsList": [],
                                "hashtags": {},
                                "hashtagsList": [],
                                "scoredHashtagsList": [],
                                "scoredHashtags": "",
                                "mentions": [
                                    "xxx",
                                ],
                                "scoredMentions": "xxx"
                            },
                            "permalink": "https://twitter.com/testt"
                        }
                    ]
                }
            ]
        }
    }
}
```



## Query Tag Matching (Beta)

The Search API V2 (and Export API V2) now includes the ability to match each document against a partial runes queries. Specific parts of runes queries can be annotated with a `queryTag` object to identify, and optionally match documents against that part of the query.

**What are QueryTags for?**

Query tags were primarily built to support Explore custom categories, but can be used to define some structure to the runes query. For example, when an explore saved search is converted into runes, the resulting query is one large JSON object, with no way to determine what part of the query was for explore filters, custom categories or the base query itself. `queryTags` can be used to annotate the different parts of the runes query to help consumers of runes queries to resolve the query into it's different parts.

**How does "matching" work?**

When `includeMatch` is set to `true`, the Search/Export V2 API will post-process documents in result lists, to determine what queryTags they matched with. This can be helpful to know why the document was included in the result list. For example, if a user creates an explore search with three custom categories, the documents in the result list will include the queryTag for the custom category they are associated with.

**`queryTag` schema**

Query tags have the following fields:

* **id (required):** an identifier for the query tag
* **type (required):** the type of query tag. E.g 'customCategory'
* **includeMatch (required):** Defaults to `false`. A boolean value that determines whether result list documents will be "matched" against the queryTag.
* **additionalAttributes (optional):** A JSON object that will be included with any documents that match the queryTag.

***(`id`, `type`) constraint***

The tuple (`id` and `type`) is expected to uniquely correspond to one sub-query. If a query tag occurs at several places
in the request, the Search API v2 assumes that their sub-queries are identical.

**Example**

Here's a sample request for the word `platypus`, but with a custom category queryTag for `car`:

```json
{
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "word",
        "field": "body.title.text",
        "value": "tesla"
      },
      {
        "type": "range",
        "field": "body.publishDate.date",
        "from": "2020-08-11T20:13:30.000Z",
        "to": "2020-08-13T20:13:30.000Z"
      },
      {
        "type": "any",
        "anyQueries": [
          {
            "value": "car",
            "field": "body.title.text",
            "type": "word"
          },
          {
            "value": "car",
            "field": "body.ingress.text",
            "type": "word"
          },
          {
            "value": "car",
            "field": "body.content.text",
            "type": "word"
          },
          {
            "value": "car",
            "field": "body.contentTags",
            "type": "term"
          }
        ],
        "queryTag": {
          "type": "customCategory",
          "id": "1073",
          "includeMatch": true,
          "additionalAttributes": {
            "name": "car"
          }
        }
      }
    ]
  },
  "viewRequests": {
    "searchResults": {
      "type": "resultList",
      "start": 0,
      "size": 10,
      "fields": [
        "body.title.text",
        "body.publishDate.date",
        "metaData.url"
      ]
    }
  },
  "modifiers": {
    "requestorCompanyId": "59103b0662eb71f944d99b05",
    "requestorUserId": "59103b0762eb71f944d99b06",
    "productType": "swagger"
  }
}

```


And here's what the `resultList` the response might look like. The `matchQueryTag` attributes will be a list of the query tags that the document matched:


```json
{
    "resultList": {
        "results": [
            {
                "quiddity": {
                  "id": "someDocumentId"
                },
                "highlights": {...},
                "consumerAttributes": {
                    "embedUrl": "https://emded-url-paywall.com/redirect",
                    "paywallUrl": "https://paywall-url.com/redirect",
                    "matchSentence": "this is a match sentence",
                    "disableInAppOpening": true,
                    "isInternalSharingDisabled": false,
                    "isSharingDisabled": false,
                    "isTranslateDisabled": true,
                    "originalUrl": "https://example.com",
                    "redirectUrl": "https://example.com",
                    "restrictionHistory": [],
                    "tagContextMatchSentence": "this is tag context match sentence",
                    "matchQueryTags": [{
                      "type": "customCategory",
                      "id": "1073",
                      "additionalAttributes": {
                         "name": "car"
                      }
                    }]
                }
            ]
        }
    }
}
```
If you're using consuming [Gyda formatted documents](/docs/default/API/search-api-v2/v2-document-formats/#gyda-documents-from-the-search-api-v2), the `matchQueryTag` attributes will be included in the gyda document. 
```json
{
    "resultList": {
        "results": [
            {
                "gyda": {
                    "documentId": "someDocumentId",
                    "date": "2021-01-17T23:00:00.000Z",
                    "sourceId": 12345,
                    "matchQueryTags": [{
                      "type": "customCategory",
                      "id": "1073",
                      "additionalAttributes": {
                         "name": "car"
                      }
                    }]
                    // ... and more
                },
                "highlights": {...},
                "consumerAttributes": { ... }
            ]
        }
    }
}
```

## Vector Search

In the V2 Search API, users can utilize vector search functionality which builds upon the k-nearest neighbors (kNN) search features available in V1. Similar to regular query requests, users can access legally compliant search content along with the various enhancements offered by V2.

### Knn Request using Vector

To construct a V2 kNN request, please provide modifiers (in the same way you would for regular searches) on top of [V1 kNN request](/docs/default/api/search-api-v1/#3-k-nearest-neighbor-search). For detailed information on all modifier parameters, refer to the [Request Modifiers](v2-request-modifiers.md) page. 

When retrieving results, only the `resultList` is supported, and you can check [this page](/docs/default/api/search-api-v1/results/retrieving-hits/#result-list) for the specific fields you can request.

Example request:

``` json
{
  "knn": {
    "k": 10,
    "field": "enrichments.embeddings.clippyV1.contentChunks.vector",
    "vector": [0.1, 0.2, 0.3], 
    "filter": {
      "type": "all",
      "allQueries": [
        {
          "type": "term",
          "field": "metaData.provider.type",
          "value": "mw"
        },
        {
          "type": "range",
          "field": "body.publishDate.date",
          "from": 1729382400000,
          "to": 1729468800000
        }
      ]
    }
  },
  "modifiers": {
    "productType": "swagger",
    "requestorCompanyId": "59103b0662eb71f944d99b05",
    "requestorUserId": "59103b0762eb71f944d99b06"
  },
  "viewRequests": {
    "hits": {
      "type": "resultList"
    }
  }
}
``` 

### kNN Request using query string 

Search V2 can translate a query string into vector. This enables you to pass a text field (which we will the convert to a vector) instead of a vector array as part of the knn query. Instead of manually providing a vector array, you can simply set the `text` field, and Search V2 will automatically populate the vector array for you.

Example request:

``` json
{
    "knn": {
      "k": 3,
      "text": "Did Microsoft make a good deal when investing in OpenAI?",
      "field": "enrichments.embeddings.clippyV1.contentChunks.vector",
      "filter": {
        "allQueries": [
          {
            "field": "body.content.text",
            "type": "word",
            "value": "microsoft"
          }
        ],
        "type": "all"
      }
    }
...
}
``` 

## Sample Search
The Search API V2 now supports Sample search. The new `/search/sample` endpoint is a wrapper around the `/search/sample` [endpoint of Search API V1](/docs/default/api/search-api-v1/api-post-search-sample). This endpoint is designed for fetching fast, but approximate search results. It consumes significantly (40%-60%) fewer resources on Horace's side.
Because of this, there are some limitations on the search criteria. These limits are controlled by the V1 API. The request and response formats for this endpoint are identical to that of the `/search` endpoint. For more information, please read the linked documentation of V1 API above.


## Explore+ Search

This feature allows clients to perform searches in Explore+, with queries and view requests similar to `/v2/search`
by calling the end-point `/v2/search/explore-plus`.

See Example Request below for an example of how a request can look. Responses are identical to `/v2/search` responses.

**N.B.** Due to being in active development, this end-point is currently only available to white-listed product
types. If you would like to use it, reach out in the [#platypus slack channel](https://meltwater.slack.com/archives/CAJKZ9RDE), or [by sending us an email](mailto:platypus@meltwater.com).

### Differences from `/v2/search`

Result grouping is not, and will likely not be, supported in Explore+ searches.

### Current limitations

These features are currently not supported in Explore+ searches.

#### Modifiers

The feature toggles in the `modifiers` object currently do not have any effect in this API. The values actually
in use are the ones seen in the example request below.

Currently, only the Gyda document format is supported.

#### consumerAttributes

The `consumerAttributes` object in the response search hits is mostly empty. For now, rely on the values in
the gyda document instead.

#### No aggregations

Currently only document count and result list (but not grouped result list) view requests are supported.

### Example request

```json
{
  "modifiers": {
    "requestorCompanyId": "581c4c674582c828ac7ab902",
    "requestorUserId": "581c4c674582c828ac7ab903",
    "productType": "digest",
    "documentFormat": "GYDA",
    "enableLegalRestrictions": true,
    "enablePaywall": true,
    "enableMWTransitionTokens": false,
    "enableAuthorEnrichments": false,
    "enableGeonames": true
  },
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "explorePlusSavedSearches",
        "ids": [5643]
      },
      {
        "field": "body.publishDate.date",
        "from": "2024-12-01T00:15:15.000Z",
        "to": "2024-12-01T01:15:15.000Z",
        "type": "range"
      }
    ]
  },
  "viewRequests": {
    "count": {
      "type": "count"
    },
    "searchResults": {
      "type": "resultList",
      "size": 10,
      "start": 0
    }
  }
}
```
