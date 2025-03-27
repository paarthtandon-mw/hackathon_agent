# Engagement Metrics

Metrics on user engagement on this document, for example, social engagement (likes, comments, etc.) or document shares.

All fields in this document are owned by [Tally](https://meltwater.atlassian.net/wiki/spaces/TAL/overview).

!!! hint "Audience Metrics"

    `reach` and `views` are not included in this document, as they are [audience metrics](../audience), not engagement
    metrics.

!!! summary "Gyda Documents"

    This documentation applies to both the Information Model General Schema and Gyda documents.

    The fields are identical in both schemas.

## Channels

A "channel" is a source of documents monitored by Meltwater. Channels can be any
[`socialOriginType`](../source#social-origin-type), `editorial` or
[`origin` for the virtual "origin" channel](#origin-fields).

Examples of channels include [`editorial`](#editorial), [`twitter`](#xtwitter), and [`sina_weibo`](#sina-weibo).

## Origin Fields

The metrics tree includes a "virtual channel", called `origin`, which contains the metrics from the channel the document originated.
For example, a X/Twitter tweet will contain:

- `metrics.shares.origin.total`: Reposts and quotes of the tweet on X/Twitter.
- `metrics.shares.origin.retweets`: Just the Reposts.
- `metrics.shares.origin.quotes`: Just the Quote Tweets.

And an Editorial document will contain:
- `metrics.shares.origin.total`: Links to this document from other Editorial documents.
- `metrics.shares.twitter.total`: Links to this document shared on X/Twitter, aka. "Social Echo".
- `metrics.shares.reddit.total`: Links to this document shared on Reddit, aka. "Social Echo".
- `metrics.shares.facebook.total`: Links to this document shared on Facebook, aka. "Social Echo".

This provides a common set of metrics that can be used in search queries to query across different channels.

For example, a query for `metrics.shares.origin.total > 0` will produce every document that has been shared at least once within the
channel it originated.

If you wish to search for documents only from a specific channel (e.g. "X/Twitter"), you should also include a predicate on the
`socialOriginType`.

### Summing metrics across all channels

All channel sums are represented in the field `metrics.*.total`. When summing shares of a document across _all channels_ `origin` represents the metrics of the origin platform and the named metrics (like metrics.shares.(twitter|facebook|reddit).total) represent shares in other platforms. 
Ex.-1 when we count the total shares across all platforms for an editorial document:

```
metrics.shares.total = metrics.shares.origin.total + metrics.shares.twitter.total + metrics.shares.facebook.total + metrics.shares.reddit.total
```
Ex.-2 when we count the total shares accross all platforms for a twitter document (we only provide editorial shares of twitter documents so far)  :
```
metrics.shares.total = metrics.shares.origin.total + metrics.shares.editorial.total
```

## Share Metrics

Share metrics record the number of times a document was shared on a platform. The mechanism for sharing varies by
platform. Usually, documents shared within the same platform use a platform-specific sharing mechanism (e.g. Retweets,
on [X/Twitter](#xtwitter)), but documents shared _across_ platforms are shared by mention of their URL (e.g. sharing a
tweet on [Reddit](#reddit)).

## Conversation Metrics

Conversation metrics capture the number of documents that are comments on or replies to a document.

!!! help "Terminology"

    The terms used to describe conversation differs from platform-to-platform. The metrics are all under the `threads`
    tree, but this term should _never_ be displayed to end-users.

    Instead, the term should match what users would expect conversation to be labelled as on the platform it takes place
    on, for example "Replies" on [X/Twitter](#xtwitter), and "Comments" on [Reddit](#reddit).

    The field tables provide a recommended English language display name for each source.

We capture both linear conversations, where every comment is a direct reply to the top-level document, and threaded
conversations, where comments can reply to other comments within the thread.

Comments/replies are counted [transitively](#transitive-replies) on all channels.

!!! help "<a id="transitive-replies"></a>Transitive Replies"

    For threaded conversations, conversation metrics count every document that is _below_ the current document in the
    thread.

    This means that a parent post will count every reply, replies to replies, replies to replies to replies, etc.
    Also, comments/replies in the thread will count every reply to that comment, as well as replies to replies, etc.

    Comments/replies in a thread will _not_ count other comments/replies that are part of a different sub-thread.

## Reaction Metrics

Reaction metrics capture engagement that doesn't provide any additional content (i.e.
[conversation](#conversation-metrics)) or broadcast the document to a wider audience (i.e. [shares](#share-metrics)),
such as "likes" and "upvotes".

The available reactions depend on the platform in question, only reactions supported by a platform will be available on
documents from that platform. Where multiple platforms use the same (or similar) terminology _and semantics_ for a
reaction, we have abstracted that reaction to a common name, e.g. both [Facebook](#facebook) and [X/Twitter](#xtwitter)
have `likes`, but only [Facebook](#facebook) has `loves`.

## Sorting

!!! hint "TL;DR"

    To sort by all [origin](#origin-fields) engagement, use the following IR sort [`script`](docs/default/api/search-api-v1/advanced-usage/script-dsl/):

    ```
        .metrics.shares.origin.total + .metrics.threads.origin.total + .metrics.reactions.origin.total
    ```

If you need to sort by the total [origin](#origin-fields) engagement on a document:

!!! hint "TL;DR"

    To sort by Social Echo:

    ```
     .metrics.shares.reddit.total + .metrics.shares.twitter.total + .metrics.shares.facebook.total
    ```

!!! warning "Important"

    Note that social-echo is just a specific cross channel engagement which is only valid for **editorial documents**. If you
    use this query for mixed document types you will get mixed results not just social echo.

## Fields

<h3>Legend</h3>

| Style                             | Meaning                                                                                                             |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------|
| _`italic`_                        | Metric is approximate, as it is updated on a schedule.                                                              |
| <span class="fade">`faded`</span> | Metric is not yet implemented/available.                                                                            |
| ~~`struck-through`~~              | Metric is legacy/deprecated.<br/>Use this metric _only if_ its replacement metric is not available on the document. | 

### Author engagement

Generic author engagement metrics across various social media networks.

| Field                            | Aliases     | Description                                         | Filter Type | Filter Type | Owner                   |
|-----------------------------------------------------|-------------|-----------------------------------------------------|-------------|------|-------------------------|
| `metrics.author.followers` | `followers` | The number of people who follow the author. | Range match, exact match | Long | Information Model Guild |
| `metrics.author.following` | `following` | The number of accounts the author follows. | Range match, exact match | Long | Information Model Guild |
| `metrics.author.posts` | `posts`     | The total number of posts (tweets, photos, videos, updates) the author has shared on the platform. | Range match, exact match | Long | Information Model Guild |

### Bluesky

All metrics fields available on Bluesky Posts.

!!! warning "Important"

    Some field names use legacy terminoloy derived from Twitter. Specifically `retweets`. This is not a typo. We are using the
    same field name in Bluesky to enable a single query to match data across both Bluesky and X/Twitter, and renaming the field
    would not be practical.

| Field                            | Aliases                       | Label   | Description                                                                                                                    |
|----------------------------------|-------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.retweets` | `retweets`<br/>               | Reposts | Total reposts of this Bluesky post within Bluesky.                                                                             |
| `metrics.shares.origin.quotes`   | `quotes`<br/>                 | Quotes  | Total quotes of this Bluesky post within Bluesky.                                                                              |
| `metrics.shares.origin.total`    | `shares`<br/>                 | Shares  | Total shares (reposts + quotes) of this Bluesky post within Bluesky.                                                           |   
| `metrics.threads.origin.total`   | `comments`<br/>`replies`<br/> | Replies | Total replies to this Bluesky post within Bluesky, including [transitive replies](#transitive-replies).                        |
| `metrics.reactions.origin.likes` | `likes`                       | Likes   | Total "like" reactions on this Bluesky post within Bluesky.                                                                    |
| `metrics.reactions.origin.total` | `reactions`                   | Likes   | Total reactions on this Bluesky post within Bluesky.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |

### Douyin

All metrics fields available on Douyin posts.

| Field                            | Aliases                       | Label     | Description                                                                                                                                                                                                                                   |
|----------------------------------|-------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`    | `shares`                      | Reposts   | Total shares of this Douyin document within Douyin.                                                                                                                                                                                           |
| `metrics.threads.origin.total`   | `comments`<br/>`replies`<br/> | Comments  | Total replies to this Douyin document within Douyin, including [transitive replies](#transitive-replies).                                                                                                                                     |
| `metrics.reactions.origin.likes` | `likes`                       | Likes     | Total "like" reactions on this Douyin document within Douyin.                                                                                                                                                                                 |
| `metrics.reactions.origin.total` | `reactions`                   | Likes     | Total reactions on this Douyin document within Douyin.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                                                                                                              |

### Editorial

All metrics fields available on Editorial/news documents.

| Field                                                                    | Aliases    | Label    | Description                                                                                                                |
|--------------------------------------------------------------------------|------------|----------|----------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`                                            | `shares`   | Shares   | Total references to this document's URL in other editorial documents.                                                      |
| `metrics.shares.facebook.total` ~~`enrichments.socialScores.fb_shares`~~ | `shares`   | Shares   | Total references to this document's URL on Facebook.<br/><br/>Updated 24 hours and 7 days after document is first indexed. |
| `metrics.shares.reddit.total`~~`enrichments.socialScores.rd_shares`~~    | `shares`   | Shares   | Total references to this document's URL on Reddit.                                                                         |
| `metrics.threads.reddit.total`                                           | `threads`  | threads  | Total replies to this document's URL on Reddit.                                                                            |
| `metrics.shares.twitter.total`~~`enrichments.socialScores.tw_shares`~~   | `shares`   | Shares   | Total references  to this document's URL on X/Twitter.                                                                     |
| `metrics.shares.twitter.tweets`                                          | `tweets`   | Tweets   | Total number of tweets mentioning this document's URL                                                                      |
| `metrics.shares.twitter.quotes`                                          | `quotes`   | Quotes   | Total number of quotes mentioning this document's URL                                                                      |
| `metrics.shares.twitter.retweets`                                        | `retweets` | Retweets | Total number of retweets of tweets mentioning this document's URL                                                          |             
| `metrics.threads.twitter.total`                                          | `replies`  | Replies  | Total number of replies mentioning this document's URL                                                                     |


### Facebook

All metrics fields available on Facebook Posts and Comments.

_Facebook's engagement metrics are approximate, as they are updated periodically, every 12 hours after the Facebook
document is indexed, for 7 days (monitored pages) or 30 days (competitor pages)_

| Field                                                                                       | Aliases                  | Label     | Description                                                                                                                                                                                                          |
|---------------------------------------------------------------------------------------------|--------------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`<br/>~~`enrichments.socialScores.fb_post_shares`~~             | `shares`                 | Shares    | Total shares of this Facebook document within Facebook.                                                                                                                                                              |
| `metrics.threads.origin.total`<br/>~~`enrichments.socialScores.fb_post_comments`~~          | `comments`<br/>`replies` | Comments  | Total comments/replies to this Facebook document within Facebook, including [transitive replies](#transitive-replies).                                                                                               |
| `metrics.reactions.origin.likes`                                                            | `likes`                  | Likes     | Total "like" (and "care") reactions on this Facebook document within Facebook.                                                                                                                                       |
| `metrics.reactions.origin.loves`                                                            | `loves`                  | Loves     | Total "love" reactions on this Facebook document within Facebook.                                                                                                                                                    |
| `metrics.reactions.origin.wows`                                                             | `wows`                   | Wows      | Total "wow" reactions on this Facebook document within Facebook.                                                                                                                                                     |
| `metrics.reactions.origin.hahas`                                                            | `hahas`                  | Hahas     | Total "haha" reactions on this Facebook document within Facebook.                                                                                                                                                    |
| `metrics.reactions.origin.sorrys`                                                           | `sorrys`                 | Sorrys    | Total "sorry" reactions on this Facebook document within Facebook.                                                                                                                                                   |
| `metrics.reactions.origin.angrys`                                                           | `angrys`                 | Angrys    | Total "angry" reactions on this Facebook document within Facebook.                                                                                                                                                   |
| `metrics.reactions.origin.total`<span><br/>~~`enrichments.socialScores.fb_post_reactions`~~ | `reactions`              | Reactions | Total reactions on this Facebook document within Facebook.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                                                                                 |

### Instagram 

All metrics fields available on Instagram Posts 

_Instagram engagement metrics are approximate, as they are updated periodically, every 20 minutes after the Instagram 
document is indexed, for up to 30 days maximum_

| Field                            | Aliases                  | Label     | Description                                                                                                                            |
|----------------------------------|--------------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.threads.origin.total`   | `comments`<br/>`replies` | Comments  | Total comments/replies to this Instagram document within Instagram, including [transitive replies](#transitive-replies).               |
| `metrics.reactions.origin.likes` | `likes`                  | Likes     | Total "like"  reactions on this Instagram document within Instagram.                                                                   |
| `metrics.reactions.origin.total` | `reactions`              | Reactions | Total reactions on this Instagram document within Instagram.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |

### Little Red Book

All metrics fields available on Little Red Book posts.

| Field                                | Aliases                       | Label     | Description                                                                                                                                                                                                |
|--------------------------------------|-------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.threads.origin.total`       | `comments`<br/>`replies`<br/> | Comments  | Total replies to this Little Red Book post within Little Red Book, including [transitive replies](#transitive-replies).                                                                                    |
| `metrics.reactions.origin.likes`     | `likes`                       | Likes     | Total "like" reactions on this Little Red Book post within Little Red Book.                                                                                                                                |
| `metrics.reactions.origin.favorites` | `favorites`<br/>`favourites`  | Stars     | Total "star" reactions on this Little Red Book post within Little Red Book.                                                                                                                                |
| `metrics.reactions.origin.total`     | `reactions`                   | Reactions | Total reactions on this Little Red Book post within Little Red Book.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                                                             |

### Pinterest

All metrics fields available on Pinterest posts.

| Field                          | Aliases                       | Label    | Description                                                                                                                                                                                          |
|--------------------------------|-------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`  | `shares`                      | Saves    | Total shares of this Pinterest post within Pinterest.                                                                                                                                                |
| `metrics.threads.origin.total` | `comments`<br/>`replies`<br/> | Photos   | Total replies to this Pinterest post within Pinterest, including [transitive replies](#transitive-replies).                                                                                          |

### Reddit

All metrics fields available on Reddit Posts and Comments.

| Field                                                                 | Aliases                  | Label      | Description                                                                                                                                                                                                    |
|-----------------------------------------------------------------------|--------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <span class="fade">`metrics.shares.origin.total`</span>               | `shares`                 | Crossposts | Total shares of this Reddit document within Reddit.                                                                                                                                                            |
| <span class="fade">`metrics.shares.total`</span>                      |                          | Shares     | Total shares of this Reddit document across _all_ [channels](#channels).<br/><br/>For details [see above](#Summing-metrics-across-all-channels).                                                               |
| `metrics.threads.origin.total`                                        | `comments`<br/>`replies` | Comments   | Total comments/replies to this Reddit document within Reddit, including [transitive replies](#transitive-replies).                                                                                             |
| `metrics.reactions.origin.score`                                      | `score`                  | Score      | Aggregate of up-votes and down-votes on this Reddit document within Reddit.                                                                                                                                    |

### Sina Weibo

All metrics fields available on Sina Weibo posts.

| Field                                | Aliases                       | Label     | Description                                                                                                                                                                                                                    |
|--------------------------------------|-------------------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`        | `shares`                      | Shares    | Total shares of this Sina Weibo post within Sina Weibo.                                                                                                                                                                        |
| `metrics.threads.origin.total`       | `comments`<br/>`replies`<br/> | Replies   | Total replies to this Sina Weibo post within Sina Weibo, including [transitive replies](#transitive-replies).                                                                                                                  |
| `metrics.reactions.origin.favorites` | `favorites`<br/>`favourites`  | Favorites | Total "favorite" reactions on this Sina Weibo post within Sina Weibo.                                                                                                                                                          |
| `metrics.reactions.origin.total`     | `reactions`                   | Favorites | Total reactions on this Sina Weibo post within Sina Weibo.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                                                                                           |

### Snapchat

All metrics fields available on Snapchat posts.

| Field                            | Aliases     | Label     | Description                                                                                                             |
|----------------------------------|-------------|-----------|-------------------------------------------------------------------------------------------------------------------------|
| `metrics.reactions.origin.likes` | `likes`     | `likes`   | Total likes of this snap within Snapchat.                                                                               |
| `metrics.reactions.origin.total` | `reactions` | `likes`   | Total reactions on this snap within Snapchat.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |
| `metrics.shares.origin.total`    | `shares`    | `shares`  | Total shares of this snap within Snapchat.                                                                              |
| `metrics.threads.origin.total`   | `replies`   | `replies` | Total replies to this snap within Snapchat.<br/><br>This is the sum of all other `metrics.threads.origin.*` fields.     |
| `metrics.views.origin.total`     | `views`     | `views`   | Total views of this snap within Snapchat.<br/><br>This is the sum of all other `metrics.views.origin.*` fields.         |


### Social Blogs

All metrics fields available on socials blogs.

This includes Wordpress metrics fields.

| Field                            | Aliases | Label | Description                               |
|----------------------------------|---------|-------|-------------------------------------------|
| `metrics.reactions.origin.likes` | `likes` | Likes | Total "like" reactions on this blog post. |

### TikTok

All metrics fields available on TikTok posts.

| Field                            | Aliases                       | Label     | Description                                                                                                                                                                                       |
|----------------------------------|-------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.total`    | `shares`                      | Shares    | Total shares of this TikTok post within TikTok.                                                                                                                                                   |
| `metrics.threads.origin.total`   | `comments`<br/>`replies`<br/> | Comments  | Total replies to this TikTok post within TikTok, including [transitive replies](#transitive-replies).                                                                                             |
| `metrics.reactions.origin.likes` | `likes`                       | Likes     | Total "like" reactions on this TikTok post within TikTok.                                                                                                                                         |
| `metrics.reactions.origin.total` | `reactions`                   | Likes     | Total reactions on this TikTok post within TikTok.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                                                                      |
    

### WeChat

All metrics fields available on WeChat posts.

| Field                            | Aliases     | Label     | Description                                                                                                                                    |
|----------------------------------|-------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.reactions.origin.likes` | `likes`     | Likes     | Total "like" reactions on this WeChat post within WeChat.                                                                                      |
| `metrics.reactions.origin.wows`  | `wows`      | Wows      | Total "wow" reactions on this WeChat post within WeChat.                                                                                       |
| `metrics.reactions.origin.total` | `reactions` | Reactions | Total reactions on this WeChat post within WeChat.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields.                   |

### NaverCafe

All metrics fields available on NaverCafe posts.

| Field                            | Aliases                       | Label     | Description                                                                                                                        |
|----------------------------------|-------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.reactions.origin.likes` | `likes`                       | Likes     | Total "like" reactions on this NaverCafe post within NaverCafe.                                                                    |
| `metrics.reactions.origin.wows`  | `wows`                        | Wows      | Total "wow" reactions on this NaverCafe post within NaverCafe.                                                                     |
| `metrics.reactions.origin.total` | `reactions`                   | Reactions | Total reactions on this NaverCafe post within NaverCafe.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |
| `metrics.threads.origin.total`   | `comments`<br/>`replies`<br/> | Replies   | Total comment count on this NaverCafe <br/>post <br/>within <br/>NaverCafe.<br/>                                                   |

### Youtube

All metrics fields available on Youtube videos.

| Field                            | Aliases     | Label     | Description                                                                                                             |
|----------------------------------|-------------|-----------|-------------------------------------------------------------------------------------------------------------------------|
| `metrics.reactions.origin.likes` | `likes`     | `likes`   | Total likes of this video within Youtube.                                                                               |
| `metrics.reactions.origin.total` | `reactions` | `likes`   | Total reactions on this video within Youtube.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |
| `metrics.threads.origin.total`   | `threads`   | `threads` | Total replies to this video within Youtube.<br/><br>This is the sum of all other `metrics.threads.origin.*` fields.     |
| `metrics.views.origin.total`     | `views`     | `views`   | Total views of this video within Youtube.<br/><br>This is the sum of all other `metrics.views.origin.*` fields.         |

### X/Twitter

All metrics fields available on X/Twitter Posts.

| Field                                                                           | Aliases                       | Label     | Description                                                                                                                        |
|---------------------------------------------------------------------------------|-------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.shares.origin.retweets`<br/>~~`enrichments.socialScores.tw_retweets`~~ | `retweets`<br/>               | Reposts   | Total reposts of this X/Twitter post within X/Twitter.                                                                             |
| `metrics.shares.origin.quotes`<br/>~~`enrichments.socialScores.tw_retweets`~~   | `quotes`<br/>                 | Quotes    | Total quotes of this X/Twitter post within X/Twitter.                                                                              |
| `metrics.shares.origin.total`<br/>~~`enrichments.socialScores.tw_retweets`~~    | `shares`<br/>                 | Shares    | Total shares (reposts + quotes) of this X/Twitter post within X/Twitter.                                                           |   
| `metrics.shares.editorial.total`                                                | `shares`<br/>                 | Shares    | Total shares of this X/Twitter post on news articles.                                                                              |   
| `metrics.threads.origin.total`<br/>~~`enrichments.socialScores.tw_replies`~~    | `comments`<br/>`replies`<br/> | Replies   | Total replies to this X/Twitter post within X/Twitter, including [transitive replies](#transitive-replies).                        |
| `metrics.reactions.origin.bookmarks`                                            | `bookmarks`                   | Bookmarks | Total "bookmark" reactions of this X/Twitter post within X/Twitter.                                                                |
| `metrics.reactions.origin.likes`<br/>~~`enrichments.socialScores.tw_likes`~~    | `likes`                       | Likes     | Total "like" reactions on this X/Twitter post within X/Twitter.                                                                    |
| `metrics.reactions.origin.total`                                                | `reactions`                   | Likes     | Total reactions on this X/Twitter post within X/Twitter.<br/><br>This is the sum of all other `metrics.reactions.origin.*` fields. |

!!! warning "Important"

    `metrics.reactions.origin.bookmarks` are now included in `metrics.reactions.origin.total` sum. This will be effective from mid November 2023. The previous data will not be corrected by backfills.
