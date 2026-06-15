// Tax is expressed in basis points (1 bps = 0.01%). 875 bps = 8.75%.

/** Tax owed on a subtotal at `rateBps`, rounded to the nearest cent. */
export function taxCents(subtotalCents: number, rateBps: number): number {
  return Math.round(subtotalCents * (rateBps / 10000));
}
