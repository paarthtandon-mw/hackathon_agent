# Aliases

Aliases are added to the information model by inserting a list with the key `aliases` to a field in the information-model.
After platform-tenants has been released, the `mi-information-model` version in [boolean-query-parser](https://github.com/meltwater/boolean-query-parser/)
has to be bumped and then the `boolean-query-parser` and `mi-information-model` versions have to be bumped in [masfsearch](https://github.com/meltwater/masfsearch/).
The alias can then be used as a handle/shortcut for consumers of the information-model to lookup that field. Unfortunately,
there are also some more complex aliases that reside in [boolean-query-parser](https://github.com/meltwater/boolean-query-parser/blob/14997b5ab88ae8835315bc66b6391e807a7921cb/boolean-query-parser/src/main/kotlin/com/meltwater/booleanqueryparser/BooleanQueryParser.kt#L173).

**NOTE**:The aliases are only valid to use in *boolean queries* and **must** be expanded before they get converted to a rune format.

E.g. the alias `content` for `body.content.text`
```yaml
  body.content.text:
    type: string
    indexed: true
    analyzed: true
    reversed: true
    prefixes: true
    aliases:
      - content
```

One field can have multiple aliases, e.g. the field `metaData.authors.authorInfo.handle` is aliased by `author`, `from` and `handle`.

```yaml
    metaData.authors.authorInfo.handle:
      type: string
      indexed: true
      reversed: true
      aliases:
        - author
        - from
        - handle
```

Note that the same alias can point to more than one field, thus indicating that a consumer who is using such an alias
is actually interested in all of those fields. E.g. the alias author points to both `metaData.authors.authorInfo.handle` and
`metaData.authors.authorInfo.rawName`

```yaml
    metaData.authors.authorInfo.handle:
      type: string
      indexed: true
      reversed: true
      aliases:
        - author
        - from
        - handle
    metaData.authors.authorInfo.rawName:
      type: string
      indexed: true
      analyzed: true
      reversed: true
      aliases:
        - author
```
