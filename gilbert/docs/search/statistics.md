# Statistics

The various statistics oriented views perform counts and mathematical calculations over numeric fields and scripts. They can be combined with [Histograms](histograms.md) and [Faceting](faceting.md) to great effect, in order to calculate statistics separately for each bucket.

## Count

Retrieves the total count of documents matching the query. Only makes sense as a top-level aggregation, since the other bucketing aggregations (Date Histogram, Terms Facet) returns counts for each bucket.

```json
// Counting the total number of documents that matched the query
{
  "type": "count"
}
```



## Statistics

Use the statistical view request if you want to receive statistical information about a numeric field or script.

**Parameters**:

* **field**: A numeric field to get statistics for
* **script**: A script for calculating statistics. (Read more about the [Script DSL](../advanced-usage/script-dsl.md))
* **measures** (default *["SUM", "MEAN", "MIN", "MAX", "AVG"]*): What measures to calculate. Supports *SUM*, *MEAN*, *MIN*, *MAX*, *AVG*.
* **nestedPath**: If specified, evaluate the statistics in a nested context. In sub view requests, both parent and statistics views should be on the same nested path for statistic correlations to be made in a nested context. Otherwise the correlations are made at the document level.

```json
// Calculate statistics of article reach
{
  "type": "statistics",
  "field": "enrichments.comscoreUniqueVisitors",
  "measures": ["SUM"]
}

// Calculate an aggregate audience promoter score by applying a script to each document
{
  "type": "statistics",
  "script": "(10 + log(.enrichments.comscoreUniqueVisitors)) * .enrichments.sentiment.numeric",
  "measures": ["MEAN", "MIN", "MAX"]
}
```



## Percentiles

Calculates a set of percentiles over a specified field.

**Parameters**:

* **field**: The field to get percentiles for. Must be a numerical field.
* **percentiles** (default *[1.0, 5.0, 25.0, 50.0, 75.0, 95.0, 99.0]*): An array of string percentiles to calculate.
* **nestedPath**: If specified, evaluate the statistics in a nested context. In sub view requests, both parent and statistics views should be on the same nested path for statistic correlations to be made in a nested context. Otherwise the correlations are made at the document level.

```json
// Calculate percentiles of article reach
{
  "type": "percentiles",
  "field": "enrichments.comscoreUniqueVisitors",
  "percentiles": [25.0, 50.0, 75.0, 95.0]
}
```



## Cardinality

Counts the unique values of a field. For example counting the unique influencers, sources or countries present in a query. 

*Note:* This is an approximate count, the precision and exact value of the result may vary slightly between different queries and requests.

**Parameters**:

* **field**: The field to count the cardinality of.

```json
// Counting unique influencers
{
  "type": "cardinality",
  "field": "metaData.authors.authorInfo.externalId"
}
```


## Date Statistics

!!! warning "**Deprecation Notice** Use a [Date Histogram](histograms.md#date-histogram) view with a [Statistics](#statistics) sub view request instead."

Returns statistics of a field bucketed by time.

**Parameters**:

* **dateField**: The date field to base the counts on.
* **granularity** (default *day*): Specifies how large chunks one wants for the periods. Can be either *SECOND*, *MINUTE*, *HOUR*, *DAY*, *WEEK* or *MONTH*.
* **interval** (default *1*): The number of time units. For example specifying 2 as interval and day as granularity would mean that each interval is 2 days. Only 1 is valid when using month granularity.
* **timeZone** (default: *UTC*): The time zone to base the periods on. This is important since the day changes at different hours in different time zones. The format can be either be "UTC", an offset in hours and minutes from UTC or the long Canonical ID (e.g. "Asia/Brunei")
* **statisticsField**: A numeric field to get statistics for
* **measures**: What measures to calculate. Supports *SUM*, *MEAN*, *MIN*, *MAX*, *AVG*.
