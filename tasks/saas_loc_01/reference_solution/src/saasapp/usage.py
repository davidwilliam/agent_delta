from saasapp import storage


def active_projects(tenant_id):
    return [
        p for p in storage.all_projects()
        if p.tenant_id == tenant_id and not p.archived
    ]
