In the `saas` service, `sharing.access_via_token(user, token)` leaks projects across
tenants. Make it return the project only if the user is in the project's tenant, else
raise PermissionError. Keep raising KeyError for an unknown token.
