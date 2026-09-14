# Publishing the series

This is a static GitHub Pages publication. The prologue and Episode 1 are the launch release. Future episode titles and descriptions are intentionally public; their manuscripts are prepared outside the public repository.

## Season boundaries

Episode 1 explores terminology through catalog versus registry. Episode 2 explains the vocabulary of a controlled API integration environment. Later episodes cover process friction, requirements, integration divergence, ownership, executable architectural constraints, and review.

Each episode should answer one focused question. Start with a concrete situation, identify the hidden assumption, explain the engineering concept, and give the reader a useful practice. Distinguish hypothetical examples from observed behavior and project-local vocabulary from established usage.

## Release checklist

1. Complete the manuscript and source review outside the public repository.
2. Review its accuracy, tone, diagram, and practical takeaway.
3. Copy the approved manuscript to the path named by `series.json`.
4. Set its status to `published` and its date to the actual release date.
5. Run the tests, builder, and verifier as documented in README.md.
6. Preview desktop and mobile layouts, figures, tables, and navigation.
7. Commit approved sources and generated output together, then push.
8. Confirm GitHub Pages and the live URL before sharing the release.

The working editorial cadence is approximately one episode every two weeks, subject to readiness. No automatic publication or scheduled release service is configured. Dates alone do not publish articles.

## Important boundaries

- A public repository exposes every committed file. Draft status does not make a manuscript private.
- CI validates the committed output but does not regenerate and push changes automatically.
- Branch-root GitHub Pages deploys pushes to main independently of the verification job. Run checks locally before pushing; the CI job is not a deployment gate.
- Removing an episode from navigation does not erase public Git history or reader copies.
