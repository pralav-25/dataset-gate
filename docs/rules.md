# Contract rule reference

Every example below is one entry in a version-1 contract’s `rules` array.
See [semantics](semantics.md) for nulls, records, numeric limits and aggregate counts.

## allowed_pairs

Restrict exact pairs across two columns, including blank values.

Required parameters: other, pairs.

```json
{
  "id": "allowed-pairs",
  "check": "allowed_pairs",
  "column": "value",
  "params": {
    "other": "other",
    "pairs": [
      [
        "open",
        "pending"
      ],
      [
        "closed",
        "done"
      ]
    ]
  }
}
```

## column_count

Require an exact number of columns.

Required parameters: count.

```json
{
  "id": "column-count",
  "check": "column_count",
  "column": null,
  "params": {
    "count": 2
  }
}
```

## compare_columns

Compare pairs of finite numbers; incomplete pairs are skipped.

Required parameters: other, op.

```json
{
  "id": "compare-columns",
  "check": "compare_columns",
  "column": "value",
  "params": {
    "other": "other",
    "op": "le"
  }
}
```

## composite_unique

Require unique tuples across multiple columns; tuples containing blanks are included.

Required parameters: columns.

```json
{
  "id": "composite-unique",
  "check": "composite_unique",
  "column": null,
  "params": {
    "columns": [
      "a",
      "b"
    ]
  }
}
```

## conditional_required

Require a nonblank target when another column equals a declared string.

Required parameters: when, equals.

```json
{
  "id": "conditional-required",
  "check": "conditional_required",
  "column": "value",
  "params": {
    "when": "status",
    "equals": "closed"
  }
}
```

## date_format

Validate ISO dates or ISO datetimes with explicit timezone offsets.

Required parameters: format.

```json
{
  "id": "date-format",
  "check": "date_format",
  "column": "value",
  "params": {
    "format": "date"
  }
}
```

## date_order

Require a date or timezone-aware timestamp to be no later than another column.

Required parameters: other.

```json
{
  "id": "date-order",
  "check": "date_order",
  "column": "value",
  "params": {
    "other": "other"
  }
}
```

## distinct_ratio

Bound distinct nonblank values divided by the number of nonblank records.

Required parameters: min, max.

```json
{
  "id": "distinct-ratio",
  "check": "distinct_ratio",
  "column": "value",
  "params": {
    "min": 0.9,
    "max": 1
  }
}
```

## email

Check a conservative ASCII email shape; this does not verify ownership or delivery.

Required parameters: none.

```json
{
  "id": "email",
  "check": "email",
  "column": "value",
  "params": {}
}
```

## enum

Require nonblank cells to match one of the case-sensitive allowed strings.

Required parameters: values.

```json
{
  "id": "enum",
  "check": "enum",
  "column": "value",
  "params": {
    "values": [
      "open",
      "closed"
    ]
  }
}
```

## functional_dependency

Require each determinant value to map to only one dependent value.

Required parameters: dependent.

```json
{
  "id": "functional-dependency",
  "check": "functional_dependency",
  "column": "value",
  "params": {
    "dependent": "other"
  }
}
```

## json

Require valid JSON in nonblank cells and reject nonfinite numeric literals.

Required parameters: none.

```json
{
  "id": "json",
  "check": "json",
  "column": "value",
  "params": {}
}
```

## length

Check inclusive Unicode code-point lengths of nonblank strings.

Required parameters: min, max.

```json
{
  "id": "length",
  "check": "length",
  "column": "value",
  "params": {
    "min": 1,
    "max": 3
  }
}
```

## mean_range

Check the mean of finite nonblank numbers; empty or malformed numeric data fails.

Required parameters: min, max.

```json
{
  "id": "mean-range",
  "check": "mean_range",
  "column": "value",
  "params": {
    "min": 2,
    "max": 4
  }
}
```

## monotonic

Check numeric order across nonblank records, with optional strictness.

Required parameters: order.

