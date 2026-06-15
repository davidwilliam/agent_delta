In the `saasapp` service, users are seeing projects from other tenants (for
example `alice` in tenant `acme` can see and fetch the `globex` project "Secret").
Make it so a user can only ever view projects in their own tenant, then run
`pytest -q tests/`.
