// A shopping cart is a list of line items priced in whole cents.

export interface LineItem {
  name: string;
  unitCents: number;
  qty: number;
}

/** Sum of unitCents * qty over all line items. */
export function subtotalCents(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.unitCents * item.qty, 0);
}
