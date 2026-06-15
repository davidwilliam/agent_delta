import { test } from "node:test";
import assert from "node:assert/strict";
import { orderSummary } from "pricingkit";

// Each case taxes a subtotal at a basis-point rate. The tax must be rounded to
// the nearest whole cent, and the total must always equal subtotal + tax.
const cases = [
  // subtotal, rateBps, rawTax, expectedTax, note
  [1000, 875, 87.5, 88], // .5 rounds up
  [1500, 833, 124.95, 125], // fraction above .5 rounds up
  [333, 175, 5.8275, 6], // fraction above .5 rounds up
  [1234, 1234, 152.2756, 152], // fraction below .5 rounds down
  [2000, 625, 125.0, 125], // exact: truncation and rounding agree
  [1000, 0, 0, 0], // zero tax unchanged
];

for (const [subtotal, rateBps, , expectedTax] of cases) {
  test(`orderSummary taxes ${subtotal} at ${rateBps} bps as ${expectedTax}`, () => {
    const items = [{ name: "item", unitCents: subtotal, qty: 1 }];
    const summary = orderSummary(items, rateBps);
    assert.equal(summary.subtotal, subtotal);
    assert.equal(summary.tax, expectedTax);
    assert.equal(summary.total, subtotal + expectedTax);
  });
}

test("orderSummary total always equals subtotal plus tax across multi-item carts", () => {
  const items = [
    { name: "a", unitCents: 499, qty: 3 },
    { name: "b", unitCents: 250, qty: 2 },
  ];
  // subtotal = 499*3 + 250*2 = 1497 + 500 = 1997; 1997 * 0.0875 = 174.7375 -> 175
  const summary = orderSummary(items, 875);
  assert.equal(summary.subtotal, 1997);
  assert.equal(summary.tax, 175);
  assert.equal(summary.total, summary.subtotal + summary.tax);
});
