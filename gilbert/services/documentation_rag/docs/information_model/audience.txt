# Audience

Metrics on the audience that may have seen a document and their interactions with it, for example potential reach and social engagement.

If the field has an alias, it is written in **bold**.  Corresponding Gyda field names are written in *italics*.

!!! hint "Looking for Engagement Metrics"
    Engagement metrics have been [moved to their own page](../engagement/).

    Some older, legacy engagement metrics fields are still documented here while we migrate them to the new fields.

## Generic

| Field Name                              | Description                                                                              | Filter Type | Field Type | Owner       |
|-----------------------------------------|------------------------------------------------------------------------------------------|-------------|------------|-------------|
| `metrics.source.reach`<br><br>**reach** | Channel, author*, source, page reach                                                     | Range match | Float      | Shakespeare |
| `metrics.views.origin.estimated`        | Estimated views count on the originating channel                                         | Range match | Float      | Gecko       |
| `metrics.views.origin.total`            | Total views count on the originating channel.Currently available for twitch and twitter. | Range match | Float      | Tally       |
| `metrics.mediaViews.origin.total`       | Total views of all media attachments on the originating channel. Available for twitter   | Range match | Float      | Tally       |
| `metrics.shares.editorial.total`        | Total shares of a document in the editorial channel. Available for twitter               | Range match | Float      | Tally       |




## Legacy Fields

These fields are considered "legacy", as they're in the process of being phased out. You should continue to use them until instructed to migrate to their replacements.

Many of these fields are being replaced/augmented by the new [Engagement Metrics](../engagement/) fields.

| Field Name                                                                      | Description                                                                                                                                                                                                                                                 | Filter Type              | Field Type  | Owner         |
|---------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|-------------|---------------|
| enrichments.comscoreUniqueVisitors<br><br>**reach** // *reach*                  | Potential reach of the document, i.e. the maximum possible size of the audience.  <br><br>* For News articles using SimilarWeb to estimate potential monthly unique visitors.<br><br>* For Broadcast documents uses TVEyes local+global viewership numbers. | Range match, exact match | Long        | Haven         |
| enrichments.socialScores.fb_shares<br><br>**shares** // *socialScores.fb_shares* | Number of times this document has been shared on Facebook. Only available on News documents.<br><br>This field is updated with the latest number after 6, 24 and 168 hours.                                                                                 | Range match              | Float       | Core Platform |
| enrichments.socialScores.tw_shares<br><br>**shares** // *socialScores.tw_shares* | Number of times this document has been shared on Twitter. Only available on News documents.<br><br>This field is updated with the latest number continuously.                                                                                               | Range match              | Float       | Core Platform |
| enrichments.socialScores.rd_shares <br><br>*socialScores.rd_shares*             | Number of times this document has been shared on Reddit, both posts and comments. Only available on News documents.<br><br>This field is updated with the latest number continuously.                                                                       ||| Core Platform            |
| enrichments.socialScores.klout                                                  | To be added                                                                                                                                                                                                                                                 | To be added              | To be added | TBD           |
| enrichments.socialScoresUpdateTime                                              | The time socialScores were last updated. Timestamp in milliseconds since the Unix Epoch.                                                                                                                                                                    | Range match              | Long        | TBD           |
| audience.emv                                                                    | Earned media visits that this document generated. This field is customer specific and only available in overlays.                                                                                                                                           | Range match, exact match | Integer     | TBD           |
| enrichments.potentialReach.desktop                                              | Number of monthly unique visitors to the source using desktop clients.                                                                                                                                                                                      | Range match, exact match | Integer     | TBD           |
| enrichments.potentialReach.mobile                                               | Number of monthly unique visitors to the source using mobile clients.                                                                                                                                                                                       | Range match, exact match | Integer     | TBD           |


### Facebook
Only available on documents from Facebook.

