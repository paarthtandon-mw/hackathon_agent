# Audience Aggregate View Request


## Audience Aggregate Data

The Search API V2 now has the ability to leverage Linkfluence to retrieve audience aggregate data on Twitter authors.

This can be enabled by adding the `audienceAggregate` view request to the `viewRequests` in the Search request:

```json
"audienceAggregate": {
  "type": "audienceAggregate",
  "size": 200,
  "minFollowers": 150
}
```

**Configuration:**

* **size** *(optional, default 100)*: represents the maximum number of unique twitter authors that will be used to retrieve audience aggregate data from Linkfluence's API. The large the number the better aggregate data, but the slower the request.
* **minFollowers** *(optional, default 50)*: represents the minimum number of followers a twitter author should have to be included. Recommended minimum value is 50.

## How it works
When using the `audienceAggregate` view request, the search request will be enhanced with an extra view request to retrieve (up to [`size`]) twitter authors having a follower count of at least 50. Before returning the search results, the list of authors will be sent to Linkfluence to build aggregate data which will then be included in the response.

## Sample Request

```json
{
    "query": {
        "type": "all",
        "allQueries": [
            {
                "type": "word",
                "field": "body.content.text",
                "value": "tesla"
            },
            {
                "field": "metaData.source.socialOriginType",
                "value": "twitter",
                "type": "term"
            },
            {
                "type": "range",
                "field": "body.publishDate.date",
                "from": "2021-09-01T04:00:00.000Z",
                "to": "2021-09-09T04:00:00.000Z"
            }
        ]
    },
    "viewRequests": {
        "documentCount": {
            "type": "count"
        },
        "audienceAggregate": {
            "type": "audienceAggregate",
            "size": 200,
            "minFollowers": 150
        },
        "resultList": {
            "type": "resultList",
            "start": 0,
            "size": 25,
            "fields": [
                "body.content.text",
                "metaData.url"
            ]
        }
    },
    "modifiers": {
        "productType": "swagger",
        "requestorCompanyId": "59103b0662eb71f944d99b05",
        "requestorUserId": "59103b0762eb71f944d99b06"
    }
}
```

## Sample Response

