# Architecture Has to Become Executable

*Engineering at AI Speed · Episode 7*

**An architectural decision becomes more useful when the system can tell us that a change violates it.**

Imagine an importer with a clear recovery rule: never record a page as complete until its destination records are safely stored.

The rule is in a design document. It was discussed. Someone remembers why it matters.

Then an AI agent improves the importer. It separates progress reporting from persistence, moves a few operations, and adds tests for the new structure.

The code looks cleaner. The tests pass.

But the importer can now advance its checkpoint before the records are durable. A crash in that gap causes the next run to skip work that never finished.

The decision survived in the document. It did not survive in the system.

This is an illustrative failure, but it points to a practical question: how does an architectural decision influence the next change, especially when that change arrives faster than its original author can inspect it?

## Give the Decision Somewhere to Live

The previous episode argued that consequential decisions need accountable owners. Those owners also need a way to make the decision available beyond the meeting where it was made.

An **architecture decision record**, or **ADR**, captures a significant choice, its context, status, and consequences. Michael Nygard’s original description emphasizes preserving the reasoning and retaining superseded decisions so future contributors can understand how the architecture evolved. [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

For the importer, the record should explain why progress cannot get ahead of durable work, what repeated processing may do, and which parts of recovery the chosen design covers.

That reasoning helps someone recognize the danger in a seemingly harmless reordering.

An ADR is still prose. It can explain a guarantee without checking whether the current implementation preserves it.

We need to connect the decision to something the development process can observe.

## Turn the Decision Into a Property

“Make ingestion reliable” is difficult to enforce.

For this example, a more precise **invariant** is:

> Whenever a checkpoint marks a page complete, all destination records required for that page are durably stored.

The word “whenever” matters. This property must hold at the relevant observable boundaries, including after recovery from an interruption.

The scope matters too. The property says nothing yet about notifications, a separate search index, or whether the upstream provider changes its pagination while we read it. Those need their own guarantees.

A transaction may let us commit destination records and progress together if they share a suitable transactional boundary. Database transactions provide an all-or-nothing grouping of changes within that boundary. They do not automatically include an unrelated remote service. [PostgreSQL: Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html).

Another design may allow records to commit before progress advances, with safe reprocessing after a crash. That requires evidence about repeated effects as well as missing records.

The invariant constrains the result. The architecture explains how the system preserves it.

## Make the Wrong Behavior Fail

Here is a behavioral test specification for the illustrative importer. It is deliberately independent of a particular test framework.

| Step | What the exercise establishes |
|---|---|
| Start from known data and progress | A two-page source and an empty destination make the expected records explicit. |
| Interrupt before page one’s destination commit completes | Exercise the boundary where progress must not claim completion. |
| Inspect durable state after the interruption | If any required records are absent, the checkpoint must not mark that page complete. |
| Restart through the normal recovery path | The importer must retrieve or otherwise recover unfinished work. |
| Compare destination identities with the expected set | All required records must exist; a matching count alone could conceal a missing record and an unwanted extra. |

Begin with a meaningful failing test that exposes the violation. Then implement the change and demonstrate that the same case passes.

The interruption must affect the mechanism we are making a claim about. A mock that throws before a method call can exercise error handling. It cannot establish how a real database behaves when a process terminates during persistence.

Use the appropriate integration environment for that claim. Record what the interruption actually simulated and what it left untested.

Then exercise the other gap: records committed, checkpoint not advanced. Restart and inspect duplicate entities and any relevant side effects.

These are related cases, but they ask different questions. One looks for skipped work. The other looks for unsafe repeated work.

## Match the Check to the Constraint

Executable architecture is a working phrase for connecting architectural intent to checks that can evaluate relevant properties. It does not mean that every architectural judgment can become an automated test.

Different decisions need different forms of evidence.

| Decision | Constraint | Useful check | Limit of the evidence |
|---|---|---|---|
| Preserve source identity | Identical local IDs from different retailers remain distinct listings | Send the collision example through ingestion and search | Does not settle identifier reuse or product matching |
| Keep recovery safe | Completed progress never exceeds durable destination work | Interrupt and restart around the persistence boundary | Covers the exercised failure points and storage configuration |
| Keep domain logic independent of a provider SDK | Domain code must not depend on the provider package | Inspect dependencies with an architecture test | Does not establish runtime behavior |
| Bound page retrieval | Attempts and delays remain within the agreed budget | Exercise failures using controlled time | Does not measure production network performance |
| Preserve a consumer interaction | The provider supports the agreed request and response expectations | Verify the consumer contract against the provider | Does not establish every downstream business outcome |

Tools such as ArchUnit can check package, class, and layer dependencies in Java code. That is a concrete example of turning a structural rule into an automated check. It is not a recommendation that every team use the same language or library. [ArchUnit User Guide](https://www.archunit.org/userguide/html/000_Index.html).

A constraint earns its place by protecting a meaningful property. A test that freezes an incidental helper name may simply make a future refactor harder.

## Repository Instructions Need an Enforcement Partner

Repository guidance can tell an agent where decisions live, which boundaries apply, which checks to run, and when to ask for a new decision.

For the importer, a useful instruction might be:

> Before changing persistence or progress tracking, read the recovery decision and run its interruption tests. If the change requires a different guarantee, identify that decision before altering the tests.

That instruction makes the right action easier to find. It is not an access control or a guarantee that the action occurred.

The check also needs to run in the path where changes are accepted. A passing local command, a CI job, a required merge check, and a deployment gate are different things.

For example, GitHub can require status checks on protected branches, subject to the configured rules and bypass permissions. Merely adding a workflow file does not make its result mandatory. [GitHub: About Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Inspect the actual route from change to release. Know where a violation is reported, where it blocks progress, and who can authorize an exception.

## Check the Check

An automated check can look convincing while observing the wrong thing.

The recovery test might use a fixture that never persists progress. The dependency rule might scan a package that no longer contains the domain code. A condition might cause the important assertion to be skipped.

When the consequence warrants it, deliberately introduce the prohibited behavior in an isolated test copy and confirm that the check fails for the intended reason. This is the principle behind mutation testing: change the implementation and see whether the tests detect the change. Mutation tools distinguish detected changes from those that survive or are not exercised. [Stryker: Mutant States and Metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/).

A detected mutation gives evidence about that particular check. It does not prove the entire suite is complete.

Review the oracle too. “The expected result is whatever the current implementation returns” can preserve a defect with remarkable consistency.

## Keep the Reason and the Rule Together

Architectural decisions change as the product and its constraints change.

When a guarantee changes, update the decision, the affected interfaces, and the checks together. Explain any migration or compatibility work. Preserve the earlier rationale so someone can understand why the rule existed.

When a check is wrong, repair it. When an implementation violates a valid constraint, repair the implementation. When the decision is no longer appropriate, involve its owner.

A failing test is a request to investigate. It does not automatically mean the test should be deleted or the old architecture should remain forever.

For your next significant decision, make a small map: the reason, the property, the check, where it runs, and who maintains it. Call it a decision-to-evidence map if that name is useful; the relationship matters more than the label.

That map gives both people and agents a way to preserve intent while changing implementation.

**An architectural decision should leave evidence in the system that depends on it.**

The final episode brings these practices into the development loop: what to review before generation, what to inspect while the work is still small, and what evidence matters after the code is written.
