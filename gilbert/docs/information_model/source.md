# Source

Fields relating to the source that produced a document, for example a news paper or forum.

If the field has an alias, it is written in **bold**.

### Fields

| Field Name                                                                                                               | Description                                                                                                                                                                                                                 | Filter Type               | Field Type           | Owner                          |
|--------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|----------------------|--------------------------------|
| externalId                                                                                                               | ID used by source system. Only for twitter/gnip at the moment. Format: id:twitter.com:1123860451492794368                                                                                                                   | Exact match               | String               | Shared (Source ingestion team) |
| metaData.provider.type<br><br>*provider*                                                                                 | Which provider through which the document was obtained. The provider can be a crawler operated by Meltwater or a data aggregator. See [Provider Type](#provider-type).                                                      | Exact match               | Enum (String)        | Huntsman                       |
| metaData.provider.specifier<br><br>*providerSpecifier*                                                                   | The specific fetcher or mechanism used to obtain the document, for example "shakespeare:dow-jones-fetcher" for the Dow Jones Fetcher owned by team Shakespeare.                                                             | Exact match               | String               | Shared (Source ingestion team) |
| metaData.source.allowPdf                                                                                                 | True if the corresponding source can produce PDF content.                                                                                                                                                                   | Exact match               | Boolean              | Gecko                          |
| metaData.source.authority.newsguard                                                                                      | **Deprecated:** Use the *metaData.source.authority.newsguardScore* field.                                                                                                                                                   | Exact match               | Integer              | Gecko                          |
| metaData.source.authority.newsguardScore                                                                                 | Newsguard trust rating score for news sites                                                                                                                                                                                 | Exact match               | Float                | Gecko                          |
| metaData.source.contentLocation                                                                                          | Indicates if the content is hosted by Meltwater or accessible through a public url                                                                                                                                          | Not possible to search in | Enum(String)         | Huntsman                       |
| metaData.source.copyrightOwners                                                                                          | List of copyright owners (agencies) of the source See [Copyright Owner](#copyright-owner)                                                                                                                                   | Exact match               | Array<Enum (String)> | Gecko                          |
| metaData.disambiguatedSourceId                                                                                           | Meltwater Influencers ID (Kermit) of this source.                                                                                                                                                                           | Exact match               | String               | Hedgehog                       |
| metaData.source.id<br><br>**sourceid** **pageId**// *sourceId*                                                           | Unique ID of this source.                                                                                                                                                                                                   | Exact match               | String               | Gecko?                         |
| metaData.source.informationType<br><br>*informationType*<br><br>**infoType, infotype, informationType, informationtype** | Broad categorization of the source of the document. See [Information Type](#information-type).                                                                                                                              | Exact match               | Enum (String)        | Information Model Guild        |
| metaData.source.language                                                                                                 | **Deprecated:** Use the *enrichments.languageCode* field. Contains a plain text description of the language that the News source usually publish content in, only available on documents from the Meltwater news documents. | Exact match               | String               | Gecko                          |
| metaData.source.languageCode                                                                                             | Contains bcp47 compatible code of the language that the News source usually publish content in, only available on documents from the Meltwater news documents.                                                              | Exact match               | String               | Gecko                          |
| metaData.source.location.city                                                                                            | The geographical location (city) of the intended audience of this source medium                                                                                                                                             | To be added               | To be added          | Gecko                          |
| metaData.source.location.country                                                                                         | The geographical location (country) of the intended audience of this source medium                                                                                                                                          | To be added               | To be added          | Gecko                          |
| metaData.source.location.region                                                                                          | The geographical location (region) of the intended audience of this source medium                                                                                                                                           | To be added               | To be added          | Gecko                          |
| metaData.source.mediaType                                                                                                | **Deprecated:** Use the *metaData.mediaType* field. See [Media Type](document.md#media-type).                                                                                                                               | Exact match               | Enum (String)        | Information Model Guild        |
| metaData.source.name<br><br>*source*                                                                                     | Name of the source of this document.                                                                                                                                                                                        | Text search               | String               | Gecko?                         |
| metaData.source.newsFocus                                                                                                | News focus provides source visibility information. See [News Focus](#news-focus)                                                                                                                                            | Exact match               | Enum (String)        | Gecko                          |
| metaData.source.outletTypes                                                                                              | Outlet type of the source. See [Outlet Type](#outlet-type)                                                                                                                                                                  | Exact match               | Enum (String)        | Gecko                          |
| metaData.source.paywall                                                                                                  | Paywall provides the paywall type of the source [Paywall](#paywall)                                                                                                                                                         | Exact match               | Enum (String)        | Gecko                          |
| metaData.source.pricing                                                                                                  | The pricing model of content from this source. See [Pricing](#pricing).                                                                                                                                                     | Exact match               | Enum (String)        | Shared (Source ingestion team) |
| metaData.source.publisherId                                                                                              | Id of the source's publisher                                                                                                                                                                                                | Exact match               | String               | Gecko                          |
| metaData.source.socialOriginType<br><br>**socialType, socialtype**                                                       | More specific categorization of the source of the document. See [Social Origin Type](#social-origin-type).                                                                                                                  | Exact match               | Enum (String)        | Information Model Guild        |
| metaData.source.url<br><br>*sourceUrl*                                                                                   | Root URL of the website or other source of this document.                                                                                                                                                                   | Exact match               | String               | Information Model Guild        |

### Provider Type

| metaData.provider.type  | Description                                                                    |
|-------------------------|--------------------------------------------------------------------------------|
| added_content           | Content by customers to their own private index.                               |
| ap                      | News articles coming from Associated Press.                                    |
| belga                   | Belgium’s leading news agency and media monitoring company                     |
| bloomberg               | Documents coming from Bloomberg (fetcher)                                      |
| bluesky                 | Documents coming from Bluesky                                                  |
| boardreader             | Reviews, posts and comments coming from Boardreader.                           |
| cbcnews                 | cbc content                                                                    |
| cdmos                   | Documents coming from CDMOS, an Indonesian print provider                      |
| cfc                     | Documents coming from French premium content partner                           |
| datasift                | Blog posts and comments coming from DataSift.                                  |
| discord                 | Documents coming from Discord API                                              |
| dk_premium              | Documents from Danish Premium integration (print and online content partners)  |
| dowjones                | Factive print, online news, and radio transcripts coming from Factiva API      |
| epress                  | ePress provides Finnish print content                                          |
| explicar                | Documents coming from Explicar (Indonesian print partner)                      |
| faz                     | FAZ print and premium news coming from FAZ fetcher                             |
| fd                      | Het Financieele Dagblad - Dutch newspaper for finance and economics            |
| ft                      | Financial Times                                                                |
| gnip                    | Tweets coming from Gnip PowerTrack subscriptions.                              |
| gsdata                  | WECHAT & DOUYIN provider                                                       |
| infomart_premium_online | Online news coming from various Canadian publishers                            |
| infomart_premium_print  | Print news coming from various Canadian publishers                             |
| instagram               | Content from Instagram social media platform                                   |
| ir                      | Content coming from IceRocket RSS crawler                                      |
| kakaotalk               | Content   coming from Kakaotalk                                                |
| kinetiq                 | Broadcast content coming from Kinetiq                                          |
| klarity                 | Chinese social content coming from Klarity.                                    |
| knewin                  | Knewin - Premium Print provider                                                |
| lexisnexis              | Lexis Nexis - Premium Content Provider                                         |
| linevoom                | LineVoom - Media content for LINE messaging platform                           |
| linkedin                | LinkedIn                                                                       |
| linkfluence             | In-house crawling from Linkfluence                                             |
| mcna                    | Manitoba Community Newspapers Association - Publisher of Canadian news         |
| mediaconnect            | Documents coming from Mediaconnect                                             |
| mediaconnect_aus_print  | Australian Print provided by Mediaconnect                                      |
| mediaconnect_nz_print   | New Zealand Print provided by Mediaconnect                                     |
| mediameter              | Documents coming from Media Meter                                              |
| mediaobserver           | Documents coming from Media Observer                                           |
| meedius                 | Documents coming from Meedius                                                  |
| meta                    | Meta (formerly Facebook), provider of Threads social content                   |
| moodys                  | Moody's NewsEdge content                                                       |
| mw                      | News documents coming from Meltwater crawlers.                                 |
| nine                    | Documents coming from Nine, Australian Publisher (especially of AFR)           |
| nla                     | Collecting Society for UK Newspapers, provides access to print and online      |
| nlaeclips               | NLA Eclips documents fetched from NLA                                          |
| nlaftp                  | NLA content fetched from ftp                                                   |
| nltd                    |                                                                                |
| nytimes                 | Content received directly from The New York Times                              |
| omgili                  | Documents coming from OMGILI.                                                  |
| pear                    | South African content provider                                                 |
| pinterest               | Documents coming from Pinterest social media platform                          |
| pmg                     | Presse Monitor GmbH - DACH content provider                                    |
| pmnews                  |                                                                                |
| postmedia_premium_online | Postmedia is a Canadian content provider                                      |
| postmedia_premium_print | Postmedia is a Canadian content provider                                       |
| reddit                  | Documents coming from Reddit social media platform                             |
| retriever               | Norwegian premium content provider                                             |
| satismeter              | Satismeter customer feedback and surveys                                       |
| schibsted               | Nordic premium content partner                                                 |
| scmp                    | South China Morning Post - Hong Kong Newspaper                                 |
| scmponline              |  South China Morning Post - Hong Kong Newspaper                                |
| sinamidu                | Provider of Chinese social content (Little Red Book)                           |
| snapchat                | Content from social media platform Snapchat                                    |
| socialconnections       | Content coming from Social Connections / Engage                                |
| socialgist              | Content coming from Socialgist                                                 |
| sph                     | Content coming from Singapore Press Holdings (Straits Times)                   |
| spinn3r                 | Tweets coming from Spinn3r. Only available on historic content.                |
| swedish_premium_national | Swedish premium (Bonnier) crawled content with national interest              |
| swedish_premium_regional | Swedish premium (Bonnier) crawled content with regional interest              |
| swna                    | Saskatchewan Weekly Newspapers Association - Canadian content provider         |
| sz                      | Content from Südwestdeutsche Medien Holding (SWMH), especially SZ              |
| tiktok                  | Content from TikTok                                                            |
| torontostar             | Toronto Star Newspapers Ltd., Canadian publisher of local newspapers           |
| tribune                 | Content from Tribune Publishing Company (especially Chicago Tribune)           |
| tveyes                  | TV, Radio, and Podcast content coming from content provider TVEyes             |
| twitch                  | Content from streaming platform Twitch                                         |
| twitter                 | Content coming from X (formerly Twitter)                                       |
| unknown                 |                                                                                |
| vk                      | Content from Russian social media platform VK                                  |
| washingtonpost          | Content from Washington Post                                                   |
| webz                    | Dark web/Alternative Social provider for tor,i2P,telegram,discord,openweb      |
| weibo                   | Content from Chinese social media platform Sina Weibo                          |



### Information Type
Broad categorization of the source of the document.

| metaData.source.informationType | Description                                                   |
|---------------------------------|---------------------------------------------------------------|
| broadcast                       | Video and audio streams, TV, radio and other broadcast media. |
| news                            | Journalistic content.                                         |
| social                          | Content produced by public.                                   |
| tender                          | Tenders                                                       |

### Pricing
The *metaData.source.pricing* field contains pricing information about the document.

| metaData.source.pricing | Description |
|-------------------------|-------------|
| free                    ||
| paid_premium            ||
| premium                 ||
| subscription            ||

### Social Origin Type
More specific categorization of the source of the document.

| metaData.source.socialOriginType | Description                                                               |
|----------------------------------|---------------------------------------------------------------------------|
| facebook                         | Content from Facebook.                                                    |
| instagram                        | Content from Instagram.                                                   |
| reddit                           | Content from Reddit.                                                      |
| social_blogs                     | Blog posts from various feeds and crawlers, e.g. Wordpress and IceRocket. |
| social_reviews                   | Reviews from various feeds, e.g. Boardreader.                             |
| social_message_boards            | Forum posts and comments from various feeds, e.g. OMGILI.                 |
| social_comments                  | Comments from various feeds, e.g. Disqus, IntenseDebate and Wordpress.    |
| twitter                          | Content from Twitter.                                                     |
| youtube                          | Content from YouTube.                                                     |
| wechat                           | Content from WeChat                                                       |
| sina_weibo                       | Content from Sina Weibo                                                   |
| linkedin                         | Content from Linkedin                                                     |
| pinterest                        | Content from Pinterest                                                    |
| twitch                           | Content from Twitch                                                       |
| tiktok                           | Content from Tiktok                                                       |
| douyin                           | Content from Douyin                                                       |
| little_red_book                  | Content from little red book                                              |
| google_reviews                   | Content from Google My Business reviews                                   |
| threads                          | Content from Meta Threads                                                 |
| kakaotalk                        | Content from Kakaotalk                                                    |
| linevoom                         | Content from Linevoom                                                     |
| podcasts                         | Podasts from TVEyes                                                       |
| snapchat                         | Content from Snapchat                                                     |
| bluesky                          | Content from Bluesky                                                      |

### News Focus
The *metaData.source.newsFocus* field contains source visibility information.

| metaData.source.newsFocus | Description        |
|---------------------------|--------------------|
| international             ||
| national                  ||
| local                     ||
| regional                  ||
| unknown                   | data not available |

### Outlet Type
The *metaData.source.outletTypes* field contains type information from the source.

| metaData.source.outletTypes | Description        |
|-----------------------------|--------------------|
| advertising_paper           ||
| aggregator                  ||
| blog                        ||
| government                  ||
| job_portal                  ||
| magazine                    ||
| market_research_reports     ||
| newspaper                   ||
| news_agency                 ||
| online                      ||
| other                       ||
| press_releases              ||
| radio                       ||
| stock_market_news           ||
| television                  ||
| trade_publication           ||
| unknown                     | data not available |


A new field has been added to narrow these categories and reduce noise `enrichments.media.news.categories`, see [Derived news outlet type](../document#derived-news-outlet-type)

### Copyright Owner
The *metaData.source.copyrightOwners* field contains the list of abbreviated names of the copyright agencies.

| metaData.source.copyrightOwners | Description                                                                                                    |
|---------------------------------|----------------------------------------------------------------------------------------------------------------|
| CAL                             | Copyright Agency in Australia.                                                                                 |
| CFC                             | Centre Francais D'Exploitation Du Droit De Copie. Responsible for management of reproduction rights in France. |
| CLA                             | Copyright Licensing Agency in UK.                                                                              |
| NLA                             | Newspaper Licensing Agency in UK.                                                                              |
| NLI                             | Newspaper Licensing Ireland, manage copyright interests Irish Publishers.                                      |
| MBL                             | Mediebedriftenes Klareringstjeneste AS (Norway)                                                                |
| PMCA                            | Print Media Copyright Agency New Zeland                                                                        |
| CAL-NLA                         | NLA repertoire that CAL is authorised to license in Australia.                                                 |
| CAL-CFC                         | CFC repertoire that CAL is authorised to license in Australia.                                                 |
| Dow_Jones                       | The Dow Jones Partnership gives our clients full-text options to key sources that are behind paywalls.         |
| AFR                             | Australian Financial Review                                                                                    |
| The_Australian                  | The Australian                                                                                                 |
| DK                              | Danish Publishers                                                                                              |
| MCA                             | Copyright Licensing Agency in New Zealand                                                                      |
| CFC-PRINT                       | Centre Francais D'Exploitation Du Droit De Copie. Responsible for management of reproduction rights in France. |
| Explicar                        | Indonesian print agency                                                                                        |
| Meedius                         | Dutch print content

### Format
The *metaData.source.format* field contains the format of the original document.

| metaData.source.format | Description                                                                                                          |
|------------------------|----------------------------------------------------------------------------------------------------------------------|
| online                 | The original article is being shown on a website. This is the default value. If this field is not set, it is online. |
| print                  | The original article is being shown on paper.                                                                        |
| app                    | The original article is being shown on mobile.                                                                       |

### Paywall
The *metaData.source.paywall* field contains the paywall type.

| metaData.source.paywall | Description                                       |
|-------------------------|---------------------------------------------------|
| partial                 | Partial paywall type. No paywall URL is generated.|
| full                    | Full paywall type. Paywall URL is generated.      |
