Make `saasapp.provisioning.assign` safe under concurrent assignment. Concurrent
assignments to one tenant must never exceed its seat limit.
