import { test } from "node:test";
import assert from "node:assert/strict";
import { receipt } from "pricingkit";

test("the legacy amount alias equals the total", () => {
  const r = receipt([
    { name: "a", unitCents: 500, qty: 1 },
    { name: "b", unitCents: 250, qty: 3 },
  ]);
  assert.equal(r.total, 1250);
  assert.equal(r.amount, 1250);
});
