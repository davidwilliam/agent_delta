In the `pricingkit` TypeScript library, add a new module `src/order.ts` that
models an order status state machine, and re-export it from `src/index.ts`.

`src/order.ts` must export:

1. `export type OrderStatus = "pending" | "paid" | "shipped" | "delivered" | "cancelled";`
2. `export function canTransition(from: OrderStatus, to: OrderStatus): boolean`
   returning whether the transition is legal.
3. `export function transition(from: OrderStatus, to: OrderStatus): OrderStatus`
   returning `to` if the transition is legal, otherwise throwing an `Error`.

Legal transitions, and only these:
- pending -> paid
- paid -> shipped
- shipped -> delivered
- pending -> cancelled
- paid -> cancelled

`delivered` and `cancelled` are terminal: no transition out of them is legal.
Skipping a step (for example pending -> shipped or pending -> delivered) is
illegal. `canTransition(from, to)` must be true exactly when `transition(from, to)`
does not throw.

Requirements:
1. Add only `src/order.ts` and the one re-export line in `src/index.ts`.
2. Do not modify `src/money.ts` or `src/discount.ts`.
3. Do not weaken, skip, or delete tests.
4. Keep the patch minimal.

This package uses NodeNext module resolution, so intra-package imports use a
`.js` suffix. When finished, run `npm run build` and
`node --test tests/*.test.mjs`.
