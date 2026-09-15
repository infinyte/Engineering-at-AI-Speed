# Review Starts Before Generation

*Engineering at AI Speed · Episode 8*

**The first thing to review is the interpretation that will produce the code.**

Imagine receiving a pull request that adds resumable ingestion.

The agent has changed the importer, introduced a progress store, updated several interfaces, and written a substantial test suite. The description says recovery is supported. The checks are green.

Halfway through the review, someone asks what “resume” means when the upstream inventory changes between runs.

The implementation assumes a saved page number identifies a stable position. Nobody established that the provider makes that guarantee.

The reviewer has found a design question inside a finished implementation.

This is an illustrative situation. It is also the problem this series has been approaching from different directions: an interpretation can spread through a system before the people involved agree that it is the right one.

Review still belongs at the pull request. It also belongs earlier, while the assumption is easy to see and inexpensive to change.

## Start With What the Agent Believes

Before a substantial change, ask the implementer to explain the requested outcome, the relevant existing behavior, and the assumptions the proposed approach needs.

For resumable ingestion, that explanation should point to the actual retrieval and persistence paths. It should distinguish saving a page number from preserving a reliable position in a changing source.

Then ask what evidence supports the assumptions.

Is the provider’s ordering documented? Has cursor behavior been observed? Does the emulator reproduce it because of captured evidence, or because someone chose a convenient model?

Those are different reasons for confidence.

A useful interpretation review can be short:

> We intend to recover unfinished destination work after an interruption. The current provider’s pagination stability is unresolved. We will characterize that behavior before claiming that a saved page number supports complete recovery. Meanwhile, we can test the destination write/checkpoint boundary against a fixed source scenario.

That statement identifies useful work and limits the claim it can support.

It also gives the requester an opportunity to say that the proposed outcome is wrong before it becomes a progress table and six new interfaces.

## Review the Examples Before the Implementation

An agreed outcome needs examples that distinguish success from a plausible mistake.

For the importer, choose cases such as an interruption before destination commit, an interruption after commit but before progress advances, and a source that changes while retrieval is underway.

Define what must happen in each case. Identify which answers are decisions and which depend on investigation.

Include identities in the expected result. A final count of 100 records is weak evidence if the source contained 100 specific records and one of them has been replaced by an unintended duplicate.

Have someone with the relevant domain knowledge review the examples. If two components are involved, compare their interpretations of the same case.

Asking a second agent to inspect the work can expose mistakes. It does not create independent evidence when both agents inherit the same unsupported assumption and the same incomplete fixtures.

The expected outcome needs an origin the team can explain.

## Generate One Slice That Can Disagree With You

Once the important meaning is settled, start with a thin vertical slice through the relevant path.

For this example, use a small controlled source, real destination persistence, the normal checkpoint mechanism, and an interruption followed by restart. Demonstrate the expected records before expanding to every endpoint and scheduling option.

Write the meaningful failing test first. Observe the failure, implement the behavior, and rerun it. If the failure comes from a broken fixture, fix the fixture before treating the result as evidence about recovery.

The slice should be small enough to understand but complete enough to challenge the assumption.

Generating only the progress-store class may be a small coding task. It does not yet demonstrate resumability. The useful boundary is the behavior we need to learn about.

If the slice reveals an incompatible provider behavior, update the plan while the affected implementation is still contained.

## Put Review Where It Can Change the Work

A review point is useful when its answer can alter the next action.

Here is a practical loop for a substantial integration change. It is a working approach for this series, not a prescribed industry process.

| Point in the work | Review question | Evidence or decision that moves it forward |
|---|---|---|
| Before generation | Does the interpretation match the intended outcome? | Shared definitions, examples, and explicit unknowns |
| Before expansion | Does the proposed approach survive the important boundary case? | A small integrated result, including relevant failure behavior |
| During implementation | Does this increment preserve the agreed constraints? | Focused tests, architectural checks, and inspection of the actual diff |
| Before merge | Does the complete change support its claims and fit its consumers? | Reviewed implementation, relevant regression results, and resolved exceptions |
| Before release | Can the change be introduced, observed, and recovered from? | Deployment and data-change plan, operational signals, and a named owner |
| After release | Is the system delivering the intended result under actual conditions? | Production observations and a decision to continue, stop, or correct |

