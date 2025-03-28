# Query use cases

!!! type "There is always room for another use case ..."
This list is not complete - please add your use case (a complete query) below, briefly describing it.

## Top 5 Twitter followers

This query returns the top 5 authors with the most followers whose tweets match the query "meltwater". 

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "word",
                "field": "body.content.text",
                "value": "meltwater"
            },
            {
                "type": "range",
                "field": "body.publishDate.date",
                "from": "1574836800000",  
                "to": "1577923200000"
            },
            {
                "type": "term",
                "field": "metaData.source.socialOriginType",
                "value": "twitter"
            }
        ]
    },
    "viewRequests": {
        "uniqueAuthors": {  
          "type": "termsFacet",
          "termsField": "metaData.authors.authorInfo.externalId",
          "size": "5",
          "subViewRequests": {
            "twitterFollowers": {
              "type": "statistics",
              "field": "enrichments.socialScores.tw_followers",
              "measures": ["MAX"]
            }
          },
          "sortDirectives": [
            {
              "sortBy": "twitterFollowers.statistics.MAX",
              "sortOrder": "DESC"
            }
          ]}
        }
}
```



## Getting Documents from specific URL

```json
{
  "query": {
    "type": "all",
    "allQueries": [
      {
        "type": "wildcard",
        "field": "metaData.url",
        "value": "https://www.domain.com*"
      },
      {
        "type": "range",
        "field": "body.publishDate.date",
        "from": 1546300800000,
        "to": 1546905599999
      }
    ]
  },
  "viewRequests": {
    "documentCount": {
      "type": "count"
    },
    "searchResults": {
      "type": "resultList",
      "start": 0,
      "size": 2,
      "fields": [
        "body.title.text",
        "body.publishDate.date",
        "metaData.url"
      ]
    }
  },
  "restrictions": {
    "requestorCountry": "se"  
  }
}
```



## Number of documents per Source id



```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "field": "metaData.provider.specifier",
                "value": "pulitzer",
                "type": "term"
            },
            {
                "field": "body.publishDate.date",
                "from": 1600070400000,
                "to": 1600279200000,
                "type": "range"
            }
        ]
    },
    "viewRequests": {
        "sources": {
            "type": "termsFacet",
            "size": 7000,
            "includeDocErrorUpperBound": false,
            "termsField": "metaData.source.id"
        }
    }
}
```

