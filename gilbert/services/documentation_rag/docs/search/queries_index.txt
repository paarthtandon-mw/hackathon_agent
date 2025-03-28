# Queries

The **query** parameter of the [Search API](../api-post-search.md) uses something called the *Runes* query syntax, which takes the form of a tree of JSON objects with multiple nesting levels. It has a number of query constructs and allows expressing complicated Boolean logic.

**Field queries**:

- **term** query which filters for an exact value in a field, for non-analyzed fields. Non-analyzed fields are categorical fields where exact matching is supported, for example language and country codes.
- **terms** query which filters for an multiple values in a field, for non-analyzed fields. Non-analyzed fields are categorical fields where exact matching is supported, for example language and country codes.
- **word** query which performs full text search of analyzed fields. Analyzed fields are those where keyword/phrase based search are supported, for example the document title and body.
- **wildcard** query allows for expansion of \* and ? wildcards in words.
- **range** query matches a numeric or date field with an upper and lower bounds.
- **exists** query which filters for an existing field.

**Boolean queries**:

- **all** query represent an *AND* statement. It requires all the nested queries to match.
- **any** query represent an *OR* statement. It requires at least one of the nested queries to match
- **not** query express an *AND NOT* statement. It has one nested query that needs to match, and another nested query that must not match.

**Special queries**:

- **near** query express that a set of nested queries must match within a certain distance within the text of the field.
- **nested** query searches inside nested objects, for example a list of authors or named entities.
