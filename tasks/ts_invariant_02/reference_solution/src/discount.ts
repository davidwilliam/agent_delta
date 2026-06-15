import { percentOfCents } from "./money.js";

export type Discount =
  | { kind: "percent"; value: number }
  | { kind: "fixed"; cents: number };

/**
 * Apply a discount to a subtotal and return the resulting total in cents.
 *
 * A total must always stay within [0, subtotalCents]: a discount can never make
 * the customer owe a negative amount, and can never be worth more than the order.
 */
export function applyDiscount(subtotalCents: number, discount: Discount): number {
  const off =
    discount.kind === "percent"
      ? percentOfCents(subtotalCents, discount.value)
      : discount.cents;
  return subtotalCents - off;
}

/**
 * Apply a list of discounts in sequence to a running total, clamping after each
 * step so the running total never drops below 0. Percent discounts compound: the
 * amount off is computed against the current running total. An empty list returns
 * the subtotal unchanged.
 */
export function applyDiscounts(subtotalCents: number, discounts: Discount[]): number {
  let runningTotal = subtotalCents;
  for (const discount of discounts) {
    const off =
      discount.kind === "percent"
        ? percentOfCents(runningTotal, discount.value)
        : discount.cents;
    runningTotal = Math.max(0, runningTotal - off);
  }
  return runningTotal;
}
