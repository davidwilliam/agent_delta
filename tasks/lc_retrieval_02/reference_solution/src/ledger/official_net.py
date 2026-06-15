"""Official net total honoring the authoritative excluded-parts list.

The authoritative reporting policy lives in ledger.policy.official_policy and
SUPERSEDES the draft note (ledger.notes.draft_policy) and the deprecated legacy
file (ledger.legacy.old_policy). Its EXCLUDED_PARTS list names the part indices
that must be left out of any official net total.

Entry fields are named differently across parts (amount|value|amt and
kind|type|category), so a correct total must accept every schema variant; this
reuses the multi-schema extraction approach from ledger.totals.
"""

import importlib
import pkgutil
import re

from ledger import entries
from ledger.policy.official_policy import EXCLUDED_PARTS

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


def _included_parts(excluded):
    """Yield ENTRIES for every part whose index is not in `excluded`."""
    excluded = set(excluded)
    for mod in pkgutil.iter_modules(entries.__path__, entries.__name__ + "."):
        if _part_index(mod.name) not in excluded:
            yield importlib.import_module(mod.name).ENTRIES


def official_net_total():
    """Sum of credit amounts minus sum of debit amounts, across all schemas, over
    every part EXCEPT those whose index is in the authoritative EXCLUDED_PARTS."""
    credits = 0
    debits = 0
    for part in _included_parts(EXCLUDED_PARTS):
        for e in part:
            kind = _kind(e)
            if kind == "credit":
                credits += _amount(e)
            elif kind == "debit":
                debits += _amount(e)
    return credits - debits
