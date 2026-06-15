import { subtotalCents, LineItem } from "./cart.js";

export interface Receipt { total: number; amount: number; }

export function receipt(items: LineItem[]): Receipt {
  const total = subtotalCents(items);
  // BUG: "amount" is a legacy alias that must equal total, but is set to 0
  return { total, amount: 0 };
}
