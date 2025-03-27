# Extensible Queries

[xRunes](https://www.npmjs.com/package/@meltwater/xrunes) is an npmjs library that provides the patterns and tooling to create an extensible, superset of the *Runes* query syntax.

- Extensible query types can be implemented to compose primitive queries into domain specific queries.
- Queries that are composed with extensible query types can be rendered into *Runes* query syntax.
  
!!! type "Note"
  Only available in Node.js. Extensible Queries are only supported in the Node.js v12+ environment.



## Benefits

- **Declarative**: Use-case specific query types allow for clear, expressive, powerful queries
- **Composable**: You can compose complex queries using simple building blocks.
- **Reusable**: You can share queries across applications and teams.
- **Maintainable**: Queries are compartmentalized, testable, and isolated.
- **Extensible**: As a superset of the runes query syntax, new query types can be built and used alongside the primitive types.
- **Productive**: Using already built query types and iterating on top of them lets us develop faster and be more productive.

## Example

Below are several examples of the benefits of using extensible query types. Toggle below on the tabs to see a query using an extensible type and the equivalent query using only primitive types.

#### Named Date Range

`x:dateRange` converts a named date range to a `range` type with millisecond date values.

```json
{
  "type": "x:dateRange",
  "field": "body.publishDate.date",
  "rangeType": "LAST_WEEK"
}
```

#### Template Queries

`x:all` renders an array of values against a query template.

```json
{
  "type": "x:all",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "allQueries": ["apple", "banana", "orange", "pear", "cherry"]
}
```

#### Domain Specific Queries

`social:tweet` renders a query to retrieve a specific tweet provided the url.

```json
{
  "type": "x:tweet",
  "url": "https://twitter.com/MeltwaterEng/status/1445822363824656390"
}
```



## Getting Started

## Installing xRunes

```shell
npm whomai # must be a user with access to the npmjs Meltwater organization.

npm install @meltwater/xrunes @meltwater/xrunes-core --save
```

## Initialize xRunes and register query types

```javascript
const xRunes = require("@meltwater/xrunes");
const XRunesCore = require("@meltwater/xrunes-core");

let xRunes = new xRunes();

// register extensible rune components
xRunes.registerLibrary(XRunesCore))

// render the runes query to primitive types
let result = xRunes.render({
  query: {
    type: "x:all",
    allQueries: [
      {
        type: "x:dateRange",
        field: "body.publishDate.date",
        rangeType: "LAST_WEEK",
      }
    ],
  },
});
```

## Building a Query Type Handler

Query type handlers implement a simple class interface:

- a constructor that optionally is provided a reference to the `XRunes` object.
- a readonly `type` property that returns the unique name. Conventionally, the name is prefixed with a namespace: `namespace:queryType`.
- an async `render` function that accepts an xRunes query and returns a runes query.

#### Example

```javascript
class ExampleQuery {
  constructor() {}

  get type() {
    return "x:example";
  }

  async render(query) {
    let { boost } = query;

    // custom implementation

    return {
      xtype: this.type, // always include xtype
      boost, // always include boost
      type: "term",
      field: "body.content.text",
      value: "Hello World!",
    };
  }
}
```

Register the new query type with the `xRunes` object.

```javascript
xRunes.register(new ExampleQuery());
// or
xRunes.registerLib({
  ExampleQuery
});
```

#### Composite Example

In many cases extensible query types may be defined in terms of *other* extensible query types. In this case a recursive call to `render` must be made. 

```javascript
class CompositeExampleQuery {
  constructor(xRunes) {
    this.xRunes = xRunes;
  }

  get type() {
    return "x:compositeExample";
  }

  async render(query) {
    let { boost } = query;

    // custom implementation

    return this.xRunes.render({
      xtype: this.type, // always include xtype
      boost, // always include boost
      type: "all",
      allQueries: [
        {
          type: "x:example",
        },
        {
          type: "term",
          field: "enrichments.sentiment.discrete",
          value: "p",
        },
      ],
    });
  }
}
```



## Core Query Types and Decorators

[@meltwater/xrunes-core](https://www.npmjs.com/package/@meltwater/xrunes-core) is a supplemental library that provides:
- A collection of common extensible query types.
- A collection of common decorators for authoring extensible query types.

## Core Query Types

### Named Date Range Query

It can be cumbersome to deal with epoch milliseconds or ISO8601 dates when writing ad-hoc search queries. This query accepts a named date range to ease manipulation of the search range.

Unlike the `range` type query, either the upper bound or lower bound may be excluded. It will default to 365 days.

#### Parameters

- **field**: The field to search in.
- **rangeType**: (optional) The named date range as defined in [meltwater/date-range](https://github.com/meltwater/date-range).
- **timezone** (optional): The name of the [moment timezone](https://momentjs.com/timezone/).
- **to** (optional): The upper bound.
- **from** (optional): The lower bound.
- **includeTo** (default _false_): If the _from_ value should be included in the range.
- **includeFrom** (default _true_): If the _to_ value should be included in the range.
- **boost** (default 1.0): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "x:dateRange",
  "field": "body.publishDate.date",
  "rangeType": "TODAY"
  // "timezone": "America/New_York"
}
```

### Match Query

The Match query is a variation on the [Not query](../queries/boolean-queries.md#not-query) that allows for an optional `notMatchQuery` parameter. This allows for the `notMatchQuery` parameter to be optionally toggled on and off without modifying the query type.

#### Parameters:

- **matchQuery** (required): The nested query that must match.
- **notMatchQuery** (optional): The nested query that must not match.
- **boost** (default 1.0): Boost hits from this query compared to other queries, see [Sorting](../results/sorting.md).

```json
{
  "type": "x:match",
  "matchQuery": {
    "type": "word",
    "field": "body.content.text",
    "value": "meltwater"
  },
  "notMatchQuery": {
    "type": "word",
    "field": "body.content.text",
    "value": "glacier"
  }
}
```



```javascript
let baseQuery = {
  type: "x:match",
  matchQuery: {
    type: "word",
    field: "body.content.text",
    value: "meltwater",
  },
};

// `notMatchQuery` can be optionally included without
// restructuring the query type.
if (exludeGlacier) {
  basesQuery.notMatchQuery = {
    type: "word",
    field: "body.content.text",
    value: "glacier",
  };
}
```

### Any Query

Often the nested queries within a boolean query follow a similar template. As a result the full boolean query is often quite verbose and difficult to visually parse or programmatically construct.

#### Parameters

- **template**: A partial query object that contains the properties that are the same on each nested query
- **anyQueries** (or _values_, _queries_): The values to apply to each nested query, of which at least one must match.
- **property** (default _value_): The name of the property to be added to the template with each string value.
- **boost** (default _1.0_): Boost hits from this query compared to other queries, see Sorting.

```json
{
  "type": "x:any",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "anyQueries": ["apple", "banana", "orange", "pear", "cherry"]
}
```

### All Query

Often the nested queries within a boolean query follow a similar template. As a result the full boolean query is often quite verbose and difficult to visually parse or programmatically construct.

#### Parameters

- **template**: A partial query object that contains the properties that are the same on each nested query
- **allQueries** (or _values_, _queries_): The values to apply to each nested query, of which all must match.
- **property** (default _value_): The name of the property to be added to the template with each string value.
- **boost** (default _1.0_): Boost hits from this query compared to other queries, see Sorting.

```json
{
  "type": "x:all",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "allQueries": ["apple", "banana", "orange", "pear", "cherry"]
}
```

### Near Query

The near query matches when a set of nested queries match within a certain distance within the text of the field. The extensible version includes the same enhancements as `x:all` and `x:any`.

#### Parameters

- **template**: A partial query object that contains the properties that are the same on each nested query
- **queries** (or _values_): The values to apply to each nested query, of which all must match.
- **property** (default _value_): The name of the property to be added to the template with each string value.
- **inOrder** (default _false_): If the nested queries must appear in the specified order for the query to match.
- **slop** (default _4_): How many words or tokens that are allowed to appear between the specified queries.
- **boost** (default _1.0_): Boost hits from this query compared to other queries, see Sorting.

```json
{
  "type": "x:near",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "queries": ["apple", "banana", "orange", "pear", "cherry"]
}
```

### Template Query

The base for All, Any, and Near Query. This abstract query type handles all generic collection based queries. All nested queries are transformed based on a template.

#### Parameters

- **template**: A partial query object that contains the properties common to each nested query.
- **values** (or _queries_): The values to apply to each nested query.
- **valueProperty** (default _value_): The name of the property to be added to each nested query.
- **typeProperty**: The value to assign to the property `type`.
- **arrayProperty**: The name of the property to assign the array of nested queries.
- **boost** (default _1.0_): Boost hits from this query compared to other queries, see Sorting.

```json
{
  "type": "x:template",
  "typeProperty": "all",
  "valueProperty": "value",
  "arrayProperty": "allQueries",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "values": [
    { "value": "apple" },
    { "value": "banana" },
    { "value": "orange" },
    { "value": "pear" },
    { "value": "cherry" }
  ]
}
```

### Identity Query

A query that renders a copy of the query it was provided. Its primary applications are unit tests and applying decorators to primitive types.

#### Parameters

- **query**: The runes query.
- **boost** (default _1.0_): Boost hits from this query compared to other queries, see Sorting.

```json
{
  "type": "x:identity",
  "query": {
    "type": "term",
    "field": "body.title.text",
    "value": "meltwater"
  }
}
```

## Core Query Type Decorators

Decorators handle common query rendering transformations.

### Boost Decorator

`boostDecorator` adds the `boost` property to the rendered query if set on the xRunes query.

### xType Decorator

`xtypeDecorator` adds the `xtype` property to the rendered query. It is useful for debugging and troubleshooting rendered xRunes queries.

`type` property is required on the query type handler.

### Compound Decorator

`compoundDecorator` runs the xRunes processor against the results of the rendered query. This enables the xRunes query types to be defined as a composition of other xRunes query types.

`xRunes` property is required on the query type handler to be set to an instance of the xRunes processor.

### Bind Decorator

`bindDecorator` evaluates the mappings of the `bind` object on the query object and applies the results to the query object _before_ rendering. This allows dynamic values to be applied to subqueries at render time.

#### Example

In the xRunes query below:

- The outer query `kg:company` makes an external call for company data based on an id
- The inner query `social:tweets` renders a query for tweets from a specific `handle`

The `bind` property contains mappings that transform the `twitterHandle` of the company to the `handle` of the tweets query. Without `bind`, a new query type would be required to link the two query types.

```json
{
  "type": "kg:company",
  "companyId": "12345",
  "bind": {
    "query.handle": "company.twitterHandle"
  },
  "query": {
    "type": "social:tweets"
  }
}
```

### `decorate` Utility Function

Utility function for composing multiple decorators onto a query handler.

```javascript
// Function
function decorate(Query, ...decorators) {}

// Usage
module.exports = decorate(
  MyQuery,
  FirstDecorator,
  SecondDecorator,
  ThirdDecorator
  //...
);
```

## xRunes Proxy

xRunes Proxy is a reverse proxy that renders extensible queries to primitive query syntax and routes the request to `https://mi.content.fairhair.ai`.
[block:callout]
{
  "type": "warning",
  "title": "Not Intended for Production",
  "body": "The xRunes Proxy should only be used for exploring, composing, and debugging extensible queries."
}
[/block]


```http
POST /v1/search?apikey={YOUR-API-KEY} HTTP/1.1
Host: xrunes-proxy.meltwater.io
content-type: application/json
{
  "type": "x:all",
  "template": {
    "type": "word",
    "field": "body.content.text"
  },
  "allQueries": ["apple", "banana", "orange", "pear", "cherry"]
}
```

- **Staging**: `xrunes-proxy.meltwater.io`
- **Production**: `xrunes-proxy-staging.meltwater.io`

`apikey` is the same key associated with your Content API consumer. _Cf. [IR API guide](/docs/default/component/ir-api-access)_.

## Maintaner

These Node.js libraries are maintained by Team Phoenix. To get in touch with us, use our [Slack channel](https://meltwater.slack.com/archives/GJYBX5JRL), or [send us an email](mailto:phoenix@meltwater.com).
