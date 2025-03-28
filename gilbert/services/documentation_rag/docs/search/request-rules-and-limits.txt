# Search request rules

* **Date Range validation**: The total range of publish date cannot exceed 1 year, with the exception of [archive search](docs/default/component/ir-api-access/api_access/search-use-cases/#i-want-to-search-for-longer-than-year).

* **Near validation**: Sub queries to near queries must refer to the same field
* **Nested Field validation**:
  * Queries on nested fields must be within nested queries* 
  * Queries on nested fields are not supported within Filters


# Search request limits

[Current search request limits](https://github.com/meltwater/horace-k8s/blob/main/applications/search/search-resource-prediction-features.yaml)

In order to guarantee the stability of the search system we have a set of rules to block queries with known instability problems that we evaluate each search request against. Search requests are evaluated against these rules either when calling the [/search/validate endpoint](../api-post-search-validate.md) or before a search is executed in [/search endpoint](../api-post-search.md).

For each of these rules there are two levels, warning and invalid. Warning means that the query has issues but will still be executed. However, searches with warnings might be down prioritized. Invalid means that the query is too bad and will probably not succeed, so those searches are rejected before executed.

The set of rules and the exact limits are ever changing. The most up-to-date description of all the rules and the corresponding limits for warning and invalid can be found [here](https://github.com/meltwater/horace-k8s/blob/master/applications/search/search-resource-prediction.yaml#L90).

For searches that include twitter firehose there are stricter restrictions. This as the amount of documents searched when using twitter firehose are many billions, which is known to cause instability in the cluster. Those rules can also be seen in the link above with a twitter firehose suffix.

## Credit limits

As well as specific limit rules that must be adhered too, there are also limits 
on how much CPU resources can be concurrently consumed by searches by each API consumer.
For more information on search credits please refer to our documentation on [API Limits](https://backstage.meltwater.io/docs/default/domain/information-retrieval/api-access/search-limits).