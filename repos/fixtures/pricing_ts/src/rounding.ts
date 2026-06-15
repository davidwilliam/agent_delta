// Round a fractional cents amount to a whole number of cents.

/** Round to the nearest whole cent. */
export function roundCents(x: number): number {
  return Math.trunc(x);
}
