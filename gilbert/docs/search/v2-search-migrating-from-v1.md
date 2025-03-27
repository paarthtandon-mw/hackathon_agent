# Migrating from Search API V1

This Search API V2 is a legally compliant version of the Search API with some extra enhancements built in.

# Built on top of the Search API Version 1

This API is a thin wrapper around the current [Search API V1](/docs/default/API/search-api-v1/). It supports the same request and response format that the Search API V1 provides. However, to add features such as regional content restrictions and paywall urls, we require some extra request parameters and return some extra response values, outlined below.

## Request format

The Search API V1 uses the following basic request format as outlined in the [Search API documentation](/docs/default/API/search-api-v1/#1-the-anatomy-of-search-requests). It accepts an object with the following parameters `query`, `viewRequests`, `restrictions`, `overlayGroups`, `scope`.

```json
{
   "query": {
     // searchQuery
   },
   "viewRequests": {
     // viewRequests
   },
   "restrictions": {
     // restriction data
   },
   "overlayGroups": [
     // overlay groups
   ],
   "scope": [
     // document states to search
   ],
   "metaData: {
     // request meta data for tracing
   }
}

```

This Search API V2 builds on the same API request format with some small changes, it accepts an object with the following parameters `query`, `viewRequests`, `scope`, `modifiers`.

```json
{
   "query": {
     // searchQuery as per Search API
   },
   "viewRequests": {
     // some viewRequests as per Search API
   },
   "scope": [
     // document states to search as per Search API
   ],
   "modifiers": {
     // extra parameters we use to modify the Search API request
   },
   "metaData: {
     // request meta data for tracing
   }
}

```

### Parameters that remain unchanged from the Search API

The following parameters are accepted and work the same way as with the Search API:

* **query**: The filter to match documents against, see [Queries](/docs/default/API/search-api-v1/queries/) and [Fields](/docs/default/Component/mi-information-model/dataset/fields/document).
* **viewRequests**: The aggregations and result lists to calculate, see [Analytics](/docs/default/API/search-api-v1/analytics/statistics/) and [Results](/docs/default/API/search-api-v1/results/retrieving-hits/).
* **scope** (*optional*): Scope allows searching on specific document states, see [Overlays](/docs/default/API/search-api-v1/advanced-usage/overlays/).
* **metaData** (*optional*): Used to help identify requests. Search API V2 only accepts `metaData.savedSearchIds`, a list of search ID that the search request is based upon. *Note, if you're using [Saved Search Query Types](/docs/default/api/search-api-v2/v2-saved-search-query-type) in your query, you do not need to set this field. We will populate it with the saved search IDs on your behalf.*

### Parameters are added in the Search API V2

The following parameter is required by this API to 'modify' the Search API request

* **modifiers**: This contains attributes that are required to perform legal compliance restrictions and reporting e. g. `requestorCompanyId`. For details of all modifier parameters, take a look at the [Request Modifiers](v2-request-modifiers.md) page.

### Parameters that are not needed with Search API V2

The following parameters are no longer necessary when using this API. By using the `modifiers.requestorCompanyId ` we automatically retrieve the necessary information and populate these values on your behalf when passing on your request to the Search API

* **restrictions**: by looking up the company country, we populate the value of restrictions accordingly. A `400` error response will be returned if the search request contains the `restrictions` parameter.
* **overlayGroups**: by looking up the companies' entitlements we populate the overlay groups to ensure you're searching private and premium content for that company. A `400` error response will be returned if the search request contains the `overlayGroups` parameter.

## Extra response values the Search API V2 provides

This API enriches documents with some extra attributes that are not available through the Search API. These attributes may be added as part of the legal compliance restriction process (e.g. `isSharingEnabled`) or they may be extra attributes added to help when displaying documents for consumers (e.g. `paywallUrl`).

These extra attributes will be included in a `consumerAttributes` object along with each quiddity result. More details of these fields can be found on the [Response Consumer Attributes](v2-consumer-attributes.md) page.

# What does sample request looks like?

Taking all of the above into account, here's a sample request to the Search API V2:

```json
{
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "word",
        "field": "body.title.text",
        "value": "platypus"
      },
      {
        "type": "range",
        "field": "body.publishDate.date",
        "from": "2020-08-11T20:13:30.000Z",
        "to": "2020-08-13T20:13:30.000Z"
      }
    ]
  },
  "viewRequests": {
    "searchResults": {
      "type": "resultList",
      "start": 0,
      "size": 1,
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

# What a sample response looks like?

Using the request above would produce the following result:

```json
{
    "views": {
        "searchResults": {
            "results": [
                {
                    "quiddity": {
                        "metaData": {
                            "url": "https://www.reddit.com/r/PrequelMemes/comments/i94iq3/a_platypus_ah_perry_the_platypus/",
                        },
                        "body": {
                            "publishDate": {
                                "date": 1597340674000
                            },
                            "title": {
                                "text": "A platypus ah Perry the platypus"
                            }
                        }
                    },
                    "highlights": {},
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
                        "geonames": {
                            "place": {
                                "id": 5128581,
                                "names": {
                                    "original": "New York City"
                                },
                                "type": "city",
                                "countryCode": "US",
                                "timezone": "America/New_York",
                                "latitude": 40.71427,
                                "longitude": -74.00597
                            }
                        }
                    }
                ]
                "type": "resultList"
            }
        }
    }
}
```

