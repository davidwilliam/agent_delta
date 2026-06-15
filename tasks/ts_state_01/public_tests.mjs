import { test } from "node:test";
import assert from "node:assert/strict";
import { canTransition, transition } from "pricingkit";

test("a legal order chain advances step by step", () => {
  assert.equal(transition("pending", "paid"), "paid");
  assert.equal(transition("paid", "shipped"), "shipped");
});

test("an illegal transition out of a terminal state throws", () => {
  assert.throws(() => transition("delivered", "shipped"));
});

test("canTransition reports a legal step as true", () => {
  assert.equal(canTransition("pending", "paid"), true);
});
