# The Search API V2

This API delivers legally compliant search content. It builds on the existing functionality of  [Search API V1](/docs/default/API/search-api-v1/), but with some augmentations to the request language.

It aims to replicate the full functionality of the Search API V1 but also provide some helpful enhancements to translate the media intelligence domain of companies and saved searches into runes queries and legally compliant results.

## Why should I use this instead of the Search API V1?

The content delivered by this API is processed to fulfil any legal or contractual requirements for your use case.

## Already familiar with the Search API V1?
Check our [Migration guide](v2-search-migrating-from-v1.md) to see what's different in the Search API V2.

### Examples

#### Showing documents to an end-user

Documents that we show to an end-user have to undergo scrutiny to make sure they adhere to Meltwaters agreements with content providers. Some documents may need to be redacted due to geographical restrictions, others may need to be reported as viewed by an end-user. By default, all documents returned by this API will be legally compliant.

#### Reporting compliance

Meltwater has contractual agreements with many different content providers. For each content provider we have different requirements on reporting — for some we report each document consumed both for internal and external use, for others, we only report documents consumed by external users.

This API is fully compliant with Meltwater's reporting requirements, ensuring all documents consumed are reported to their corresponding content providers in a compliant manner.

## How does this compare to Keystone?

You may or may not have heard of [Keystone](https://github.com/meltwater/keystone), an API for returning documents from the Search API. Keystone solves a similar problem, it returns documents that are legally compliant from both a reporting and regional content restriction perspective.

Keystone was built a long time ago when Meltwater was a very different product. Keystone's API was not built with products like Explore or Engage in mind. It can be hard to adapt search requests and retrieve search results for these newer products, which are not tied to specific information types (e.g. news vs. social) and are more ad-hoc in manner.

This API aims to fill the shortcomings of Keystone by exposing the full functionality of the [Search API](/catalog/default/api/search-api-v1/definition#/Search%20API/searchUsingPOST) while ensuring the results you receive are legally compliant.

### Migrating from Keystone?

If you're using Keystone to retrieve search results, we've put together a guide outlining how some of Keystone's optional parameters map to Search API Requests:
[Migrating from Keystone to Search API V2](https://docs.google.com/document/d/1qssusf-NFfUJzkMqXOM9aZ48Y_Zcm0veT8OabXac4Fo)

## Maintainer

This API is maintained by Team Platypus. To get in touch with us, use our [Slack channel](https://meltwater.slack.com/archives/CAJKZ9RDE), or [send us an email](mailto:platypus@meltwater.com).
