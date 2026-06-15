import { subtotalCents, LineItem } from "./cart.js";
import { roundCents } from "./rounding.js";

export interface OrderSummary {
  subtotal: number;
  tax: number;
  total: number;
}

/** Build an order summary: subtotal, tax at `taxRateBps`, and the grand total. */
export function orderSummary(items: LineItem[], taxRateBps: number): OrderSummary {
  const subtotal = subtotalCents(items);
  const tax = roundCents(subtotal * (taxRateBps / 10000));
  return { subtotal, tax, total: subtotal + tax };
}