```json
{
  "id": "monotonic",
  "check": "monotonic",
  "column": "value",
  "params": {
    "order": "increasing"
  }
}
```

## no_whitespace

Reject surrounding whitespace while preserving internal spaces.

Required parameters: none.

```json
{
  "id": "no-whitespace",
  "check": "no_whitespace",
  "column": "value",
  "params": {}
}
```

## not_null

Reject empty and whitespace-only cells; every record is checked.

Required parameters: none.

```json
{
  "id": "not-null",
  "check": "not_null",
  "column": "value",
  "params": {}
}
```

## null_ratio

Limit the fraction of blank records; an empty dataset has zero missingness.

Required parameters: max.

```json
{
  "id": "null-ratio",
  "check": "null_ratio",
  "column": "value",
  "params": {
    "max": 0.1
  }
}
```

## pattern

Match whole nonblank cells using shell-style globs, not executable regular expressions.

Required parameters: glob.

```json
{
  "id": "pattern",
  "check": "pattern",
  "column": "value",
  "params": {
    "glob": "T-*"
  }
}
```

## prefix

Require a literal case-sensitive prefix on nonblank cells.

Required parameters: value.

```json
{
  "id": "prefix",
  "check": "prefix",
  "column": "value",
  "params": {
    "value": "T-"
  }
}
```

## range

Require finite numeric cells inside inclusive lower and upper bounds.

Required parameters: min, max.

```json
{
  "id": "range",
  "check": "range",
  "column": "value",
  "params": {
    "min": 0,
    "max": 10
  }
}
```

## required_column

Require a named column even when there are no data records.

Required parameters: none.

```json
{
  "id": "required-column",
  "check": "required_column",
  "column": "value",
  "params": {}
}
```

## row_count

Require a dataset record count within inclusive bounds.

Required parameters: min, max.

```json
{
  "id": "row-count",
  "check": "row_count",
  "column": null,
  "params": {
    "min": 1,
    "max": 3
  }
}
```

## schema

Check exact column membership and optionally the declared order.

Required parameters: columns.

```json
{
  "id": "schema",
  "check": "schema",
  "column": null,
  "params": {
    "columns": [
      "a",
      "b"
    ]
  }
}
```

## sequence

Require every nonblank integer to advance by a declared step in record order.

Required parameters: step.

```json
{
  "id": "sequence",
  "check": "sequence",
  "column": "value",
  "params": {
    "step": 1
  }
}
```

## suffix

Require a literal case-sensitive suffix on nonblank cells.

Required parameters: value.

```json
{
  "id": "suffix",
  "check": "suffix",
  "column": "value",
  "params": {
    "value": ".csv"
  }
}
```

## sum_equals

Compare a target against a decimal sum with a nonnegative absolute tolerance.

Required parameters: columns.

```json
{
  "id": "sum-equals",
  "check": "sum_equals",
  "column": "value",
  "params": {
    "columns": [
      "a",
      "b"
    ]
  }
}
```

## type

Validate nonblank lexical types; string accepts any text and number accepts integers.

Required parameters: type.

```json
{
  "id": "type",
  "check": "type",
  "column": "value",
  "params": {
    "type": "integer"
  }
}
```

## unique

Require distinct nonblank values; only later duplicate records fail.

Required parameters: none.

```json
{
  "id": "unique",
  "check": "unique",
  "column": "value",
  "params": {}
}
```

## url

Require an absolute HTTP or HTTPS URL with a host and no embedded credentials.

Required parameters: none.

```json
{
  "id": "url",
  "check": "url",
  "column": "value",
  "params": {}
}
```

## uuid

Nonblank cells must be 36-character hyphenated UUIDs. Hexadecimal letters may
be uppercase or lowercase; braces, URN prefixes, compact hex, and surrounding
whitespace are rejected. Nil UUIDs are accepted. Blanks are skipped; combine with
`not_null` when required. Each nonblank cell contributes one checked result;
malformed cells fail and up to 20 record indices are retained. No parameters.

```json
{
  "id": "uuid",
  "check": "uuid",
  "params": {},
  "column": "value"
}
```

