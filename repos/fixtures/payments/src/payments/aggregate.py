from payments import storage


def gross_total():
    # BUG: skips the first invoice (off-by-one slice)
    return sum(inv.amount for inv in storage.INVOICES[1:])
