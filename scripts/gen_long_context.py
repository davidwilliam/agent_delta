#!/usr/bin/env python
"""Deterministically generate the long_context fixture (SPEC 21).

A ledger split across many part_*.py files. The entry schema varies by part
(three variants of the amount/kind field names), so computing a correct total
requires discovering every variant, which means reading broadly across the
fixture rather than inferring the structure from one file. The output is
committed; rerun this only to regenerate. No randomness, so it is reproducible.

Usage: python scripts/gen_long_context.py
"""

from __future__ import annotations

from pathlib import Path

N_PARTS = 220
PER_PART = 110

ROOT = Path(__file__).resolve().parent.parent / "repos" / "fixtures" / "long_context"
ENTRIES_DIR = ROOT / "ledger" / "entries"

SCHEMAS = [
    ('{{"amount": {amt}, "kind": "{kind}"}}'),
    ('{{"value": {amt}, "type": "{kind}"}}'),
    ('{{"amt": {amt}, "category": "{kind}"}}'),
]


def entry_values(idx: int) -> tuple[int, str]:
    amount = (idx % 50) + 1
    kind = "credit" if idx % 3 == 0 else "debit"
    return amount, kind


def expected_totals() -> dict[str, int]:
    credit = debit = 0
    for idx in range(N_PARTS * PER_PART):
        amount, kind = entry_values(idx)
        if kind == "credit":
            credit += amount
        else:
            debit += amount
    return {"credit": credit, "debit": debit, "n_entries": N_PARTS * PER_PART, "n_parts": N_PARTS}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def generate() -> dict[str, int]:
    write(ROOT / "pyproject.toml",
          '[project]\nname = "ledger"\nversion = "0.1.0"\nrequires-python = ">=3.9"\n'
          'dependencies = []\n\n[project.optional-dependencies]\ndev = ["pytest>=7.0"]\n\n'
          '[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n\n'
          '[tool.setuptools.packages.find]\nwhere = ["src"]\n')
    write(ROOT / "src" / "ledger" / "__init__.py",
          '"""ledger: a large, multi-schema ledger (AgentDelta long-context fixture)."""\n'
          '__version__ = "0.1.0"\n')
    write(ROOT / "src" / "ledger" / "entries" / "__init__.py",
          '"""Ledger entries split across many parts with varying field schemas."""\n')

    for p in range(N_PARTS):
        variant = p % 3
        lines = [f'"""Ledger part {p:03d} (schema variant {variant}); generated."""',
                 "", "ENTRIES = ["]
        for j in range(PER_PART):
            amount, kind = entry_values(p * PER_PART + j)
            lines.append("    " + SCHEMAS[variant].format(amt=amount, kind=kind) + ",")
        lines.append("]\n")
        write(ROOT / "src" / "ledger" / "entries" / f"part_{p:03d}.py", "\n".join(lines))

    totals = expected_totals()
    # Baseline test: structure only (totals.py does not exist at base).
    write(ROOT / "tests" / "test_ledger.py",
          '"""Baseline tests for the ledger fixture (structure only)."""\n\n'
          "from ledger.entries import part_000, part_001\n\n\n"
          "def test_parts_load():\n"
          f"    assert len(part_000.ENTRIES) == {PER_PART}\n"
          f"    assert len(part_001.ENTRIES) == {PER_PART}\n\n\n"
          "def test_schema_variants_differ():\n"
          "    # part_000 is variant 0 (amount/kind); part_001 is variant 1 (value/type).\n"
          '    assert "amount" in part_000.ENTRIES[0]\n'
          '    assert "value" in part_001.ENTRIES[0]\n')
    return totals


if __name__ == "__main__":
    totals = generate()
    approx_tokens = sum(len(p.read_text()) for p in ROOT.rglob("*.py")) // 4
    print(f"Generated {totals['n_parts']} parts, {totals['n_entries']} entries.")
    print(f"Approx content tokens: {approx_tokens:,}")
    print(f"Expected totals: {totals}")
