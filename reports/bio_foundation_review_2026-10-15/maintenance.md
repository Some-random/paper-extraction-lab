# Maintaining the literature review

Edit [review.json](review.json), then run `python3 scripts/render_foundation_catalog.py` from the repository root. This produces the review, supporting pages, study pages and [numeric CSV](catalog.csv) from one registry.

The `presentation` record selects the review section, starting checkpoint and one overview budget, with explicit content scope and quantity type. It must cite initialization evidence. Keep every original budget in `token_budgets`; selecting an overview row never changes a reported amount. CPT studies belong with CPT models regardless of publication type. Do not classify instruction tuning, contrastive learning or random initialization as CPT.

The [token audit](token_budget_verification.json) records numerical checks and source snapshots. [Archived references](archive.md) preserve earlier out-of-scope material.

Evaluation protocols, benchmark cases and runs live in the separate private [bio-evaluation repository](https://github.com/Some-random/bio-evaluation). This repository holds extraction work and public literature notes. Private evaluation links remain in the registry as provenance, not public review navigation.
