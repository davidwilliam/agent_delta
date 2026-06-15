# Expected behavior - ts_state_01

The correct solution adds a new module `src/order.ts` with an explicit transition
table and re-exports it from `src/index.ts`. The reference encodes the allowed
edges as `Record<OrderStatus, readonly OrderStatus[]>`:

- pending -> paid, cancelled
- paid -> shipped, cancelled
- shipped -> delivered
- delivered -> (none, terminal)
- cancelled -> (none, terminal)

`canTransition(from, to)` checks membership in `ALLOWED[from]`. `transition`
returns `to` when `canTransition` is true and throws an `Error` otherwise, so the
two functions agree by construction.

Why the obvious solution fails:
- A model that only handles the happy-path chain (pending -> paid -> shipped ->
  delivered) often forgets the cancel edges, treats terminal states as
  transitionable (mutating a delivered or cancelled order), or allows step
  skipping such as pending -> shipped. The hidden tests exercise each of these:
  both cancel edges, both terminal states against every target, and two skip
  cases.

Discriminators: terminal states reject every outgoing transition; skipping a
step throws; both cancel edges are legal; `canTransition` matches `transition`
exactly across legal and illegal pairs; the change is confined to `src/order.ts`
and the single re-export line in `src/index.ts`.
