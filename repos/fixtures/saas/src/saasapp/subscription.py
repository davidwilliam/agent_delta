LEGAL = {("free", "pro"), ("pro", "free"), ("pro", "enterprise"), ("enterprise", "pro")}
_PLANS = {}


def reset():
    _PLANS.clear()


def plan(tenant):
    return _PLANS.get(tenant, "free")


def change_plan(tenant, new):
    # BUG: does not validate the transition; allows illegal jumps
    _PLANS[tenant] = new
    return new
