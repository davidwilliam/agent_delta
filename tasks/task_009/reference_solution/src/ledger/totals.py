"""Ledger totals across every schema variant (reference solution for task_009).

The amount and kind fields are named differently in different parts, so a correct
total must accept all variants. Discovering them requires reading broadly across
the fixture.
"""

import importlib
import pkgutil

from ledger import entries

_AMOUNT_KEYS = ("amount", "value", "amt")
_KIND_KEYS = ("kind", "type", "category")


def _amount(entry):
    for key in _AMOUNT_KEYS:
        if key in entry:
            return entry[key]
    raise KeyError("entry has no amount field")


def _kind(entry):
    for key in _KIND_KEYS:
        if key in entry:
            return entry[key]
    raise KeyError("entry has no kind field")


def all_entries():
    """Yield every entry from every part."""
    out = []
    for mod in pkgutil.iter_modules(entries.__path__, entries.__name__ + "."):
        out.extend(importlib.import_module(mod.name).ENTRIES)
    return out


def total(kind):
    """Sum the amount of every entry whose kind matches, across all schemas."""
    return sum(_amount(e) for e in all_entries() if _kind(e) == kind)


def total_credits():
    return total("credit")


def total_debits():
    return total("debit")