## ip_address

`version` is optional: `any` (default), integer `4`, or integer `6`. Booleans
are rejected. Nonblank cells must be an address of the chosen version; subnet
suffixes, zone identifiers, and surrounding whitespace fail. Uses standard-library
`ipaddress` parsing, including its rejection of IPv4 leading zeros. Blanks are
skipped. Counts are per nonblank cell, with up to 20 failing record indices.

```json
{
  "id": "ip-address",
  "check": "ip_address",
  "params": {
    "version": "any"
  },
  "column": "value"
}
```

## decimal_scale

`places` is required: an integer from 0 through 18, excluding bool. Nonblank
cells must be finite numbers in the shared numeric domain and exactly representable
with at most that many fractional digits. Trailing zeros do not count: `1.2300`
passes with 2 places. Scientific notation is interpreted numerically. Blanks are
skipped; every other cell is checked and malformed numbers fail. Up to 20 failing
record indices are returned. Decimal tuples are inspected without binary floats.

```json
{
  "id": "decimal-scale",
  "check": "decimal_scale",
  "params": {
    "places": 2
  },
  "column": "value"
}
```

## multiple_of

`divisor` is required: a positive finite JSON number in the shared numeric
domain, excluding bool. Each nonblank cell must be a finite exact multiple of
that divisor; negative multiples and zero pass. Blanks are skipped. Decimal
values are converted to exact integer ratios for divisibility, avoiding binary
rounding and Decimal context precision. Counts are per nonblank cell; at most
20 failing record indices are retained.

```json
{
  "id": "multiple-of",
  "check": "multiple_of",
  "params": {
    "divisor": 0.05
  },
  "column": "value"
}
```

## median_range

`min` and `max` are required finite JSON numbers in the shared numeric
domain, with min <= max and bool excluded. Bounds are inclusive. Blank cells
are ignored; no nonblank values or any malformed numeric cell fails the aggregate.
Even-sized samples average their two central values using exact rational arithmetic.
The rule produces checked=1 and failed=0 or 1, with no row samples.

```json
{
  "id": "median-range",
  "check": "median_range",
  "params": {
    "min": 2,
    "max": 4
  },
  "column": "value"
}
```

## quantile_range

`q`, `min`, and `max` are required finite JSON numbers, excluding bool.
q lies in [0,1] and min <= max. The sorted sample is interpolated at q*(n-1)
(type-7 quantile), with inclusive bounds and exact rational arithmetic. Blank
cells are ignored; empty samples or any malformed number fail. This aggregate
always has checked=1, failed=0 or 1, and no row samples.

```json
{
  "id": "quantile-range",
  "check": "quantile_range",
  "params": {
    "q": 0.9,
    "min": 0,
    "max": 30
  },
  "column": "value"
}
```

## string_case

`case` is required: `lower` or `upper`. A nonblank cell passes when it is
unchanged by the corresponding Python Unicode case conversion. Digits, punctuation,
and scripts without case pass both modes. Text is not stripped or normalized;
combine with `no_whitespace` for whitespace restrictions. Blanks are skipped.
Counts are per nonblank cell, with at most 20 failing record indices.

```json
{
  "id": "string-case",
  "check": "string_case",
  "params": {
    "case": "lower"
  },
  "column": "value"
}
```

## nonblank_count

`columns` is a required nonempty list of distinct column names. `min` and
`max` are required nonnegative integers, excluding bool, with min <= max <=
the number of listed columns. This supports exactly-one and at-least-one field
requirements. Every record is checked, including fully blank records. A cell
is populated when its text is not whitespace-only. Missing columns produce a
failed finding. At most 20 failing record indices are retained; `column` is omitted.

```json
{
  "id": "nonblank-count",
  "check": "nonblank_count",
  "params": {
    "columns": [
      "a",
      "b"
    ],
    "min": 1,
    "max": 1
  }
}
```

## date_range

