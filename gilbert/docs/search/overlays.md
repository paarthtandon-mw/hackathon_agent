# Private documents and modifications

Both the Search and Export API's supports querying customer private documents and/or modifications (so called *overlays*). Use the *overlayGroups* parameter to supply a list of customer ID's and other namespaces to consider in the search request. The Alerting API on the other hand only supports subscribing to customer private documents, not overlays.

```json
// Include private documents and modifications for "some-customer-id1" into export result
{
  "query": { 
    // ... some query
  },
  "overlayGroups": ["some-customer-id", "some-private-namespace"]
}

```



## Scopes

The **scope** parameter accepts a list of document states to search, and limits the search query to only those states. It requires the **overlayGroups** parameter to be provided. Possible scopes are

* **modified**: Query documents that have been modified/overlaid in the context of the specified **overlayGroups**.
* **private**: Query documents that are private to the specified **overlayGroups**.

```json
// Query only for documents that have been modified by some-customer-id
{
  "query": {
    // ... some query
  },
  "overlayGroups": ["some-customer-id"],
  "scope": ["modified"]
}

// Query only for documents are private to some-customer-id
{
  "query": {
    // ... some query
  },
  "overlayGroups": ["some-customer-id"],
  "scope": ["private"]
}

// Query for documents are private or have been modified by some-customer-id 
{
  "query": {
    // ... some query
  },
  "overlayGroups": ["some-customer-id"],
  "scope": ["modified", "private"]
}

```

