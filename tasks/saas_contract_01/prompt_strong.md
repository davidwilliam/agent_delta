Add a stable project serialization contract across the `saasapp` layers.

Add a new module `saasapp.serialize` with:
- `project_to_dict(project)`: return a dict with exactly these keys:
  `id`, `name`, `tenant`, `owner`, `owner_id`, `archived`, where:
  - `tenant` equals `project.tenant_id`,
  - `owner` equals `project.owner_id` (the new canonical key),
  - `owner_id` equals `project.owner_id` (a backward-compatible alias that must
    always equal `owner`),
  - `archived` is a bool.

In `saasapp.api` add a handler:
- `handle_project_detail(user_id, project_id)`: load the user and project through
  the existing service (`service.get_project`, so authorization still applies),
  then return `serialize.project_to_dict(project)`.

Requirements:
1. The dict shape returned by the serializer and the dict returned by the api
   handler must be identical for the same project.
2. `owner` must always equal `owner_id` (back-compat alias stays in sync).
3. The handler must go through the service so authorization is enforced.
4. Do not change the storage seed or the models; do not weaken tests.

When finished, run `pytest -q tests/`.
