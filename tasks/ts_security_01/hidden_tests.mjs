import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount } from "pricingkit";

test("an Infinity subtotal is rejected", () => {
  assert.throws(() => applyDiscount(Infinity, { kind: "percent", value: 10 }));
});

test("a non-integer subtotal is rejected", () => {
  assert.throws(() => applyDiscount(10.5, { kind: "fixed", cents: 10 }));
});

test("a fixed discount with non-integer cents is rejected", () => {
  assert.throws(() => applyDiscount(1000, { kind: "fixed", cents: 12.5 }));
});

test("a negative percent value is rejected", () => {
  assert.throws(() => applyDiscount(1000, { kind: "percent", value: -5 }));
});

test("valid percent and fixed calls still return the same numbers as before", () => {
  assert.equal(applyDiscount(1000, { kind: "percent", value: 10 }), 900);
  assert.equal(applyDiscount(2000, { kind: "fixed", cents: 500 }), 1500);
  assert.equal(applyDiscount(1000, { kind: "percent", value: 0 }), 1000);
  assert.equal(applyDiscount(1000, { kind: "fixed", cents: 0 }), 1000);
});
