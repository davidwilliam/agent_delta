In `mathkit.record.to_dict`, the legacy `"val"` key is `None` but must always mirror
`"value"`. Fix it without dropping the legacy key.
