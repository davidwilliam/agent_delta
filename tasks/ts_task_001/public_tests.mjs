import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount } from "pricingkit";

test("a fixed discount larger than the subtotal yields 0, not a negative total", () => {
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 1500 }), 0);
});
