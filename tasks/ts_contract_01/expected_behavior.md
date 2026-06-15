# Expected behavior - ts_contract_01

The minimal correct fix sets the legacy `amount` field to `total` so the alias
stays consistent. The reference computes `total = subtotalCents(items)` and returns
`{ total, amount: total }`.

Why the obvious solution fails:
- The base code hardcodes `amount: 0`. The `total` field is computed correctly, so a
  test that only checks `total` would pass and the broken alias looks absent.
- Hidden tests check that `amount` equals `total` across several carts, including
  the empty cart where both are 0, and that `total` equals `subtotalCents(items)`.

Discriminators: `amount` always equals `total`; the empty cart yields 0 and 0;
`total` equals `subtotalCents` of the items; the fix stays in `receipt.ts` and
leaves `cart.ts` and `money.ts` untouched.
