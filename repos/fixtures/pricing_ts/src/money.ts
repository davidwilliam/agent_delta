// Integer-cents money helpers. All amounts are whole cents to avoid float drift.

/** The discount/tax amount for `percent` of `amountCents`, rounded to the nearest cent. */
export function percentOfCents(amountCents: number, percent: number): number {
  return Math.round(amountCents * (percent / 100));
}

/** Format whole cents as a USD string, e.g. 1234 -> "$12.34", -50 -> "-$0.50". */
export function formatUSD(cents: number): string {
  const sign = cents < 0 ? "-" : "";
  const abs = Math.abs(cents);
  const dollars = Math.floor(abs / 100);
  const remainder = (abs % 100).toString().padStart(2, "0");
  return `${sign}$${dollars}.${remainder}`;
}
