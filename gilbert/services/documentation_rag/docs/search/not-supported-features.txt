# Not Supported Features & Queries

This is a list of common use cases that are **not** supported in the Search API.

- **Value length:** It is not possible to search on the length of a field value.
    - **Example:** Find all documents that have a content body longer than 1000 chars.

- **Frequency in nears:** It is not possible to set frequency on a word query inside a near query
    - **Example:** Word1 near Word2{2,} is the same as Word1 near Word2 or even Word1 near Word2{99,}
