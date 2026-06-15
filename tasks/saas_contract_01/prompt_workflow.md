Follow this process to add a stable project serialization contract to `saasapp`:

1. Read `models.py`, `service.py`, and `api.py` to see how a Project is shaped and
   how `service.get_project(user, project_id)` enforces authorization.
2. State the contract: the exact dict keys (`id`, `name`, `tenant`, `owner`,
   `owner_id`, `archived`), which fields map to which Project attributes, and the
   back-compat rule that `owner` and `owner_id` must always be equal.
3. Add a new `saasapp.serialize` module with `project_to_dict(project)` producing
   that dict.
4. Add `handle_project_detail(user_id, project_id)` to `api.py` that loads the
   project via `service.get_project` (so authorization still applies) and returns
   `serialize.project_to_dict(project)`.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm the serializer and the api handler return an identical
   dict, that `owner` equals `owner_id`, and that the storage seed and models are
   unchanged.
