# Deduplicating

In GroupedResultList and SortedGroupedResultList you need to define how to cluster similar documents into groups. The similarity types we support are: exact match, charikarHamming distance or max.

## Exact similarity

Exact similarity will group up documents where the field is identical in the documents.

**Parameters**:

* **field**: The field to group on. Please note that it's not possible to group on fields from [Nested Objects](docs/default/component/mi-information-model/Dataset/terminology/#nested-object.md).

```json
"similarityType": {
  "type": "exact",
  "field": "body.title.text"
}
```



## Charikar hamming distance similarity

Charikar hamming distance groups up documents based on how similar a hash of the document is. 
The similarity is computed as the percentage of bits that differs between two hashes. 

You can tweak the threshold for how many percent similar the hashes needs to be to be considered in the same group using the `threshold` parameter in the GroupedResultList or SortedGroupedResultList.

The only hash currently supported is the field `enrichments.charikarLSH`. The Charikar hash here is optimized so that similar content gives very similar hashes.

**Parameters**:

* **field**: The hash field to be used for grouping . Please note that it's only possible to use `enrichments.charikarLSH` field.

```json
"similarityType": {
  "type": "charikarHamming",
  "field": "enrichments.charikarLSH"
}
```



## Max similarity

You can also use a combination of different similarities using the max similarity. The max similarity will compute all the sub similarities and then use the max value from those to group up documents.

**Parameters**:

* **similarities**: A list of similarities.

```json
"similarityType": {
  "type": "max",
  "similarities": [
    {
      "field": "body.title.text",
      "type": "exact"
    },
    {
      "field": "enrichments.charikarLSH",
      "type": "charikarHamming"
    }
  ]
}
```

