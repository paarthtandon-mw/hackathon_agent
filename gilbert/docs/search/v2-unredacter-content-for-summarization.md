# Getting unredacted content for summarization

**N.B.** This feature is disabled for almost all clients. If you do need it, 
then please reach out to us in 
[#platypus](https://meltwater.slack.com/archives/CAJKZ9RDE)

Before building functionality that uses GenAI, please read 
[these slides](https://docs.google.com/presentation/d/1RqPR6GNBaL0bUa6I5uFJKoxSHwsYqROR-zNme1e-eUo/edit#slide=id.g2a372f9ea78_0_5).
We also encourage you to share your efforts in 
[#rnd-genai-helpdesk](https://meltwater.slack.com/archives/C07DMP5JRDH)
chat room.

If your product uses GenAI to summarize content (for presenting to a user), 
you can request unredacted content to be included from Search v2 (this
is currently **not** supported in the other v2 APIs).

## Which documents can we summarize?

Along with each document returned in a result list, there is a 
[consumerAttributes](v2-consumer-attributes.md) object, which contains some
metadata about the document. This object may contain `isSummarizationDisabled`,
which indicates that any summarization of this document is **prohibited**.

So, your software **must** check that 
`consumerAttributes.isSummarizationDisabled` is **not true** for each document
you want to summarize.

## Requesting unredacted fields for summarization

Each `resultList` view request has a property `unredactedQuiddityFields`. 
Any field found in this list, will be returned unredacted from the Search API.
If you want the whole quiddity unredacted, you can set this field to the empty
list.

The unredacted fields will be found in the `unredactedQuiddity` property of
each search hit.

### Example

**Request**
```json
{
  "modifiers": {
    "enableLegalRestrictions": true,
    // ...
  },
  "query": {
    // ...
  },
  "viewRequests": {
    "resultList": {
      "type": "resultList",
      "fields": ["id", "body.content.text"],
      "unredactedQuiddityFields": ["body.content.text"],
      "size": 1
    }
  }
}
```

**Response**
```json
{
  "views": {
    "resultList": {
      "results": [
        {
          "quiddity": {
            "id": "CEnePBh7rusQq5ccPaV5DxCjXgc",
            "body": {
              "content": {
                "text": "A section of leaders and elders in Garissa are calling on the government to lift the ban on gypsum mining in the county which was put in ..."
              }
            }
          },
          "highlights": {},
          "consumerAttributes": {
            "disableInAppOpening": false,
            "isInternalSharingDisabled": false,
            "isSharingDisabled": false,
            "isSummarizationDisabled": false,
            "isSocialSharingDisabled": false,
            "isTranslateDisabled": false,
            "isEditingDisabled": false,
            "originalUrl": "https://www.kbc.co.ke/government-asked-to-lift-ban-on-gypsum-mining-in-garissa/",
            "restriction": "NOT_RESTRICTED",
            "restrictionHistory": [
              {
                "ruleName": "Non social content ingress and body truncation rule",
                "description": "Truncate the ingress, body to a maximum of 140 characters. Always include the last complete word in the ingress and body after truncation. Applies to all non-social sources apart from AFR and TheAustralian"
              },
              {
                "ruleName": "Non social content matchSentence truncation rule",
                "description": "Truncate the matchSentence for non social documents to a maximum of 140 characters. Always include the last complete word in the matchSentence after truncation"
              }
            ],
            "keywords": [],
            "matchTags": [],
            "matchQueryTags": []
          },
          "unredactedQuiddity": {
            "body": {
              "content": {
                "text": "A section of leaders and elders in Garissa are calling on the government to lift the ban on gypsum mining in the county which was put in place a year ago following increased insecurity in the mines.\n\nLed by the former MP aspirant for Balambala constituency Mohamed Aress, said that gypsum mining has contributed significantly to local and national tax revenues, funding critical public services and infrastructure projects and that the government should set up policies to allow the companies to resume operations.\n\nThe leaders further are calling on the newly appointed cabinet secretary for Mining Hassan Joho to come up with a plan to value- add gypsum in the coast and north eastern regions.\n\n“Our communities used to benefit from the mining companies especially through employment of our young people, food and water supply during drought seasons, building of madrasas and even paying for teachers in these areas,” Aress said.\n\n“We do not see any correlation between insecurity in Garissa town and mining activities in the interior parts of the county like Balambala, korakora and alinjugur. Insecurity should not be used to curtail genuine companies from carrying out mining activities that are benefiting hundreds of our people,’’ he added.\n\nThey also called on the government to deter illegal miners who do not have permits or trading licenses from conducting any mining activity in the county, alleging that they are the primary source of insecurity in the mining sector.\n\n“By reinstating gypsum mining, the mining companies aim to restore economic vitality, support sustainable development and ensure the well-being of our pastoralist population. The decision reflects our commitment to balancing environmental stewardship with economic prosperity, safeguarding both natural resources and livelihoods,” he said.\n\nMining activities in Garissa were banned in August last year by the Regional Security Committee and County Government following clashes at the sites which led to the death of at least nine people in separate incidents."
              }
            }
          }
        }
      ],
      "type": "resultList"
    }
  }
}
```