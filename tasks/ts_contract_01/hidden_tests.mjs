import { test } from "node:test";
import assert from "node:assert/strict";
import { receipt, subtotalCents } from "pricingkit";

const carts = [
  [],
  [{ name: "a", unitCents: 100, qty: 1 }],
  [
    { name: "a", unitCents: 500, qty: 1 },
    { name: "b", unitCents: 250, qty: 3 },
  ],
  [
    { name: "x", unitCents: 1, qty: 7 },
    { name: "y", unitCents: 999, qty: 2 },
    { name: "z", unitCents: 0, qty: 5 },
  ],
];

test("amount always equals total for several carts including the empty cart", () => {
  for (const items of carts) {
    const r = receipt(items);
    assert.equal(r.amount, r.total, "amount alias must equal total");
  }
});

test("the empty cart yields total 0 and amount 0", () => {
  const r = receipt([]);
  assert.equal(r.total, 0);
  assert.equal(r.amount, 0);
});

test("total equals subtotalCents of the items", () => {
  for (const items of carts) {
    const r = receipt(items);
    assert.equal(r.total, subtotalCents(items));
  }
});
