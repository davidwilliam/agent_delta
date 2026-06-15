import { subtotalCents, LineItem } from "./cart.js";

export interface Receipt { total: number; amount: number; }

export function receipt(items: LineItem[]): Receipt {
  const total = subtotalCents(items);
  return { total, amount: total };
}
