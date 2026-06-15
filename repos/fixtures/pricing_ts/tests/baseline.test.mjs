// Baseline suite: the happy-path behaviour that must keep working. It imports the
// package by name (Node self-reference via package.json "exports"), so it runs
// against the compiled dist/ output.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  subtotalCents,
  applyDiscount,
  taxCents,
  percentOfCents,
  formatUSD,
} from "pricingkit";

test("subtotalCents sums line items", () => {
  const items = [
    { name: "a", unitCents: 500, qty: 2 },
    { name: "b", unitCents: 250, qty: 1 },
  ];
  assert.equal(subtotalCents(items), 1250);
});

test("applyDiscount handles a normal percentage", () => {
  assert.equal(applyDiscount(1000, { kind: "percent", value: 10 }), 900);
});

test("applyDiscount handles a normal fixed amount", () => {
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 250 }), 750);
});

test("taxCents rounds to the nearest cent", () => {
  assert.equal(taxCents(1000, 875), 88);
});

test("percentOfCents and formatUSD", () => {
  assert.equal(percentOfCents(1000, 10), 100);
  assert.equal(formatUSD(1234), "$12.34");
});
