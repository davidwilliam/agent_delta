import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount } from "pricingkit";

test("a percentage discount over 100% clamps to 0", () => {
  assert.equal(applyDiscount(1000, { kind: "percent", value: 150 }), 0);
});

test("a fixed discount equal to the subtotal yields 0", () => {
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 1000 }), 0);
});

test("zero discounts leave the subtotal unchanged", () => {
  assert.equal(applyDiscount(1000, { kind: "percent", value: 0 }), 1000);
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 0 }), 1000);
});

test("normal in-range discounts are unaffected by the clamp", () => {
  assert.equal(applyDiscount(1000, { kind: "percent", value: 10 }), 900);
  assert.equal(applyDiscount(2000, { kind: "fixed", cents: 500 }), 1500);
});
