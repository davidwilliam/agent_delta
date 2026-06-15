import { test } from "node:test";
import assert from "node:assert/strict";
import { orderSummary } from "pricingkit";

// A subtotal of 1000 cents taxed at 875 bps is 87.5 cents of tax, which must
// round to 88, not truncate to 87. The buggy roundCents truncates, so this fails
// at base with tax 87 and total 1087.
test("orderSummary rounds a .5 tax up to the nearest cent", () => {
  const items = [{ name: "widget", unitCents: 1000, qty: 1 }];
  const summary = orderSummary(items, 875);
  assert.equal(summary.subtotal, 1000);
  assert.equal(summary.tax, 88);
  assert.equal(summary.total, 1088);
});
