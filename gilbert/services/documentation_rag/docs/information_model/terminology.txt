# Terminology

## Alias
An alias is a handle to a field in the information model. Aliases are usually added for convenience for whoever wants to query
a document. An example would be the alias `content`, which is a handle to the expanded field `body.content.text`.

## Nested Object

The *nested* type is a specialized version of the object data type that allows arrays of objects to be indexed in a way that they can be queried independently of each other.

For example, if a document has multiple authors, it is possible to match the document searching for any of the listed authors.

```json
{
  "metaData" : {
    "authors" : [ 
      {
        "authorInfo" : {
        	"externalId" :  "123456",
          "handle" : "@johndoe",
          "rawName" : "John Doe"
        }
      },
      {
        "authorInfo" : {
        	"externalId" :  "7891011",
          "handle" : "@doejane",
          "rawName" : "Jane Doe"
        }
      }
    ]
  }
}
```
