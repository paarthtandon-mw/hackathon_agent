# Adding a new data source

Adding a new data source to the Meltwater dataset is a joint collaboration between teams. The process is divided in three steps:

1. Crawling (fetching documents on the Internet) - Teams Hedgehog, Huntsman, Wrapidity
2. [Enrichment](/docs/default/component/nlp-api-docs) (adding useful metadata to documents) - Teams Platypus, Karma
3. Indexing (adding the data to the search cluster, to make it useable by Meltwater apps) - Team Horace

The remainder of this document will outline important aspects to take into consideration when **Indexing**.

## Preparation
As all data in the search cluster are stored in a [common format](search-fields), one needs to consider which fields will be used when new documents are indexed. The common format is rarely changed as it impacts both new and existing data. Reach out to [@horace](https://meltwater.slack.com/archives/CABNB5AJY) in Slack or at [horace@meltwater.com](mailto:horace@meltwater.com) to get our help and to discuss your data source needs. We are particularly interested in the use cases of the new data source and its quantity/volume.

## Document the data source
In the process of finalising indexing to production, the data source should be documented:

☐ Add the new source to [Sources](index.md), filling in all columns.

- The retention column should also specify when a source went live
- Add a sub-page to [Sources](index.md) if more detailed source specific information is required.

☐ Add the new source to [Source-Field Mapping](../source-field-mapping.md), describing which fields are used in the new source.

☐ If new fields were added to the common format, add them in the respective sub-section of [Fields](../fields/index.md).

☐ Throughout the lifetime of the data feed, maintain above-mentioned resources. Important events and decisions that affect the data and its quality - e.g., outages, missing enrichments, if data fields are used/ignored or have a modified meaning to the end-user applications. - should be listed in the [Sources](index.md) subsection tied to the new source.

Note: these guidelines for documenting sources are new as of May 2020, so sources added prior to this do not have all this information.

## Cost estimate for new data source (as of January 2021)

Assumptions
> - Two replicas = three copies of all data
> - Each node is filled up to 85%
> - Instance type is i3.4xlarge
> - Overhead and On Demand Price Discounts cancel each other out, both are roughly 10%

| Type         | Description                                                                                            | Storage size / million documents | Cost / million documents and month |
|--------------|--------------------------------------------------------------------------------------------------------|----------------------------------|------------------------------------|
| Twitter      | Low amount of text but lots of metadata and enrichment<br><br>Data is removed after 15 months          | 8 GiB                            | $2800                              |
| News         | Lots of text and medium amount of metadata and enrichment<br><br>Data is stored indefinitely           | 60 GiB                           | $21000                             |
| Other Social | Medium amount of text and low amount of metadata and enrichment<br><br>Data is removed after 15 months | 9.5GiB                           | $3325                              |



## Cost estimate for backfilling data (as of January 2021)

On top of the actual storage cost is a one time cost when backfilling new data. This cost comes from:
* Increased network traffic - Increasing/decreasing the size of documents/shards triggers more relocations in the cluster
* Processing cost of parsing json - More CPU is needed to process and transform json documents in the ingestion pipeline

| Type | Description                                               | Cost / million documents |
|------|-----------------------------------------------------------|--------------------------|
| Any  | The cost is an average for social and editorial documents | $0.5                     |