Require canonical `YYYY-MM-DD` dates between inclusive `min` and `max` dates. Both bounds are required, must be valid calendar dates, and must satisfy `min <= max`. Nonblank cells are checked individually; malformed dates and dates outside the interval fail. Blank cells are skipped. Whitespace is not trimmed.

```json
{
  "id": "rule",
  "check": "date_range",
  "column": "value",
  "params": {
    "min": "2024-01-01",
    "max": "2024-12-31"
  }
}
```

## sum_range

Require the exact decimal sum of nonblank cells to fall between inclusive numeric `min` and `max` bounds. Both finite bounds are required and must satisfy `min <= max`. Numeric cells follow the shared bounded numeric domain. A malformed or nonfinite value fails the single aggregate check. Blanks are skipped; the empty sum is zero. `checked` is 1, `failed` is 0 or 1, and record samples are empty.

```json
{
  "id": "rule",
  "check": "sum_range",
  "column": "value",
  "params": {
    "min": 0,
    "max": 5
  }
}
```

## distinct_count

Bound the number of distinct nonblank cell values with required nonnegative integer `min` and `max` parameters. Booleans and fractional bounds are rejected; `min <= max` is required. Matching is case-sensitive and values are not trimmed. Empty or entirely blank columns have zero distinct values. This produces one aggregate check, zero or one failures, and no record samples.

```json
{
  "id": "rule",
  "check": "distinct_count",
  "column": "value",
  "params": {
    "min": 1,
    "max": 1
  }
}
```

## luhn

Check each nonblank identifier using the Luhn checksum. Values must contain at least two ASCII digits, including the check digit. No parameters are accepted. Leading zeros are preserved; spaces, punctuation, signs, and non-ASCII digits fail. Blank cells are skipped. This verifies a checksum only; it does not establish that an identifier was issued, is active, or is unique.

```json
{
  "id": "rule",
  "check": "luhn",
  "column": "value",
  "params": {}
}
```

## unicode_normalization

Require each nonblank value to already be in the declared Unicode normalization `form`: `NFC`, `NFD`, `NFKC`, or `NFKD`. The parameter is required and case-sensitive. Values are inspected without modifying them. Blanks are skipped; each nonblank value contributes one checked record and each mismatch one failure. Compatibility forms may distinguish characters that canonical forms preserve.

```json
{
  "id": "rule",
  "check": "unicode_normalization",
  "column": "value",
  "params": {
    "form": "NFC"
  }
}
```

## not_in

Reject nonblank cells that exactly match a forbidden entry in required `values`. Provide 1–200 distinct nonempty strings of at most 200 characters each. Matching is case-sensitive and no trimming or Unicode normalization is performed. Blank cells are skipped; combine with `not_null` to reject blanks. Each nonblank cell is checked once, with failing record samples bounded to 20.

```json
{
  "id": "rule",
  "check": "not_in",
  "column": "value",
  "params": {
    "values": [
      "unknown"
    ]
  }
}
```

## ip_network

Validate IPv4 or IPv6 CIDR networks with an explicit numeric prefix length and no host bits set. Optional `version` is integer `4`, integer `6`, or `"any"` (default); booleans are invalid. Bare addresses, dotted netmasks, scoped IPv6 addresses, and surrounding whitespace fail. `/0` and full-length host prefixes are valid when their network address is valid. Blanks are skipped and nonblank cells are checked individually.

```json
{
  "id": "rule",
  "check": "ip_network",
  "column": "value",
  "params": {
    "version": "any"
  }
}
```

## json_type

Parse each nonblank cell as JSON and require the top-level `type`: `object`, `array`, `string`, `number`, `boolean`, or `null`. The parameter is required. Booleans are distinct from numbers. Decimal parsing avoids binary-float overflow for large finite numeric literals; nonstandard `NaN` and `Infinity` literals, including nested ones, fail. Malformed or excessively nested JSON also fails the record. CSV blanks are skipped; the literal JSON `null` is checked.

```json
{
  "id": "rule",
  "check": "json_type",
  "column": "value",
  "params": {
    "type": "object"
  }
}
```
