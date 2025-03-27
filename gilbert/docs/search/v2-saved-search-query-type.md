# Saved Search Query Type

## Saved search query type

The Search API V2 adds a new `savedSearch` rune query type. This enables queries to be built using MI [Saved Searches](/docs/default/API/masfsearch-v3). It works with both regular and explore searches.

A saved search can be included in the query by add including a query type `savedSearch` and the `searchId`.

```json
{
    "type": "savedSearch",
    "searchId" : 12345
}
```
Before the search query is executed, this `savedSearch` query is replaced by the runes for the saved search in question.

*Note: the company specified by the `modifiers.requestorCompanyId` must have access to the `searchId` specified or a `404` response will be returned.*

Below are a some examples on how you can build queries using saved searches.

### Examples

#### Example 1: Using the savedSearch query type

This example illustrates using a saved search to select content within a date range.

##### Request

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
                "from": "2020-06-16T20:13:30.000Z",
                "to": "2020-06-20T20:13:30.000Z",
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
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```

#### Example 2: Narrowing a search to only twitter results

This example illustrates using a saved search to select content, a date range, and a query that narrows the search to only Twitter content.

##### Request

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
                "type": "all",
                "allQueries": [
                    {
                      "field": "metaData.source.socialOriginType",
                      "value": "twitter",
                      "type": "term"
                    },
                    {
                      "anyQueries": [
                        {
                          "field": "metaData.provider.type",
                          "value": "gnip",
                          "type": "term"
                        },
                        {
                          "field": "metaData.provider.type",
                          "value": "spinn3r",
                          "type": "term"
                        },
                        {
                          "field": "metaData.provider.type",
                          "value": "twitter",
                          "type": "term"
                        }
                      ],
                      "type": "any"
                    }
                ]
            },
            {
                "field": "body.publishDate.date",
                "from": "2020-06-16T20:13:30.000Z",
                "to": "2020-06-20T20:13:30.000Z",
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
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```

#### Example 2: Finding tweets that match either of two saved searches

This example illustrates combining multiple saved searches, a date range, and a query that narrows the search to only Twitter content.

The user wants documents that match either of the saved searches with ids 1001 and 1002.

##### Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "any",
                "anyQueries": [
                    {
                        "type": "savedSearch",
                        "searchId": 1001
                    },
                    {
                        "type": "savedSearch",
                        "searchId": 1002
                    }
                ]
            },
            {
                "type": "all",
                "allQueries": [
                    {
                        "field": "metaData.source.socialOriginType",
                        "value": "twitter",
                        "type": "term"
                    },
                    {
                        "anyQueries": [
                            {
                                "field": "metaData.provider.type",
                                "value": "gnip",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "spinn3r",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "twitter",
                                "type": "term"
                            }
                        ],
                        "type": "any"
                    }
                ]
            },
            {
                "field": "body.publishDate.date",
                "from": "2020-06-16T20:13:30.000Z",
                "to": "2020-06-20T20:13:30.000Z",
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
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```

#### Example 3: Finding tweets that match two saved searches

This example illustrates combining multiple saved searches, a date range, and a query that narrows the search to only Twitter content.

The user wants documents that match the saved searches with ids 1001 **and** 1002.

##### Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "all",
                "allQueries": [
                    {
                        "type": "savedSearch",
                        "searchId": 1001
                    },
                    {
                        "type": "savedSearch",
                        "searchId": 1002
                    }
                ]
            },
            {
                "type": "all",
                "allQueries": [
                    {
                        "field": "metaData.source.socialOriginType",
                        "value": "twitter",
                        "type": "term"
                    },
                    {
                        "anyQueries": [
                            {
                                "field": "metaData.provider.type",
                                "value": "gnip",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "spinn3r",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "twitter",
                                "type": "term"
                            }
                        ],
                        "type": "any"
                    }
                ]
            },
            {
                "field": "body.publishDate.date",
                "from": "2020-06-16T20:13:30.000Z",
                "to": "2020-06-20T20:13:30.000Z",
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
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```

#### Example 4: Finding tweets that match multiple saved searches, with nested boolean queries

This example illustrates combining multiple saved searches, a date range, and a query that narrows the search to only Twitter content.

The user wants documents that match the saved search with id 1001, AND that match **either** of the saved search with ids 1002 and ID 1003.

##### Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "all",
                "allQueries": [
                    {
                        "type": "savedSearch",
                        "searchId": 1001
                    },
                    {
                        "type": "any",
                        "anyQueries": [
                            {
                                "type": "savedSearch",
                                "searchId": 1002
                            },
                            {
                                "type": "savedSearch",
                                "searchId": 1003
                            }
                        ]
                    }
                ]
            },
            {
                "type": "all",
                "allQueries": [
                    {
                        "field": "metaData.source.socialOriginType",
                        "value": "twitter",
                        "type": "term"
                    },
                    {
                        "anyQueries": [
                            {
                                "field": "metaData.provider.type",
                                "value": "gnip",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "spinn3r",
                                "type": "term"
                            },
                            {
                                "field": "metaData.provider.type",
                                "value": "twitter",
                                "type": "term"
                            }
                        ],
                        "type": "any"
                    }
                ]
            },
            {
                "field": "body.publishDate.date",
                "from": "2020-06-16T20:13:30.000Z",
                "to": "2020-06-20T20:13:30.000Z",
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
            "fields": [
                "body.content.text"
            ],
            "size": 10,
            "start": 0
        }
    },
    "modifiers": {
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06",
        "productType": "swagger"
    }
}
```

## Twitter Guardrails Restrictions

Search API V2 handles twitter guardrails restrictions out of the box when using `savedSearch` queries. However, when `savedSearch` queries are used in combination with additional runes queries, twitter guardrails handling becomes more complex. Twitter guardrails are in place to prevent public companies from targeting individual users. We've put logic in place to try to ensure users don't bypass these restrictions by combining `savedSearch` queries with unapproved runes.

The following points clarify how the logic works in more complex cases:

* If the query contains a `savedSearch` query AND a query of type  [`term`](/docs/default/API/search-api-v1/queries/field-queries/#term-query), [`word`](/docs/default/API/search-api-v1/queries/field-queries/#word-query), or [`wildcard`](/docs/default/API/search-api-v1/queries/field-queries/#wildcard-query), then approval is `false` regardless of `twitterApproved` state of saved search

* If a `savedSearch` is part of the `notMatchQuery` part of a [`not query`](/docs/default/API/search-api-v1/queries/boolean-queries/#not-query), then approval is `false` regardless of `twitterApproved` state of saved search

* If there is a single `savedSearch` query in the request, the Search API V2 uses the approved value of that saved search.

* If there are multiple `savedSearch` queries in a request, the Search API V2 applies the `AND` operator between the approved values of those saved searches, i.e. final value can be `true` if and only if all searches have `twitterApproved: true`.

* [`modifiers.twitterApproved`](v2-request-modifiers.md#modifiers-parameters-in-detail) **overrides** the result of the logic explained above. If you would still need to set `modifiers.twitterApproved` along with the savedSearch(es) in query, **please reach out** to our [Slack channel](https://meltwater.slack.com/archives/CAJKZ9RDE) to discuss your use case.

For a clearer visualization, you can take a look at the flow chart diagram from [here](https://github.com/meltwater/gandalf/blob/5747cb2d015fad7a8ec546211ef30981aa55c2d2/docs/adr/0003-twitter-approval-logic.md)


## Search Information Types

**Standard (legacy) Searches**
Standard (legacy) MI searches have a specific information type i.e. "news", "social" or "broadcast". When building runes for these searches, the Search API V2 respects these information types,

**Explore Searches**
For backwards compatibility with some legacy components, explore searches are also saved with a specific information type. As with the Explore product itself, the Search API V2 does not use these information types when building runes with explore searches. For example, if you have an explore search that is saved as 'Social' search, you may still receive editorial or broadcast results when using the `savedSearch` query type.
