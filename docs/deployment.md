# Local deployment

`dataset-gate serve` listens on 127.0.0.1:8765 by default. The optional API extra is
required. `docker compose up --build` packages the same service; its host port remains
bound to localhost, and a named volume stores reports. The container runs as uid 10001.

The container definition is provided for reproducibility. Build and validate it on a
Docker-enabled host before relying on it; Python/API tests alone do not prove a container
image works. This repository does not provision a public multi-user service.

Use an authenticated HTTPS reverse proxy and appropriate host allowlisting if adapting
this for a network deployment. Application-level tokens can protect the local API, but
are not a substitute for tenant isolation, TLS, request quotas and deployment review.
