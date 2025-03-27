# Tokenization

In order to support search on specific words or sentences in the documents we store, the document content is *tokenized*. Roughly speaking, this means splitting document sentences into individual words ("tokens").

Tokenization happens in two places: Firstly, when we index, text is tokenized into terms not only using whitespace, but also with most special characters (such as dots, comma and other punctuation characters). For example, ".sports" is tokenized into two tokens: "." and "sports". The difference with whitespace is that it does not become a token, i.e. you cannot search for whitespace.

Secondly, it happens when executing a search against the dataset because we want to tokenize in the same way in order get matches. This means that a search for "sports" will match both ".sports" and ". sports" (notice the whitespace). If we did not separate ".sports" in the tokenization, then one could match just that exact string when searching, but you would not match it when searching for "sports" only. In other words, this is a tradeoff is better recall for worse precision.
