import { test } from "node:test";
import assert from "node:assert/strict";
import { splitEvenly } from "pricingkit";

const sum = (xs) => xs.reduce((a, b) => a + b, 0);

test("parts always sum exactly to the total for exact divisions and remainders", () => {
  const cases = [
    [100, 3],
    [100, 4],
    [99, 4],
    [1, 3],
    [1000, 7],
    [101, 5],
    [12345, 11],
  ];
  for (const [total, n] of cases) {
    const parts = splitEvenly(total, n);
    assert.equal(parts.length, n);
    assert.equal(sum(parts), total, `parts must sum to ${total} for n=${n}`);
  }
});

test("the max and min part differ by at most 1", () => {
  const cases = [
    [100, 3],
    [99, 4],
    [1000, 7],
    [101, 5],
    [12345, 11],
  ];
  for (const [total, n] of cases) {
    const parts = splitEvenly(total, n);
    assert.ok(Math.max(...parts) - Math.min(...parts) <= 1,
      `max-min must be <= 1 for total=${total} n=${n}`);
  }
});

test("every part is an integer", () => {
  for (const part of splitEvenly(100, 3)) {
    assert.ok(Number.isInteger(part));
  }
});

test("n == 1 returns the whole total as a single part", () => {
  assert.deepEqual(splitEvenly(100, 1), [100]);
  assert.deepEqual(splitEvenly(0, 1), [0]);
});

test("a total of 0 returns all zeros", () => {
  assert.deepEqual(splitEvenly(0, 4), [0, 0, 0, 0]);
});
