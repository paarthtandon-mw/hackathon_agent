# Predefined Similarity Types

With Search V2 API, you can take advantage of predefined similarity options that allow you to access common grouping logic (`Duplicates settings`) from a central location.

Instead of using `similarityType`, you can simply provide the `predefinedSimilarityType` field. 

Currently, there are two options: `exact` and `similar`. These options correspond to the following values in the app:

![duplicates-settings.png](assets/duplicates-settings.png)

An example request view:
```
...
"groupedResultListWithSimilar": {
  "type": "groupedResultList",
  "threshold": 0.92,
  "start": 0,
  "size": 10,
  "groupFrom": 0,
  "numToGroup": 1000,
  "predefinedSimilarityType": "similar"
}
...
```