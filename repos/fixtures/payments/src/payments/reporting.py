from payments import aggregate, storage


def summary():
    return {"gross": aggregate.gross_total(), "count": len(storage.INVOICES)}