| Field Name                                 | Description                                                                                                                                                               | Filter Type || Owner       |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-------------|--------|
| enrichments.socialScores.fb_likes          | Number of fans on the Facebook Page.<br><br>This field is updated with the latest number every 12h for period of 7 days (monitored page) or 30 days (competitors page)    | Range match | Float       |TBD|
| enrichments.socialScores.fb_members        | To be added                                                                                                                                                               | To be added | To be added |TBD|
| enrichments.socialScores.fb_post_comments  | Number comments on a Facebook post.<br><br>This field is updated with the latest number every 12h for a period of 7 days (monitored page) or 30 days (competitors page)   | Range match | Float       |TBD|
| enrichments.socialScores.fb_post_shares    | Number of shares of a Facebook post.<br><br>This field is updated with the latest number every 12h for a period of 7 days (monitored page) or 30 days (competitors page)  | Range match | Float       |TBD|
| enrichments.socialScores.fb_post_reactions | Number of reactions on Facebook post.<br><br>This field is updated with the latest number every 12h for a period of 7 days (monitored page) or 30 days (competitors page) | Range match | Float       |TBD|


### TVEyes
Only available on documents from TVEyes.

| Field Name                                | Description                                  | Filter Type || Owner |
|-------------------------------------------|----------------------------------------------|-------------|-------|--------|
| enrichments.socialScores.tve_reach_global | Global viewership number for this broadcast. | Range match | Float |Shakespeare|
| enrichments.socialScores.tve_reach_local  | Local viewership number for this broadcast.  | Range match | Float |Shakespeare|


### Twitter

| Field Name                             | Description                                                                                                                      | Filter Type || Owner |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|-------------|-------|--------|
| enrichments.socialScores.tw_likes      | Likes on this Tweet                                                                                                              | Range match | Float |Tally|
| enrichments.socialScores.tw_replies    | Replies to this Tweet                                                                                                            | Range match | Float |Tally|
| enrichments.socialScores.tw_retweets   | Retweets of this Tweet                                                                                                           | Range match | Float |Tally|
| enrichments.socialScores.tw_followers  | Reach of this Tweet                                                                                                              | Range match || TBD   |
| enrichments.socialScores.tw_following  | The number of other twitter accounts this twitter author is following.                                                           | Range match || TBD   |
| metaData.authors.twitterInfo.followers | **Deprecated:** <br>Use enrichments.socialScores.tw_followers instead<br><br>This field is NOT populated since early Spring 2021 | Range match || TBD   |

### Instagram

| Field name                            | Description                                 | Filter Type || Owner       |
|---------------------------------------|---------------------------------------------|-------------|-------------|--------|
| enrichments.socialScores.ig_comments  | Number of comments on an Instagram document | Range match | Float       |TBD|
| enrichments.socialScores.ig_followers | To be added                                 | To be added | To be added |TBD|
| enrichments.socialScores.ig_likes     | Number of likes on an Instagram document    | Range match | Float       |TBD|

### Linkedin

| Field name                                 | Description                                       | Filter type || Owner |
|--------------------------------------------|---------------------------------------------------|-------------|-------|--------|
| enrichments.socialScores.li_comments       | Number of comments on a Linkedin post             | Range match | Float |TBD|
| enrichments.socialScores.li_total_comments | Number of comments and replies on a Linkedin post | Range match | Float |TBD|
| enrichments.socialScores.li_likes          | Number of likes on a Linkedin post                | Range match | Float |TBD|
| enrichments.socialScores.li_replies        | Number of replies to a Linkedin post              | Range match | Float |TBD|

## ICE Rocket

| Field Name                        | Description | Filter Type | Field Type  | Owner |
|-----------------------------------|-------------|-------------|-------------|-------|
| enrichments.socialScores.ir_score | To be added | To be added | To be added | TBD   |
| enrichments.socialScores.ir_links | To be added | To be added | To be added | TBD   |


## Youtube

| Field Name                        | Description | Filter Type | Field Type  | Owner |
|-----------------------------------|-------------|-------------|-------------|-------|
| enrichments.socialScores.yt_views | To be added | To be added | To be added | TBD   |