```json
{
    "views": {
        "documentCount": {
            "totalCount": 18050,
            "type": "count"
        },
        "resultList": {
            "results": [
                // documents
            ],
            "type": "resultList"
        },
        "audienceAggregate": {
            {
                "accountVerified": {
                    "values": [
                        {
                            "key": "0",
                            "count": 24
                        },
                        {
                            "key": "1",
                            "count": 1
                        }
                    ]
                },
                "entities": {
                    "values": [
                        {
                            "key": "SMU Mustangs football",
                            "count": 9
                        },
                        {
                            "key": "National Football League",
                            "count": 3
                        },
                        {
                            "key": "Baylor University",
                            "count": 3
                        },
                        {
                            "key": "Los Angeles Lakers",
                            "count": 2
                        },
                        {
                            "key": "National Basketball Association",
                            "count": 2
                        },
                        {
                            "key": "UCF Knights football",
                            "count": 2
                        },
                        {
                            "key": "Louisiana Tech University",
                            "count": 2
                        },
                        {
                            "key": "National Collegiate Athletic Association",
                            "count": 2
                        },
                        {
                            "key": "Republican Party",
                            "count": 2
                        },
                        {
                            "key": "Democratic Party",
                            "count": 2
                        },
                        {
                            "key": "Taliban",
                            "count": 2
                        },
                        {
                            "key": "Tesla",
                            "count": 2
                        },
                        {
                            "key": "American Athletic Conference",
                            "count": 2
                        },
                        {
                            "key": "Atlantic Coast Conference",
                            "count": 2
                        },
                        {
                            "key": "Canadian Football League",
                            "count": 1
                        },
                        {
                            "key": "Standard & Poor's",
                            "count": 1
                        },
                        {
                            "key": "college football",
                            "count": 1
                        },
                        {
                            "key": "Supreme Court of the United States",
                            "count": 1
                        },
                        {
                            "key": "United States Armed Forces",
                            "count": 1
                        },
                        {
                            "key": "artificial intelligence",
                            "count": 1
                        },
                        {
                            "key": "Information Technology",
                            "count": 1
                        },
                        {
                            "key": "National Hockey League",
                            "count": 1
                        },
                        {
                            "key": "Dallas Mavericks",
                            "count": 1
                        },
                        {
                            "key": "Bloomberg L.P.",
                            "count": 1
                        },
                        {
                            "key": "Tehrik-i-Taliban Pakistan",
                            "count": 1
                        },
                        {
                            "key": "Golden State Warriors",
                            "count": 1
                        },
                        {
                            "key": "Detroit Pistons",
                            "count": 1
                        },
                        {
                            "key": "World Economic Forum",
                            "count": 1
                        },
                        {
                            "key": "Communist Party of China",
                            "count": 1
                        },
                        {
                            "key": "Manchester United F.C.",
                            "count": 1
                        },
                        {
                            "key": "Tottenham Hotspur F.C.",
                            "count": 1
                        },
                        {
                            "key": "Montreal Canadiens",
                            "count": 1
                        },
                        {
                            "key": "privacy",
                            "count": 1
                        },
                        {
                            "key": "information security",
                            "count": 1
                        },
                        {
                            "key": "SpaceX",
                            "count": 1
                        },
                        {
                            "key": "Norddeutscher Rundfunk",
                            "count": 1
                        },
                        {
                            "key": "Dallas Cowboys",
                            "count": 1
                        },
                        {
                            "key": "Stanley Cup",
                            "count": 1
                        },
                        {
                            "key": "Denver Broncos",
                            "count": 1
                        },
                        {
                            "key": "NBA Playoffs",
                            "count": 1
                        },
                        {
                            "key": "ZDNet",
                            "count": 1
                        },
                        {
                            "key": "Vegas Golden Knights",
                            "count": 1
                        },
                        {
                            "key": "Women's National Basketball Association",
                            "count": 1
                        },
                        {
                            "key": "Oakland Raiders",
                            "count": 1
                        },
                        {
                            "key": "Accenture",
                            "count": 1
                        },
                        {
                            "key": "cloud computing security",
                            "count": 1
                        },
                        {
                            "key": "Amazon",
                            "count": 1
                        },
                        {
                            "key": "European Union",
                            "count": 1
                        },
                        {
                            "key": "United Nations General Assembly",
                            "count": 1
                        },
                        {
                            "key": "cloud computing",
                            "count": 1
                        },
                        {
                            "key": "Red Hat",
                            "count": 1
                        },
                        {
                            "key": "PricewaterhouseCoopers",
                            "count": 1
                        },
                        {
                            "key": "athletics",
                            "count": 1
                        },
                        {
                            "key": "Florida State Seminoles football",
                            "count": 1
                        },
                        {
                            "key": "SAP SE",
                            "count": 1
                        },
                        {
                            "key": "NATO",
                            "count": 1
                        },
                        {
                            "key": "TCU Horned Frogs football",
                            "count": 1
                        },
                        {
                            "key": "Texas Longhorns football",
                            "count": 1
                        },
                        {
                            "key": "Texas Tech Red Raiders football",
                            "count": 1
                        },
                        {
                            "key": "ransomware",
                            "count": 1
                        },
                        {
                            "key": "Southeastern Conference",
                            "count": 1
                        },
                        {
                            "key": "Los Angeles Clippers",
                            "count": 1
                        }
                    ]
                },
                "country": {
                    "values": [
                        {
                            "key": "US",
                            "count": 21
                        },
                        {
                            "key": "IN",
                            "count": 1
                        },
                        {
                            "key": "MX",
                            "count": 1
                        }
                    ]
                },
                "age": {
                    "values": [
                        {
                            "key": "65-121",
                            "count": 1
                        },
                        {
                            "key": "55-64",
                            "count": 3
                        },
                        {
                            "key": "45-54",
                            "count": 0
                        },
                        {
                            "key": "35-44",
                            "count": 2
                        },
                        {
                            "key": "25-34",
                            "count": 2
                        },
                        {
                            "key": "18-24",
                            "count": 5
                        },
                        {
                            "key": "13-17",
                            "count": 0
                        }
                    ]
                },
                "hashtag": {
                    "values": [
                        {
                            "key": "ponyupdallas",
                            "count": 5
                        },
                        {
                            "key": "ponyexpress",
                            "count": 3
                        },
                        {
                            "key": "ponyup",
                            "count": 3
                        },
                        {
                            "key": "texas",
                            "count": 3
                        },
                        {
                            "key": "afghanistan",
                            "count": 2
                        },
                        {
                            "key": "america",
                            "count": 2
                        },
                        {
                            "key": "cowboys",
                            "count": 2
                        },
                        {
                            "key": "cybersecurity",
                            "count": 2
                        },
                        {
                            "key": "facts",
                            "count": 2
                        },
                        {
                            "key": "hybridworkforce",
                            "count": 2
                        },
                        {
                            "key": "nfl",
                            "count": 2
                        },
                        {
                            "key": "retail",
                            "count": 2
                        },
                        {
                            "key": "sase",
                            "count": 2
                        },
                        {
                            "key": "smu",
                            "count": 2
                        },
                        {
                            "key": "1strounder",
                            "count": 1
                        },
                        {
                            "key": "4thofjuly",
                            "count": 1
                        },
                        {
                            "key": "5steps2sase",
                            "count": 1
                        },
                        {
                            "key": "aac",
                            "count": 1
                        },
                        {
                            "key": "acmawards",
                            "count": 1
                        },
                        {
                            "key": "afceatechnet",
                            "count": 1
                        },
                        {
                            "key": "amd",
                            "count": 1
                        },
                        {
                            "key": "american",
                            "count": 1
                        },
                        {
                            "key": "antifa",
                            "count": 1
                        },
                        {
                            "key": "aoc",
                            "count": 1
                        },
                        {
                            "key": "apple",
                            "count": 1
                        },
                        {
                            "key": "atx",
                            "count": 1
                        },
                        {
                            "key": "ausitnts",
                            "count": 1
                        },
                        {
                            "key": "ausitntx",
                            "count": 1
                        },
                        {
                            "key": "austin",
                            "count": 1
                        },
                        {
                            "key": "austint",
                            "count": 1
                        },
                        {
                            "key": "austintx",
                            "count": 1
                        },
                        {
                            "key": "b2b",
                            "count": 1
                        },
                        {
                            "key": "b2btop100",
                            "count": 1
                        },
                        {
                            "key": "babybaby",
                            "count": 1
                        },
                        {
                            "key": "badhumanity",
                            "count": 1
                        },
                        {
                            "key": "badmedia",
                            "count": 1
                        },
                        {
                            "key": "badpolitics",
                            "count": 1
                        },
                        {
                            "key": "badscience",
                            "count": 1
                        },
                        {
                            "key": "badsports",
                            "count": 1
                        },
                        {
                            "key": "basel",
                            "count": 1
                        },
                        {
                            "key": "battleofbritain",
                            "count": 1
                        },
                        {
                            "key": "beatlatech",
                            "count": 1
                        },
                        {
                            "key": "beatunt",
                            "count": 1
                        },
                        {
                            "key": "bereal",
                            "count": 1
                        },
                        {
                            "key": "betyourefromasmalltown",
                            "count": 1
                        },
                        {
                            "key": "biden",
                            "count": 1
                        },
                        {
                            "key": "big10",
                            "count": 1
                        },
                        {
                            "key": "big12toaac",
                            "count": 1
                        },
                        {
                            "key": "biglie",
                            "count": 1
                        },
                        {
                            "key": "birdsup",
                            "count": 1
                        },
                        {
                            "key": "bis",
                            "count": 1
                        },
                        {
                            "key": "bitcoin",
                            "count": 1
                        },
                        {
                            "key": "blackhistory",
                            "count": 1
                        },
                        {
                            "key": "blacklivesmatter",
                            "count": 1
                        },
                        {
                            "key": "blockchain",
                            "count": 1
                        },
                        {
                            "key": "blues",
                            "count": 1
                        },
                        {
                            "key": "boardsofdirectors",
                            "count": 1
                        },
                        {
                            "key": "bold",
                            "count": 1
                        },
                        {
                            "key": "bordercrisis",
                            "count": 1
                        },
                        {
                            "key": "breach",
                            "count": 1
                        },
                        {
                            "key": "breachdetection",
                            "count": 1
                        },
                        {
                            "key": "brenhamtx",
                            "count": 1
                        },
                        {
                            "key": "brnovich",
                            "count": 1
                        },
                        {
                            "key": "buckeyenation",
                            "count": 1
                        },
                        {
                            "key": "bucksvssuns",
                            "count": 1
                        },
                        {
                            "key": "bucs",
                            "count": 1
                        },
                        {
                            "key": "caotex",
                            "count": 1
                        },
                        {
                            "key": "captex",
                            "count": 1
                        },
                        {
                            "key": "casb",
                            "count": 1
                        },
                        {
                            "key": "ccim",
                            "count": 1
                        },
                        {
                            "key": "ccre",
                            "count": 1
                        },
                        {
                            "key": "cdr",
                            "count": 1
                        },
                        {
                            "key": "cds",
                            "count": 1
                        },
                        {
                            "key": "cedarcreeklake",
                            "count": 1
                        },
                        {
                            "key": "championshipvibes",
                            "count": 1
                        },
                        {
                            "key": "championsleague",
                            "count": 1
                        },
                        {
                            "key": "china",
                            "count": 1
                        },
                        {
                            "key": "chipmakers",
                            "count": 1
                        },
                        {
                            "key": "cloudsecurity",
                            "count": 1
                        },
                        {
                            "key": "cmscyberworks",
                            "count": 1
                        },
                        {
                            "key": "collegefootball",
                            "count": 1
                        },
                        {
                            "key": "collegekickers",
                            "count": 1
                        },
                        {
                            "key": "collegetownproblems",
                            "count": 1
                        },
                        {
                            "key": "commercialrealestate",
                            "count": 1
                        },
                        {
                            "key": "commercialrealestatebroker",
                            "count": 1
                        },
                        {
                            "key": "commerciarealestate",
                            "count": 1
                        },
                        {
                            "key": "commerecialestate",
                            "count": 1
                        },
                        {
                            "key": "commericalrealestate",
                            "count": 1
                        },
                        {
                            "key": "corpuschristi",
                            "count": 1
                        },
                        {
                            "key": "covid",
                            "count": 1
                        },
                        {
                            "key": "covid19india",
                            "count": 1
                        },
                        {
                            "key": "covidvaccine",
                            "count": 1
                        },
                        {
                            "key": "cr7",
                            "count": 1
                        },
                        {
                            "key": "cre",
                            "count": 1
                        },
                        {
                            "key": "creepyjoe",
                            "count": 1
                        },
                        {
                            "key": "cristianoronaldo",
                            "count": 1
                        },
                        {
                            "key": "crossdomainsolution",
                            "count": 1
                        },
                        {
                            "key": "crossdomainsolutions",
                            "count": 1
                        },
                        {
                            "key": "crre",
                            "count": 1
                        },
                        {
                            "key": "crucial",
                            "count": 1
                        }
                    ]
                },
                "language": {
                    "values": [
                        {
                            "key": "en",
                            "count": 21
                        },
                        {
                            "key": "de",
                            "count": 1
                        },
                        {
                            "key": "nl",
                            "count": 1
                        }
                    ]
                },
                "occupation": {
                    "values": [
                        {
                            "key": "engineer",
                            "count": 1
                        },
                        {
                            "key": "minister",
                            "count": 1
                        },
                        {
                            "key": "consultant",
                            "count": 1
                        },
                        {
                            "key": "rancher",
                            "count": 1
                        },
                        {
                            "key": "director",
                            "count": 1
                        },
                        {
                            "key": "manager",
                            "count": 1
                        },
                        {
                            "key": "professional wrestler",
                            "count": 1
                        },
                        {
                            "key": "businessperson",
                            "count": 1
                        },
                        {
                            "key": "sports analyst",
                            "count": 1
                        },
                        {
                            "key": "investor",
                            "count": 1
                        },
                        {
                            "key": "founder",
                            "count": 1
                        }
                    ]
                },
                "gender": {
                    "values": [
                        {
                            "key": "M",
                            "count": 19
                        },
                        {
                            "key": "U",
                            "count": 6
                        }
                    ]
                }
            }
        }
    }
}
```

