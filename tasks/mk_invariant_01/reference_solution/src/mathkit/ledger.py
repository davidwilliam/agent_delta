"""Apply a sequence of transactions to a balance (reference solution for mk_invariant_01).

The invariant is that the running balance never goes below zero. A withdrawal that
would overdraw is rejected with ValueError before it is applied, so a rejected
withdrawal never partially applies. Deposits always apply.
"""

from collections.abc import Iterable


def apply_transactions(start_balance: int, transactions: Iterable[int]) -> int:
    """Apply each transaction in order to a running balance and return the final balance.

    Positive transactions are deposits and always apply. Negative transactions are
    withdrawals; a withdrawal that would drive the balance below zero is rejected
    with ValueError and is not applied. A negative start_balance raises ValueError.
    """
    if start_balance < 0:
        raise ValueError("start_balance must be non-negative")
    balance = start_balance
    for amount in transactions:
        new_balance = balance + amount
        if new_balance < 0:
            raise ValueError("withdrawal would overdraw the balance")
        balance = new_balance
    return balance
