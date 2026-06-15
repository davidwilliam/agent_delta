In the `saasapp` service, add a new `suspended` account state: `active` can go to
`suspended`, `suspended` can go back to `active` or to `closed`, a suspended
account cannot create projects but its users can still view them, and existing
active/closed behavior stays the same. When done, run `pytest -q tests/`.
