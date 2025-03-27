# Twitter

# Identifying individual tweets

If the Tweet id is known, it is possible to get that exact document in your results by searching for the id.

If the Tweet URL is, for example https://twitter.com/Meltwater/status/1278036897747447808 that document is targeted like this: `externalId:"id:twitter.com:1278036897747447808"` . The same principle also goes for finding retweets and replies, like this: `metaData.inReplyTo.externalId:"id:twitter.com:1278036897747447808"`. This is much more efficient than using the url.

## GNIP vs Firehose

Tweets are received from two systems: Firehose and GNIP. Firehose contains all public tweets while GNIP only contains tweets that matched a saved search. After a search is saved, _new_ tweets matching that search will come through GNIP.
Tweets that come through GNIP will always take preference over the same tweets that come via the Firehose.
The source of the tweet can be distinguished based on the `metaData.provider.type` field.
```
# GNIP tweets
metaData.source.socialOriginType: twitter
metaData.provider.type: gnip

# Firehose tweets
metaData.source.socialOriginType: twitter
metaData.provider.type: twitter
```

### Searching the Firehose
The Search API contains logic to exclude Firehose tweets _unless_ the query contains `metaData.provider.type=twitter`.
Therefore, searching over all tweets requires a query containing `(metaData.source.socialOriginType=twitter OR metaData.provider.type=twitter)` to access 100%. 
Searching only on `metaData.source.socialOriginType=twitter` will only match GNIP tweets (about 7-10% of all tweets) 

### Enrichments
Since 9 Dec 2019 both GNIP and Firehose tweets get almost the same enrichments. These are the known differences since then:

* GNIP tweets will have engagement metrics `enrichment.socialScores.[tw_likes, tw_retweets, tw_replies]`.
* body.links also includes shortened URLs for GNIP but not for Firehose
* `metaData.source.location.voiv` is always set to "Undef" for GNIP but no value for Firehose
* `metaData.authors.link` is always http links for GNIP and https for Firehose
* `metaData.url` is always http links for GNIP and https for Firehose
* `enrichments.location.countryCode` is populated in GNIP and is duplicated from `metaData.source.location.countryCode`
* `metaData.source.location.country` is populated in GNIP and is duplicated from `metaData.source.location.geonames.country`
* `metaData.authors.twitterInfo.bio` is populated in GNIP and is duplicated from `metaData.authors.bio`
* `metaData.authors.twitterInfo.imageUrl` is populated in GNIP and is duplicated from `metaData.authors.imageUrl`
* `metaData.authors.twitterInfo.username` is populated in GNIP and is duplicated from `metaData.authors.authorInfo.handle`

## Extracting timestamp from a Twitter id

The twitter id contains the timestamp and can be extracted with the following code snippet were >>> is unsigned bitwise right shift:

```java
(tweetId >>> 22) + 1288834974657
```

Source: https://github.com/oduwsdl/tweetedat
