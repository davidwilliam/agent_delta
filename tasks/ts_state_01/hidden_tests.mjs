import { test } from "node:test";
import assert from "node:assert/strict";
import { canTransition, transition } from "pricingkit";

test("shipped advances to delivered", () => {
  assert.equal(transition("shipped", "delivered"), "delivered");
});

test("paid can be cancelled", () => {
  assert.equal(transition("paid", "cancelled"), "cancelled");
});

test("delivered is terminal: every transition out throws", () => {
  for (const to of ["pending", "paid", "shipped", "delivered", "cancelled"]) {
    assert.throws(() => transition("delivered", to));
  }
});

test("cancelled is terminal: every transition out throws", () => {
  for (const to of ["pending", "paid", "shipped", "delivered", "cancelled"]) {
    assert.throws(() => transition("cancelled", to));
  }
});

test("skipping steps is illegal", () => {
  assert.throws(() => transition("pending", "delivered"));
  assert.throws(() => transition("pending", "shipped"));
});

test("canTransition agrees with transition across legal and illegal pairs", () => {
  const pairs = [
    ["pending", "paid"],
    ["paid", "shipped"],
    ["shipped", "delivered"],
    ["pending", "cancelled"],
    ["paid", "cancelled"],
    ["pending", "shipped"],
    ["pending", "delivered"],
    ["delivered", "shipped"],
    ["cancelled", "paid"],
    ["shipped", "cancelled"],
  ];
  for (const [from, to] of pairs) {
    let threw = false;
    try {
      transition(from, to);
    } catch {
      threw = true;
    }
    assert.equal(canTransition(from, to), !threw,
      `canTransition(${from}, ${to}) should match transition behaviour`);
  }
});
