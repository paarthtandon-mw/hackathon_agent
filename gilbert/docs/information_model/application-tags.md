# Application Tags


## Engage
| metaData.applicationTags                                            | Description                                                                                                                                                             |
|---------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| connectionsCredential=\{int\}                                       | Private social connection ID                                                                                                                                            |
| connectionsPollId=\{guid\}                                          | Unique ID of the poll cycle when the document was last updated.                                                                                                         |
| li_liked_by_user=\{bool\}                                           | Indicates if the document is liked by the social profile associated with its social connection.<br><br>Applies to LinkedIn documents.                                   |
| userLikes=\{bool\}                                                  | Indicates if the document is liked by the social profile associated with its social connection. <br><br>Applies to Facebook documents.                                  |
| conversations:searchId=\{searchId\}:assign=\{userId\}:\{timestamp\} | Indicates the user assigned to the document in MI Engage Conversations. Assignments are based on a User and a Saved Search.                                             |
| conversations:\{companyId\}:status=\{todo,complete\}                | Indicates the status of the document in MI Engage Conversations. If not present document is in 'todo' status.                                                           |
| isHidden=\{bool\}                                                   | Indicates if the document is hidden on the social platform by the social profile associated with its social connection<br><br>Applies to Facebook, Instagram documents. |



## Helios - Custom applications
| metaData.applicationTags               | Description                                                                                                                                                                       |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| helios-macquarie:faculty=\{string\}    | Custom application tag used for macquarie-university-dashboard to indicate the faculty in the article. Used by https://github.com/meltwater/macquarie-university-dashboard-bff    |
| helios-macquarie:writer=\{string\}     | Custom application tag used for macquarie-university-dashboard to indicate the writer of the article. Used by https://github.com/meltwater/macquarie-university-dashboard-bff     |
| helios-macquarie:researcher=\{string\} | Custom application tag used for macquarie-university-dashboard to indicate the researcher of the article. Used by https://github.com/meltwater/macquarie-university-dashboard-bff |


## Inception - Custom applications
| metaData.applicationTags               | Description                                                                                                                                                                                                          |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| public-youtube:engagements=\{bool\}   | A custom application tag indicating that the document’s retention period is extended to 15 months, overriding the default 30-day retention for YouTube documents. Set by https://github.com/meltwater/unified-fetcher |


## Other
|                         | Description                                                                                                                                                |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| restriction:share=false | Document can't be shared externally, for example included in Newsfeeds.                                                                                    |
| display:hosted=true     | Document is treated as "hosted." By default, hosted documents open in-app, cannot be shared, cannot be translated, are are excluded from certain searches. |
| \_hiddenDocument\_      | Document is excluded from searches.                                                                                                                        |

