import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount } from "pricingkit";

test("a NaN subtotal is rejected", () => {
  assert.throws(() => applyDiscount(NaN, { kind: "percent", value: 10 }));
});

test("a negative subtotal is rejected", () => {
  assert.throws(() => applyDiscount(-100, { kind: "fixed", cents: 10 }));
});

test("a valid fixed discount still returns the same total", () => {
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 250 }), 750);
});
