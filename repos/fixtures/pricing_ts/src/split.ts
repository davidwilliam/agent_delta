export function splitEvenly(totalCents: number, n: number): number[] {
  // BUG: drops the remainder, so the parts do not sum to totalCents
  const base = Math.floor(totalCents / n);
  return Array.from({ length: n }, () => base);
}
