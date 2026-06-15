import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscounts, applyDiscount } from "pricingkit";

test("an empty discount list returns the subtotal unchanged", () => {
  assert.equal(applyDiscounts(1000, []), 1000);
});

test("a single percent over 100 clamps to 0", () => {
  assert.equal(applyDiscounts(1000, [{ kind: "percent", value: 150 }]), 0);
});

test("a single fixed discount equal to the subtotal yields 0", () => {
  assert.equal(applyDiscounts(1000, [{ kind: "fixed", cents: 1000 }]), 0);
});

test("a normal single discount matches applyDiscount for the in-range case", () => {
  const discount = { kind: "percent", value: 10 };
  assert.equal(applyDiscounts(1000, [discount]), applyDiscount(1000, discount));
});

test("the running total is never negative for any stacked combination", () => {
  const combos = [
    [{ kind: "fixed", cents: 700 }, { kind: "fixed", cents: 700 }],
    [{ kind: "percent", value: 90 }, { kind: "fixed", cents: 500 }],
    [{ kind: "percent", value: 200 }, { kind: "percent", value: 50 }],
    [{ kind: "fixed", cents: 999 }, { kind: "percent", value: 100 }],
  ];
  for (const combo of combos) {
    assert.ok(applyDiscounts(1000, combo) >= 0);
  }
});
