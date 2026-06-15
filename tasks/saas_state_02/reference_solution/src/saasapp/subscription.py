LEGAL = {("free", "pro"), ("pro", "free"), ("pro", "enterprise"), ("enterprise", "pro")}
_PLANS = {}


def reset():
    _PLANS.clear()


def plan(tenant):
    return _PLANS.get(tenant, "free")


def change_plan(tenant, new):
    current = _PLANS.get(tenant, "free")
    if (current, new) not in LEGAL:
        raise ValueError(f"illegal plan transition: {current} -> {new}")
    _PLANS[tenant] = new
    return new
