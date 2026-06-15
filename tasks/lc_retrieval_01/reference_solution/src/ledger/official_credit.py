"""Official credit total using the authoritative reporting cutoff.

The authoritative reporting policy lives in ledger.policy.official_policy and
SUPERSEDES the draft note (ledger.notes.draft_policy) and the deprecated legacy
file (ledger.legacy.old_policy). Only parts whose index is strictly less than the
authoritative REPORTING_CUTOFF are included in any official total.

Entry fields are named differently across parts (amount|value|amt and
kind|type|category), so a correct total must accept every schema variant; this
reuses the multi-schema extraction approach from ledger.totals.
"""

import importlib
import pkgutil
import re

from ledger import entries
from ledger.policy.official_policy import REPORTING_CUTOFF

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


def _part_index(module_name):
    return int(re.search(r"part_(\d+)$", module_name).group(1))


def _parts_below(cutoff):
    """Yield ENTRIES for every part whose index is strictly less than cutoff."""
    for mod in pkgutil.iter_modules(entries.__path__, entries.__name__ + "."):
        if _part_index(mod.name) < cutoff:
            yield importlib.import_module(mod.name).ENTRIES


def official_credit_total():
    """Sum the amount of every credit entry, across all schemas, but only from
    parts whose index is strictly less than the authoritative REPORTING_CUTOFF."""
    return sum(
        _amount(e)
        for part in _parts_below(REPORTING_CUTOFF)
        for e in part
        if _kind(e) == "credit"
    )