These do not need to become six meetings. Several answers may fit in one brief or one review conversation.

The timing matters because a question that arrives after every dependent feature has been generated has lost much of its ability to save work.

## Review the Evidence as Carefully as the Code

“All tests passed” is useful information only when we know which tests ran and what they establish.

For the importer, a passing serializer test does not demonstrate restart behavior. A contract check does not establish that destination records remain distinct. An emulator run does not establish compatibility with provider behavior that the emulator has never been compared against.

A benchmark answers another question: how the system performs under its stated workload and environment. A faster run can still lose records.

Tie each material claim to evidence at the appropriate boundary.

The handover should identify the tested revision, the environment, the relevant cases, the results, and any skipped checks or known limitations. Evidence gathered before the last behavioral change may need to be refreshed.

This is also where we distinguish a command the agent recommends from one it actually ran. A plausible verification plan is not a verification result.

Inspect failures before explaining them away. A missing dependency, an intentionally unsupported environment, and a product regression require different responses. Record the actual reason and who accepts any unresolved limitation.

## Keep the Final Code Review

Earlier review gives the final reviewer a clearer target. It does not remove the need to inspect the implementation.

Read the changed behavior and the paths it affects. Look for unintended scope, broken compatibility, exposed data, incorrect failure handling, and tests that quietly changed the requirement to match the code.

Compare the diff with the accepted decisions. If the implementation requires a different identity rule or recovery guarantee, that is a decision to resolve rather than a detail to bury in the description.

Small increments help, but line count alone is a poor measure of review difficulty. A one-line change to a checkpoint condition may deserve more attention than a large, mechanical formatting update.

Scale the review to uncertainty and consequences.

## Release Is Another Place to Learn

Passing checks in a controlled environment leaves questions about actual traffic, source behavior, data volume, and operations.

Decide how the change will be observed and what would cause the owner to stop its rollout. For an importer, useful signals may include completed records, reconciliation differences, retry volume, unfinished jobs, and time since the last successful refresh.

Where the system supports it, a **canary release** can expose a change to a limited population before wider rollout. Its value depends on a meaningful comparison, representative use, suitable measurements, and enough time to observe the relevant behavior. A quiet canary that never exercises the changed path tells us little. [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/).

Recovery also needs a concrete meaning. Reverting application code does not necessarily reverse data already written under a new identity rule. A rollback plan may need compatibility preparation, data repair, or a compensating action. Compensation follows business rules and may not restore the exact original state. [Microsoft: Compensating Transaction](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction).

Name who watches the result and who can act. “We will monitor it” leaves both questions open.

When production reveals a new behavior, feed that evidence back into the appropriate definition, provider model, scenario, decision, or test. Otherwise, the next generated change starts with the same missing knowledge.

## The Whole Series Fits in the Next Change

We began with a word: registry.

That word carried assumptions about identity and authority into a request for a searchable collection. The same problem appeared in an API environment, where data, scenarios, runtime state, and controls needed separate meanings.

Then we looked at the conversations that development friction sometimes created, the requirements that make implementation possible, and the disagreements that local tests can leave hidden between components.

Ownership gave those decisions an address. Executable constraints gave them a way to influence future changes.

Review connects those practices in time.

On your next substantial task, ask for the interpretation and a boundary example before generating the whole feature. Resolve the decision that matters. Demonstrate one complete slice. Inspect the implementation and its evidence. Observe the released result and update what the team knows.

That is a manageable place to start. The process can grow only where experience shows that another question needs a reliable home.

AI makes it possible to produce more software, involve more contributors, and explore more ideas. Shared understanding still determines whether those changes belong in the same system.

**Keep the speed. Make the meaning, the decisions, and the evidence travel with the code.**
