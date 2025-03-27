# Predefined Sorting Scripts

With Search V2 API, you can benefit from predefined sorting scripts that enable common sorting logic to be accessed from
one central location.

Here is the list of sorting scripts we support:

| Name        | Value       | Example                                                                                  |
|-------------|-------------|------------------------------------------------------------------------------------------|
| Engagement  | engagement  | `... "sortDirectives": [ {  "scriptName": "engagement",  "sortOrder": "DESC" },  ...  ]` |
| Reach       | reach       | `... "sortDirectives": [ {  "scriptName": "reach",  "sortOrder": "DESC" }, 	    ...  ]`  |
| Social Echo | social-echo | `... "sortDirectives": [ {  "scriptName": "social-echo",  "sortOrder": "DESC" }, ...  ]` |
| Relevance   | relevance   | `... "sortDirectives": [ {  "scriptName": "relevance",  "sortOrder": "DESC" },   ...  ]` |
| Prominence  | prominence  | `... "sortDirectives": [ {  "scriptName": "prominence",  "sortOrder": "DESC" },  ...  ]` |
| Views       | views       | `... "sortDirectives": [ {  "scriptName": "views",  "sortOrder": "DESC" },  ...  ]`      |

**Note:** To maintain consistent document order, it's crucial to include a fallback sort directive in case the sorting
score is unavailable or the same between documents. Such as the following:

```
[
   {
        "scriptName": "engagement",
        "sortOrder": "DESC"
   },
   {
        "sortField": "body.publishDate.date",
        "sortOrder": "DESC"
    }
]
``` 