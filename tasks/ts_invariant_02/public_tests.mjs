import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscounts } from "pricingkit";

test("stacked percent then fixed compounds on the running total", () => {
  assert.equal(
    applyDiscounts(1000, [
      { kind: "percent", value: 10 },
      { kind: "fixed", cents: 100 },
    ]),
    800,
  );
});

test("two large fixed discounts clamp the running total to 0, never negative", () => {
  assert.equal(
    applyDiscounts(1000, [
      { kind: "fixed", cents: 600 },
      { kind: "fixed", cents: 600 },
    ]),
    0,
  );
});
