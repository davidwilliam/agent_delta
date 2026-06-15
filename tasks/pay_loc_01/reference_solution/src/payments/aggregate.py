from payments import storage


def gross_total():
    return sum(inv.amount for inv in storage.INVOICES)
