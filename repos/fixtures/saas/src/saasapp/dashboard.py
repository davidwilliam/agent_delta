from saasapp import usage


def project_counts(tenant_id):
    return {"active": len(usage.active_projects(tenant_id))}
