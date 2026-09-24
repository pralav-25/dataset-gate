# Security scope

Dataset Gate is a bounded, local, single-user developer application. It does not provide
multi-tenant accounts, internet-facing rate limiting, or distributed isolation.

The API binds to loopback by default and rejects unknown Host headers. Set
`DATASET_GATE_TOKEN` to require `Authorization: Bearer <token>` on every route except
`/health`. Requests are capped at 6 MB even when streamed, and mutation routes require
JSON. Never commit the token. `DATASET_GATE_HOSTS` can set an explicit comma-separated
Host allowlist for a reverse proxy; avoid wildcard hostnames.

Raw CSV values are never written to history. Reports include headers, contract names,
aggregated distributions and bounded record indices; treat those as potentially sensitive.
Review notes are arbitrary user text. Store the database on an appropriately protected
filesystem. Exported HTML escapes user strings; CSV exports neutralize formula prefixes.

Reports are written atomically, refuse replacement by default, and cannot overwrite
provided input-file aliases. SQLite uses bound values and transaction-scoped connections.
Configuration cannot import code, execute expressions, fetch URLs, or choose API filesystem
paths. Glob checks intentionally avoid arbitrary regular expressions.

Before any public deployment, add TLS, authentication suitable to your users, request quotas,
resource monitoring and deployment-specific review. The provided container stays loopback-bound
through Compose. Report vulnerabilities privately to the repository owner; do not include
real datasets or credentials in public issues.
