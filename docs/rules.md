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
