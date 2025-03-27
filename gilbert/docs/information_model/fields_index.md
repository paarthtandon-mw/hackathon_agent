# Fields

The **General Tenant** holds a repository of all of Meltwater's historical content. It uses a document model called the **General Schema**, listed below and detailed in the following pages.

This dataset is exposed through the [Search API](https://backstage.meltwater.io/docs/default/api/search-api-v2), [Export API](https://backstage.meltwater.io/docs/default/api/export-api-v2) and [Document API](https://backstage.meltwater.io/docs/default/api/consumer-ready-document-api).

## General Schema

Documents consist of many fields, each logically comprising several domain objects.

* [Document](document.md) fields make reference to elements in the original document itself, such as title, body, NLP enrichments and document meta-data.
* [Location](location.md) fields store the location at which the document was written.
* [Author](author.md) fields store information about the author of the document, e.g., a journalist or social media influencer.
* [Audience](audience.md) fields store metrics about the audience size for the document.
* [Engagement](engagement.md) fields store metrics about the engagement level for the document.
* [Source](source.md) fields store info about the source of origin of the document, e.g., a news paper or forum.
* [System](system.md) fields store system meta-data about the document, such as timestamps and visibility status.
* [Application Tags](application-tags.md) are used to label documents with application specific information.

## Aliases

[Aliases](aliases.md) are 'short names' for certain fields in the information model which are valid to use in boolean queries.

## Search Operators

Different fields will support different categories of [Runes queries](/docs/default/api/search-api-v1/queries/), as detailed below. Some fields do not support any operators, meaning they can't be used in filters but only retrieved in output documents.

| Filter Type | Description                                                                                                                                                                                                                                                                     | Query & Analytics Support                                                                                                                                                                                                                         | Field Type                    |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Text search | Full text search that matches individual keywords and phrases found in a text field. The match can be either *case insensitive* (default) or *case sensitive* by setting the [flags](/docs/default/api/search-api-v1/queries/field-queries/#word-query) parameter on the query. | [Word](/docs/default/api/search-api-v1/queries/field-queries/#word-query), [Wildcard](/docs/default/api/search-api-v1/queries/field-queries/#wildcard-query) and [Filter Facet](/docs/default/api/search-api-v1/analytics/faceting/#filter-facet) | String fields                 |
| Exact match | Matching a specific field value exactly. This matches the whole field value exactly, and in a *case sensitive* manner.                                                                                                                                                          | [Term](/docs/default/api/search-api-v1/queries/field-queries/#term-query) and [Terms Facet](/docs/default/api/search-api-v1/analytics/faceting/#terms-facet).                                                                                     | String fields, numeric fields |
| Range match | Matching a numeric range of field values.                                                                                                                                                                                                                                       | [Range](/docs/default/api/search-api-v1/queries/field-queries/#range-query). Date fields support [Date Histograms](/docs/default/api/search-api-v1/analytics/histograms/#date-histogram).                                                         | Numeric fields                |

