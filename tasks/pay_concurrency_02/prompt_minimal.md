Make `payments.sequence.next_id` safe under concurrent calls. Concurrent callers
must never receive duplicate ids; with N callers the ids are exactly 1..N.
