Make `saasapp.subscription.change_plan` reject any transition not in `LEGAL` by
raising `ValueError`, and apply only legal ones.
