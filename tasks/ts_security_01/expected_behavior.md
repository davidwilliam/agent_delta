# Expected behavior - ts_security_01

The minimal correct fix ADDS input validation to `applyDiscount` and throws an
`Error` on invalid input, while leaving the valid-input computation untouched.

Validation rules:
- `subtotalCents` must be a finite, non-negative integer (`Number.isInteger`
  and `>= 0`); otherwise throw.
- For a `fixed` discount, `cents` must be a finite, non-negative integer;
  otherwise throw.
- For a `percent` discount, `value` must be a finite number `>= 0`; otherwise
  throw.

Why the obvious solution fails:
- The base code computes `off` and returns the total directly, trusting its
  inputs. NaN, Infinity, a non-integer subtotal, a non-integer fixed `cents`, or
  a negative amount flow straight through and yield NaN or a nonsense total, so
  no `Error` is thrown and the throw-expecting tests fail.
- LLMs commonly handle the happy path and trust the inputs, returning NaN or a
  negative total on adversarial values.

Discriminators: adversarial inputs throw; valid inputs return the same numbers
as before (for example `applyDiscount(1000, { kind: "fixed", cents: 250 })` is
still `750`); the fix stays in `discount.ts` and leaves `money.ts` and the
`Discount` type untouched.

Note: the base code can return a clamped total for over-large valid discounts;
that behaviour is intentional and is NOT changed by this task.
