# Working on this publication

- Read README.md and PUBLISHING.md before changing content or publishing behavior.
- Treat series.json as the publication manifest. Do not release a draft without an explicit request to publish it.
- Use TDD for builder and verification behavior: failing test, implementation, passing tests.
- Keep canonical article text in articles/ and regenerate HTML with build.py.
- Preserve the separate Engineering at AI Speed identity. Pattern Mirror is a reference, not the series title.
- Distinguish project-local definitions, established usage, assumptions, and observed behavior.
- Do not publish private business data or imply illustrative scenarios are observed incidents.
- Run tests, build.py, and verify.py before committing; inspect responsive layouts after presentation changes.
- Keep manuscripts and generated output in the same commit. No automatic future release dates.
- Keep unreleased manuscripts and private editorial materials outside this public repository.
