"""Baseline tests for the ledger fixture (structure only)."""

from ledger.entries import part_000, part_001


def test_parts_load():
    assert len(part_000.ENTRIES) == 110
    assert len(part_001.ENTRIES) == 110


def test_schema_variants_differ():
    # part_000 is variant 0 (amount/kind); part_001 is variant 1 (value/type).
    assert "amount" in part_000.ENTRIES[0]
    assert "value" in part_001.ENTRIES[0]
