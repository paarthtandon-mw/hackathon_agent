# Information Model

The information model describes what and how content is stored in the IR elasticsearch cluster.

The Meltwater dataset holds all the enriched [editorial and social data](dataset/sources/) that is available to customers through the Media Intelligence and other product lines. This contains JSON documents, with a schema defining how the data is modeled and indexed, thus supporting search and analytics requests on top of the dataset.

The datasets reside within Europe, and Ireland and Norway are our current storage and processing locations.

| Dataset    | Description                                                                                                                                                                                                                                                                                                               | API base URL                            |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| Production | All content currently available and used by MI (Media Intelligence) and other Meltwater products.                                                                                                                                                                                                                         | https://mi.content.fairhair.ai/         |
| Staging    | All content currently available in production, but with a set of  sample rules:<br>- 100% day 0-3<br>- 5% day 4-90<br>- 1% day 91-730<br>- 0% after day 730<br><br>Tagged documents, as well as owned social data (from Engage, FB, IG, LI and TW dm's) are excluded from above rules, where 100% is stored until day 730 | https://mi-staging.content.fairhair.ai/ |

