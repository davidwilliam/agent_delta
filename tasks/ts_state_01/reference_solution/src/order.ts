export type OrderStatus =
  | "pending"
  | "paid"
  | "shipped"
  | "delivered"
  | "cancelled";

/**
 * Order status state machine.
 *
 * Legal transitions:
 *   pending   -> paid
 *   paid      -> shipped
 *   shipped   -> delivered
 *   pending   -> cancelled
 *   paid      -> cancelled
 *
 * "delivered" and "cancelled" are terminal: no transition out of them is legal.
 * Skipping a step (for example pending -> shipped or pending -> delivered) is
 * illegal.
 */
const ALLOWED: Record<OrderStatus, readonly OrderStatus[]> = {
  pending: ["paid", "cancelled"],
  paid: ["shipped", "cancelled"],
  shipped: ["delivered"],
  delivered: [],
  cancelled: [],
};

export function canTransition(from: OrderStatus, to: OrderStatus): boolean {
  return ALLOWED[from].includes(to);
}

export function transition(from: OrderStatus, to: OrderStatus): OrderStatus {
  if (!canTransition(from, to)) {
    throw new Error(`illegal order transition: ${from} -> ${to}`);
  }
  return to;
}
