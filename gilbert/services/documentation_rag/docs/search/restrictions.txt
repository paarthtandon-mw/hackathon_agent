# Restrictions

For some of the content that is ingested there are some legal terms and conditions that says who can and can't be shown certain content. 

All the APIs that exposes our data support a restrictions parameter to the request, see below.
This is an optional parameter because of backwards compatibility reasons, but any request that doesn't specify it will have **all** content with any restriction on it omitted.  


**Restrictions supported**:

* Omit tweets that are hidden in certain countries. (*Will be supported shortly*)


**Parameters**

* **requestorCountry**: The country from which the requestor is sending the request. Should be specified as lowercase ISO_3166-1_alpha-2.





```json
"restrictions": {
  "requestorCountry": "se"  
}
```

