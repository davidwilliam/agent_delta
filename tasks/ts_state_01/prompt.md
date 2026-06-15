You are working in the `pricingkit` TypeScript library.

Add an order status state machine. Create a new module `src/order.ts` and
re-export it from `src/index.ts`.

`src/order.ts` must export:
- `export type OrderStatus = "pending" | "paid" | "shipped" | "delivered" | "cancelled";`
- `canTransition(from: OrderStatus, to: OrderStatus): boolean`, returning whether
  the transition is legal.
- `transition(from: OrderStatus, to: OrderStatus): OrderStatus`, returning `to`
  if the transition is legal and throwing an `Error` otherwise.

The only legal transitions are: pending -> paid, paid -> shipped,
shipped -> delivered, pending -> cancelled, and paid -> cancelled. `delivered`
and `cancelled` are terminal, so no transition out of them is legal, and skipping
a step (for example pending -> shipped) is illegal. `canTransition` must be true
exactly when `transition` does not throw.

This package uses NodeNext module resolution, so intra-package imports use a
`.js` suffix. Keep the change minimal: add `src/order.ts` and a single re-export
line in `src/index.ts`, and do not modify the other modules. When finished, run
`npm run build` and `node --test tests/*.test.mjs`, then summarize the change.

## Required API (the tests import these exact names)

- Package `pricingkit` exporting `canTransition(from: OrderStatus, to: OrderStatus): boolean` and `transition(from: OrderStatus, to: OrderStatus): OrderStatus` (throws on an illegal transition), where `OrderStatus` is one of `"pending" | "paid" | "shipped" | "delivered" | "cancelled"`.
