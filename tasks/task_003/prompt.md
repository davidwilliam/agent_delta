You are working in the `mathkit` Python package repository.

Please add a `slugify` function to the text module so titles can be turned into
URL-friendly slugs.

Add `slugify(text)` in `src/mathkit/text.py` with this behavior:
1. Lowercase the text.
2. Replace every run of non-alphanumeric characters (spaces, punctuation, etc.)
   with a single hyphen `-`.
3. Strip any leading or trailing hyphens.
4. `slugify("Hello, World!")` must return `"hello-world"`.
5. Export `slugify` from the `mathkit` package so `from mathkit import slugify`
   works.

Keep the change minimal and consistent with existing conventions. When finished,
run `pytest -q tests/` and summarize what you changed.
