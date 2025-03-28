# Highlighting

The *highlightOptions* parameter accepts a map of field names and instructions for how to extract some text fragments that matched the query.

**Parameters**:

* **numberOfFragments**: The maximum number of fragments to extract.
* **fragmentSize**: The maximum character length of the fragments.
* **strictFragmentSize** (default *false*): Enforce a strict maximum length on the fragments.
* **keywords** (default *false*): Extract a list of the matching query keywords.
* **preTag**: Text to insert before matched keywords, for example for markup purposes.
* **postTag**: Text to insert after matched keywords, for example for markup purposes.

**Example**, extract 3 fragments matching the query of maximum length 140 characters, and surround matched keywords and phrases with `<em>` tags.
```json
{
  "type": "resultList",
  "fields": ["metaData.url", "body.title.text"],
  "highlightOptions": {
    "body.content.text": {
      "numberOfFragments": 2,
      "fragmentSize": 75,
      "keywords": true,
      "preTag": "<em>",
      "postTag": "</em>"
    }
  }
}
```

**Response**, contains the fields and extracted snippets
```json
{
  "type": "resultList",
  "results": [
    {
      "quiddity": {
        "metaData": {
          "url": "https://techcrunch.com/2018/03/19/meltwater-has-acquired-datasift-to-double-down-on-social-media-analytics/"
        },
        "body": {
          "title": {
            "text": "Meltwater has acquired DataSift to double down on social media analytics"
          }
        }
      },
      "highlights": {
        "body.content.text": {
          "fragments": [
            "is being <em>acquired</em> by <em>Meltwater</em>, the company originally out of Norway",
            "The idea will be to bring that together with <em>Meltwater</em>’s existing business to enhance it."
          ],
          "keywords": ["Meltwater", "acquired"]
        }
      }
    },
    {
      "quiddity": {
        "metaData": {
          "url": "https://techcrunch.com/2017/08/29/meltwater-acquires-algo-an-ai-based-news-and-data-tracker/"
        },
        "body": {
          "title": {
            "text": "Meltwater acquires Algo, an AI-based news and data tracker"
          }
        }
      },
      "highlights": {
        "body.content.text": {
          "fragments": [
            "<em>Meltwater</em>, a company that provides data to more than 25,000 businesses to track where and how they are mentioned in media",
            "The company has <em>acquired</em> Algo, a startup that has built a data analytics platform for real-time searches"
          ],
          "keywords": ["Meltwater", "acquired"]
        }
      }
    }
  ]
}
```

