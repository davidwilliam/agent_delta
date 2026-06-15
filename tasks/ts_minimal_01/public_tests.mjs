import { test } from "node:test";
import assert from "node:assert/strict";
import { splitEvenly } from "pricingkit";

test("splitEvenly(100, 3) distributes the remainder and sums to the total", () => {
  const parts = splitEvenly(100, 3);
  assert.deepEqual(parts, [34, 33, 33]);
  assert.equal(parts.reduce((a, b) => a + b, 0), 100);
});
