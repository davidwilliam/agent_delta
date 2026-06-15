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
  return Math.max(0, subtotalCents - off);
}
