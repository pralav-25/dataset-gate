# Data and rule semantics

## Parsing

UTF-8 with an optional BOM; comma-separated CSV or extension-selected TSV, optionally
compressed with gzip. Explicit delimiters override the extension. Duplicate or empty
headers, malformed records, NULs, excessive sizes, and inconsistent widths are errors.
Blank physical records are rejected rather than skipped. Quoted multiline cells work.

The limits are 5,000,000 decoded UTF-8 bytes, 50,000 data records and 200 columns.
The standard-library CSV parser additionally bounds individual field length.
Record indices begin at one after the header; they are not physical line numbers.

## Nulls and checks

Only empty or whitespace-only cells are null. Literal `NA`, `null`, and `None` are text.
Most scalar rules skip nulls; add `not_null` to require values. `not_null`,
`no_whitespace`, composite keys, allowed pairs, and functional dependencies include blanks.
A skipped/all-blank scalar rule can pass with zero checked cells, which is why requiredness
must be explicit. Row-count rules detect header-only or unexpectedly small files.

Uniqueness reports later duplicate records; the first occurrence is retained. Samples
contain at most 20 indices, but failure totals count every matching record. A missing
referenced column produces a failed rule with a structural diagnostic.

Finite numbers use Decimal parsing with up to 128 source characters and magnitude
exponents within ±100. Profiles convert accepted values to finite floating-point numbers.
Arithmetic checks use decimal semantics; profiling uses population standard deviation
and linear-interpolated quartiles. Integer inference rejects leading-zero identifiers.
Datetime checks require timezones. Unicode text is not normalized.

## Contracts and scores

Version 1 has a name and 1..100 uniquely identified rules. Unknown fields, checks and
parameters fail validation. JSON-file duplicate keys and nonfinite numbers are rejected.
Inference drafts column-presence and observed-type rules; it does not invent business
ranges or claim that a sample establishes truth. Review drafts before enforcement.

Quality score is the percentage of configured rules that pass, with equal rule weighting.
It is not a fraction of clean rows: row and aggregate checks measure different things.
Errors fail the default gate. Warnings fail only with `--fail-on-warning`; a minimum score
is also optional. Changing the contract changes what a score means.

## Comparisons

Schema changes, blank-rate deltas, numeric summaries, and total variation of categorical
frequencies are descriptive. Total variation is absent when either nonblank sample is
empty. Column labels are aligned by name; raw category values are not exported.
