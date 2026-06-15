"""Stable project serialization contract (reference solution for saas_contract_01).

project_to_dict is the single source of truth for the wire shape of a project.
The canonical owner key is "owner"; "owner_id" is a backward-compatible alias and
must always equal "owner".
"""


def project_to_dict(project):
    """Serialize a Project into its stable dict contract.

    Keys: id, name, tenant, owner, owner_id, archived. "tenant" mirrors
    project.tenant_id, "owner" is the canonical owner key, and "owner_id" is a
    back-compat alias that always equals "owner".
    """
    owner = project.owner_id
    return {
        "id": project.id,
        "name": project.name,
        "tenant": project.tenant_id,
        "owner": owner,
        "owner_id": owner,
        "archived": bool(project.archived),
    }
