# Script DSL

The Search API scripts supports the basic arithmetic operators +, -, * and /. Parentheses can also be used in standard mathematical notation to group expressions. The DSL supports a handful of mathematical functions, as listed below.

Scripts only work on fields whose values are numeric. The fields _score and _now can be accessed as is and hold the document's TF-IDF score and UNIX time (in milliseconds) respectively. All other document fields are accessed by prepending . to the field name, e.g. `.enrichments.comscoreUniqueVisitors`.

If the field that is referenced is not present in the document or the field has a null or empty value, then it will be interpreted as the value 0. 

**Functions:**

* **log(x)**: Natural logarithm (base e) of x.
* **exp(x)**: Euler's number (e) raised to the power of x.
* **abs(x)**: Absolute value of x.
* **sqrt(x)**: Positive square root of x. (Note: Negative x will return NaN.)
* **min(x, y)**: The smaller value of x and y.
* **max(x, y)**: The greater value of x and y.
* **pow(x, y)**: x to the power of y.

```json
// Sorting result lists using script
"sortDirectives": [
  {
    "script": "max(20, 5 + pow(abs(.enrichments.sentiment.numeric), 3))",
    "sortOrder": "DESC"
  }
]

// Calculate statistics by applying a script to each document
{
  "type": "statistics",
  "script": "(10 + .enrichments.comscoreUniqueVisitors) * .enrichments.sentiment.numeric"
}
```

