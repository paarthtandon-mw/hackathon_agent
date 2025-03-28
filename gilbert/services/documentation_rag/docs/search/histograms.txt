# Histograms

Histograms means breaking apart the matched documents into multiple *buckets* based on steps and ranges of a field, and counting or applying child aggregations onto the documents that fall in each bucket. For example a histogram over document publish time, and counting volume and unique influencers per day.

## Date Histogram

Use the date histogram view request if you want the results bucketed by time. For example to count how many documents were published per day. Date histograms also accepts sub-view requests which are aggregated for each time interval, for example to perform other statistical aggregations for each time interval. Note: the order of the buckets in the response is not guaranteed to be sorted by date.

For result buckets where no results are found, a bucket is still created, with a count of zero. However, this only works on top-level date histograms. For sub-view date histograms, no bucket element is returned for time periods where there are no results.

**Parameters**:

* **dateField**: The date field to base the counts on.
* **granularity** (default *day*): Specifies how large chunks one wants for the periods. Can be either *SECOND*, *MINUTE*, *HOUR*, *DAY*, *WEEK* or *MONTH*.
* **interval** (default *1*): The number of time units. For example specifying 2 as interval and day as granularity would mean that each interval is 2 days. Only 1 is valid when using month granularity.
* **timeZone** (default: *UTC*): The time zone to base the periods on. This is important since the day changes at different hours in different time zones. The format can be either be "UTC", an offset in hours and minutes from UTC or the long Canonical ID (e.g. "Asia/Brunei")
* **subViewRequests**: A mapping of strings to nested analytics aggregations. See [Sub view requests](../faceting#sub-view-requests) for which aggregations that can be used as sub view requests.
* **nestedPath**: If specified, evaluate the date histogram in a nested context. Never really makes sense at the moment, since there are no indexed nested date fields.

```json
// Counting volume of documents per day with a -8 hour timezone offset
{
  "type": "dateHistogram",
  "dateField": "body.publishDate.date",
  "timeZone": "-08:00",
  "granularity": "DAY"
}

// Trending the volume by media type and counting unique influencers
{
  "type": "dateHistogram",
  "dateField": "body.publishDate.date",
  "timeZone": "UTC",
  "granularity": "DAY",
  "subViewRequests": {
    "byMediaType": {
      "type": "termsFacet",
      "termsField": "metaData.mediaType",
      "subViewRequests": {
        "uniqueInfluencers": {
          "type": "cardinality",
          "field": "metaData.authors.authorInfo.externalId"
        }
      }
    }
  }
}
```

## Date Terms Histogram

!!! warning "**Deprecation Notice** Use a [Date Histogram](#date-histogram) view with a [Terms Facet](faceting.md#terms-facet) sub view request instead."

Returns the count of the top distinct values of the specified fields bucket by time. 

**Parameters**:

* **dateField**: The date field to base the counts on.
* **granularity** (default *day*): Specifies how large chunks one wants for the periods. Can be either *SECOND*, *MINUTE*, *HOUR*, *DAY*, *WEEK* or *MONTH*.
* **timeZone** (default: *UTC*): The time zone to base the periods on. This is important since the day changes at different hours in different time zones. The format can be either be "UTC", an offset in hours and minutes from UTC or the long Canonical ID (e.g. "Asia/Brunei")
* **termsField**: The field to facet on.
* **size** (default *10*): The number of values to get counts for.


## Terms Histogram

!!! warning "**Deprecation Notice** Use a [Terms Facet](faceting.md#terms-facet) with another Terms Facet sub view request instead."

Returns the top values of the sub terms field bucketed by the top values of the main terms field.

**Parameters**:

- **mainTermsField**: The main field to facet on.
- **mainTermsCount** (default *10*): The number of distinct top values of main terms field.
- **subTermsField**: The field to get top values for per each main field value.
- **subTermsCount**: The number of distinct top values of sube terms field. 
