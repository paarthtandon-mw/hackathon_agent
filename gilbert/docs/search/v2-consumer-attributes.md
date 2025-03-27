# Response Consumer Attributes

## Purpose

The Search/Export API V2 results include extra data on top of the results retrieved from Elasticsearch. This data may originate from other APIs such as the [GeoService API](https://geo-external.meltwater.io/swagger-ui.html), or might be the result of some transformations on the data, such as copyright restriction. To keep a clear distinction between this extra data and the document data in Elasticsearch, it's wrapped in a `consumerAttributes` object as part of with each document in a resultList.

For example, a `resultList` of documents will be in the format:

```json
[
  {
    "quiddity": { ... },
    "highlights": { ... },
    "consumerAttributes": {...}
  },
  {
    "quiddity": { ... },
    "highlights": { ... },
    "consumerAttributes": {...}
  }
]                  
```

## Sample `consumerAttributes`

The following gives an example of what a populated `consumerAttributes` object looks like. We'll go through each item in more detail below.

```json
{
    "quiddity": {},
    "highlights": {},
    "consumerAttributes": {
        "paywallUrl": "https://staging-transition.meltwater.net/paywall/redirect/777ef6d1bea73deb810c57aaa7318c4f7f28b475",
        "embedUrl": "https://staging-transition.meltwater.net/paywall/redirect/KFeg9kETv47NMvxPg6wqfT9wdxY?keywords=liverpool%252CLiverpool&tveyes-slim=true",
        "matchSentence": "Canning Vale Po lice are investigating <em>a</em> burglary that occurred at <em>a</em> vet erinary clinic on Alex Wood Drive in Forrestdale on Monday June 21",
        "disableInAppOpening": false,
        "isInternalSharingDisabled": true,
        "isSharingDisabled": true,
        "isSummarizationDisabled": false,
        "isSocialSharingDisabled": true,
        "isTranslateDisabled": false,
        "isEditingDisabled": false,
        "originalUrl": "https://ausprint.meltwater.com/print_clip_previewer/336318816?text=on",
        "redirectUrl": "https://staging.meltwater.net/mwTransition?url=https%3A%2F%2Fmms.tveyes.com%2Fmediaview%2F%3FstationId%3D6660%26startDateTime%3D1632849729%26dur%3D151707%26highlightRegex%3D%255Cbliverpool%255Cb%7C%255CbLiverpool%255Cb%26utcOffset%3D-21600000&urlCategories=tveyes&analytics=false&documentId=KFeg9kETv47NMvxPg6wqfT9wdxY",
        "restriction": "NOT_RESTRICTED",
        "restrictionHistory": [
            {
                "ruleName": "disable social sharing for documents from Connect Media ausprint",
                "description": ""
            },
            {
                "ruleName": "truncate matchSentence to max 140 characters for all non-social documents",
                "description": "Truncate the matchSentence to a maximum of 140 characters. Always include the last complete word in the matchSentence after truncation"
            }
        ],
        "tagContextMatchSentence": null,
        "urlTransitionToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJob3N0bmFtZSI6ImF1c3ByaW50Lm1lbHR3YXRlci5jb20ifQ.QdceaYdYa6J4VgtiHX6ZFCPUV-BG_9xIpB9plG3kQyMxxBgU-V3kwbNkPfOkjrTZVKRHkx3gIYKWwXGPTgJvFQ",
        "sourceUrlTransitionToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJob3N0bmFtZSI6Ind3dy5mYWNlYm9vay5jb20ifQ.-HrxofHsozh019XvgyhewiKqVAxYat5UlHxCHQfge-kzS1UwHRDdocSiPUTBHLW6s5Pmi23CyLKprs3z_Qw0vQ",
        "keywords": [
            "burglary", "Forrestdale"
        ],
        "matchTags": [
            "Forrestdale"
        ],
        "newsguardLinkScores": [
            {
                "url": "https://www.youtube.com/@BBCNewsMarathi",
                "score": 10.0
            },
            {
                "url": "https://www.facebook.com/BBCnewsMarathi",
                "score": null
            },
            {
                "url": "https://twitter.com/bbcnewsmarathi",
                "score": null
            },
            {
                "url": "https://www.bbc.com/marathi/podcasts/p0b1s4nm",
                "score": 95.0
            }
        ],
        "geonames": {
            "place": {
                "id": 2643743,
                "names": {
                    "original": "London"
                },
                "type": "city",
                "countryCode": "GB",
                "timezone": "Europe/London",
                "latitude": 51.50853,
                "longitude": -0.12574
            },
            "adm1": {
                "id": 6269131,
                "names": {
                    "original": "England"
                },
                "type": "admin1",
                "countryCode": "GB",
                "timezone": "Europe/London",
                "latitude": 52.16045,
                "longitude": -0.70312
            },
            "adm2": {
                "id": 2648110,
                "names": {
                    "original": "Greater London"
                },
                "type": "admin2",
                "countryCode": "GB",
                "timezone": "Europe/London",
                "latitude": 51.5,
                "longitude": -0.16667
            },
            "country": {
                "id": 2635167,
                "names": {
                    "original": "United Kingdom"
                },
                "type": "country",
                "countryCode": "GB",
                "timezone": "Europe/London",
                "latitude": 54.75844,
                "longitude": -2.69531
            },
            "continent": {
                "id": 6255148,
                "names": {
                    "original": "Europe"
                },
                "type": "continent",
                "timezone": "Europe/Vaduz",
                "latitude": 48.69096,
                "longitude": 9.14062
            },
            "regions": [
                {
                    "id": 7729883,
                    "names": {
                        "original": "Northern Europe"
                    },
                    "type": "region",
                    "timezone": "",
                    "latitude": 61.68987,
                    "longitude": 2.90039
                }
            ]
        }
    }
}
```

## `consumerAttributes` parameters in detail

| Name                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| paywallUrl                | Url that can be used to bypass paywalls. Only added if necessary - i.e. <br><br>Only set when `modifiers.enablePaywall: true`                                                                                                                                                                                                                                                                                                     |
| embedUrl                  | Similar to paywallUrl, but can be used when the document is to be viewed in an embedded player such as broadcast content.<br><br>Only set when `modifiers.enablePaywall: true`                                                                                                                                                                                                                                                    |
| matchSentence             | The sentence from the document that matched the query - extracted from `highlights` response object                                                                                                                                                                                                                                                                                                                               |
| disableInAppOpening       | A boolean to signify whether or not the document is allowed be to opened "in app".<br><br>For Search v2 and Export v2 APIs, this is only set when `modifiers.enableLegalRestrictions: true`.                                                                                                                                                                                                                                      |
| isInternalSharingDisabled | A boolean to signify if internal sharing (via email) of the document is prohibited (specific logic for NSW companies)<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                              |
| isSharingDisabled         | A boolean to signify if sharing (via email) of the document is prohibited<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                          |
| isSummarizationDisabled   | A boolean to signify if summarization of the document is prohibited<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                                |
| isSocialSharingDisabled   | A boolean to signify if sharing (via social channels) of the document is prohibited<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                |
| isTranslateDisabled       | A boolean to signify if translation of the document is prohibited<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                                  |
| isEditingDisabled         | A boolean to signify if editing of the document is prohibited<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                                      |
| originalUrl               | When mwTransition urls are being used (transition urls are the precursor to paywall urls), the document url with a transition url If the source has a paywall, and if we have an agreement with the provider to bypass their paywalls. In these cases, the document url will be copied to the `originalUrl` field. <br><br>Only set when `modifiers.enableLegalRestrictions: true` and `modifiers.enableMWTransitionTokens: true` |
| redirectUrl               | For "tyeyes" sources, a redirect url may be used to redirect to the original document for embedded documents<br><br>Only set when `modifiers.enableLegalRestrictions: true` and `modifiers.enableMWTransitionTokens: true`                                                                                                                                                                                                        |
| restriction               | Legacy field for backwards compatibility - can be ignored.<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                                         |
| restrictionHistory        | A list of legal restriction rules that have been applied to the document.<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                          |
| tagContextMatchSentence   | Simlar to `matchSentence` but applies to the sentence of the document that matched the tag query                                                                                                                                                                                                                                                                                                                                  |
| urlTransitionToken        | The signed token that is used to build a mwTransitionUrl.                                                                                                                                                                                                                                                                                                                                                                         |
| sourceUrlTransitionToken  | Legacy field for backwards compatibility - can be ignored.<br><br>Only set when `modifiers.enableLegalRestrictions: true`                                                                                                                                                                                                                                                                                                         |
| keywords                  | A list of keywords matching the query. - extracted from `highlights` response object                                                                                                                                                                                                                                                                                                                                              |
| matchTags                 | A list of tags matching the query                                                                                                                                                                                                                                                                                                                                                                                                 |
| newsguardLinkScores       | If a request comes from a specific product type and the company has a Newsguard entitlement, this field will be enriched by calling [Newsguard Service](https://newsguard-service-prod-internal.meltwater.io/swagger-ui)                                                                                                                                                                                                          |
| geonames                  | If the document contains geoIds for location data, these will be enriched by calling the [GeoService API](https://geo-external.meltwater.io/swagger-ui.html). the `consumerAttribues.genames` object will contain the enrichmed version of these geolation fields.<br><br>Only set when `modifiers.enableGeonames: true`                                                                                                          |
| protectedUrl              | This field only occurs in responses from the Consumer Ready Document API, and only for documents from Süddeutsche Zeitung. This is a URL with a generated token, which allows the user to access the printed article.                                                                                                                                                                                                             |

