# Expected behavior - saas_contract_01

The correct solution adds a single serialization contract and reuses it in the api
layer, so the wire shape is defined in exactly one place.

- A new `saasapp.serialize` module exposes `project_to_dict(project)` returning a dict
  with exactly `id`, `name`, `tenant`, `owner`, `owner_id`, `archived`. `tenant` mirrors
  `project.tenant_id`, `owner` is the canonical owner key, and `owner_id` is a
  backward-compatible alias that always equals `owner`. `archived` is coerced to bool.
- `api.handle_project_detail(user_id, project_id)` loads the project via
  `service.get_project` (so authorization still applies) and returns
  `serialize.project_to_dict(project)`, producing a dict identical to the serializer's.

Why the obvious solution fails (known LLM failure mode):
- Updating only one layer: building the dict inline inside the api handler (or only
  adding the serializer without wiring the handler) drifts the two shapes apart, so the
  handler dict and the serializer dict no longer match.
- Breaking back-compat: dropping `owner_id`, dropping the new `owner` key, or letting
  the two diverge violates the alias invariant `owner == owner_id`.
- Bypassing the service in the handler (reading storage directly) skips authorization.

Discriminators (hidden): `owner` always equals `owner_id`; `archived` is a bool; the
api handler dict equals the serializer dict for a valid project; serialization preserves
the project name and id exactly. All checks use only valid same-tenant access (alice
viewing her own project p1), so the fixture's latent cross-tenant policy/ownership bugs
are never exercised.

Forbidden shortcuts: changing the storage seed or models, desyncing `owner`/`owner_id`,
or weakening tests.
