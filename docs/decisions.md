# Engineering decisions

- **Data contracts before model metrics.** This project catches shape, value, relationship,
  and completeness errors before training. It complements drift/model monitoring tools.
- **Raw strings survive ingestion.** Leading zeros, whitespace, and textual identifiers are
  preserved. Rules choose how to interpret values; parsing never silently cleans data.
- **Configuration errors are distinct from quality failures.** Invalid contracts abort with
  exit 2; executed contracts with failing gates use exit 1. CI can distinguish the two.
- **Reports avoid raw cell values.** Failed record indices and aggregated profiles support
  debugging while reducing accidental value disclosure. Headers and contract names remain
  visible and may still be sensitive.
- **Original datasets stay outside the history database.** Reports can be reviewed and
  exported without storing a second copy of input CSV content.
- **No statistical significance claim.** Dataset comparisons are descriptive changes, not
  claims about model degradation or hypothesis-test outcomes.
