def to_dict(name, value):
    # BUG: legacy "val" alias must equal "value" but is None
    return {"name": name, "value": value, "val": None}
