# “Implement This” Is Not a Requirement

*Engineering at AI Speed · Episode 4*

**An instruction starts the work. A requirement explains what the work must accomplish.**

Imagine an import job that occasionally stops when its upstream API becomes unavailable.

Someone opens a ticket: “Add retries so the import doesn’t fail.”

An AI agent wraps the operation in retry logic. It adds a delay, tries several times, and writes a test that fails twice before succeeding.

The test passes. The ticket looks done.

Then the questions arrive.

Which failures should trigger another attempt? Are we retrying a page request or the entire import? What if the user cancels while the job is waiting? How long should the application keep trying? What does the user see when recovery fails?

“Add retries” supplied a mechanism. “So the import doesn’t fail” supplied a wish.

The requirement is still missing.

## The Agent Has to Fill the Gaps Somehow

Every implementation contains decisions that were not individually dictated by the requester. That is normal. We hire engineers partly because we want them to exercise judgment.

AI agents exercise a kind of interpretive discretion too: they select patterns, infer boundaries, and choose defaults from the request and available context.

The trouble begins when a consequential decision looks like an ordinary implementation detail.

Retrying a failed read is different from repeating a workflow that has already saved records or emitted notifications. A timeout also does not prove that a remote operation had no effect. Microsoft’s retry guidance explicitly calls out idempotency and the possibility that an operation succeeded while its response failed to arrive. [Microsoft: Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry).

The agent needs enough context to recognize which decisions it can safely make and which depend on business intent or system guarantees.

“Use best practices” will not supply that context.

## Begin With the Outcome

For the importer, the outcome might be:

> A brief interruption while retrieving an inventory page should not force an operator to restart the entire import. If retrieval cannot recover within a bounded period, preserve completed work and report where the import stopped.

That gives us something to design toward.

It identifies the affected operation, explains the operational problem, and acknowledges that recovery has a limit.

It also changes the conversation. We can now discuss what “brief,” “completed,” and “where it stopped” mean in this application.

A requirement becomes useful when those questions can produce decisions rather than more adjectives.

“Reliable,” “robust,” “scalable,” and “production-ready” can express aspirations. They become acceptance criteria only when we connect them to observable behavior.

## Make the Boundary Smaller Than the Ambition

“Improve import reliability” could reasonably lead to changes in retry policies, checkpoint storage, reconciliation, logging, scheduling, and user notifications.

That might be a program of work. It is a poor boundary for one implementation task.

For this illustrative change, we can limit the task to recovery around a page-retrieval operation. We can preserve the existing destination-write and checkpoint behavior, while requiring the agent to flag any reason those mechanisms prevent the requested outcome.

That last clause matters. Scope is not an instruction to ignore a dependency that makes the task impossible.

It is an instruction to make the dependency visible before expanding the change.

The same distinction applies to exclusions. If this task does not redesign authentication, then an authentication failure should not become an invitation to invent credential-refresh behavior.

## Supply Examples That Force a Decision

Examples are useful because they make vague agreement uncomfortable.

Consider four cases:

- A page request fails with a designated temporary error, then succeeds. Continue the same import without repeating completed destination work.
- The same request keeps failing. Stop when the agreed retry budget is exhausted and report an incomplete import.
- The provider rejects the credentials. Surface the authentication problem instead of repeatedly making the same request under this policy.
- The operator cancels during a retry delay. Stop scheduling further attempts and retain the existing cancellation semantics.

These examples do not prescribe a class hierarchy or a library. They constrain behavior.

Counterexamples help too. “A completed page is imported twice because the retry wraps the entire job” makes an unwanted interpretation explicit.

A small collection of examples can reveal more disagreement than a paragraph promising comprehensive resilience.

## Write a Brief Someone Can Implement

Here is a compact brief for the example. Its numeric limits are illustrative decisions for this scenario, not universal retry recommendations.

| Part of the brief | Agreed direction |
|---|---|
| Outcome | Recover from short interruptions during inventory page retrieval without requiring a full manual restart. |
| Scope | The existing page-retrieval operation and its recovery reporting. Preserve destination-write and checkpoint semantics. |
| Eligible failures | For this exercise, retry connection failures, timeouts, and HTTP 503 from this read operation. Other failures follow existing handling. Validate this classification against the actual provider before adopting it. |
| Limits | At most three total attempts, including the first, within a 30-second operation budget. Timeouts and delays must fit within that budget. |
| Delay policy | Use the existing bounded backoff policy if present. If absent, propose the delay values before implementation. |
| Failure outcome | Preserve completed work, mark the import incomplete, and identify the page or cursor where retrieval stopped. |
| Cancellation | Cancellation prevents further attempts; preserve the application’s existing cancellation behavior. |
| Evidence | Demonstrate temporary recovery, exhausted budget, an ineligible failure, and cancellation during the wait. Verify that completed destination work is not repeated. |
| Escalation | Surface incompatible existing retries, unsafe repeated operations, or checkpoint limitations before broadening scope. |

The brief leaves room for engineering judgment. It does not specify method names, private helper functions, or how to organize every test.

It specifies the decisions that determine whether the feature means what the requester intended.

## Unknown Is a Useful Status

Sometimes the answer is genuinely unknown. Perhaps nobody has characterized the provider’s error behavior. Perhaps the client library already retries, but the team has not inspected its configuration.

Write that down.

Then make investigation the next bounded task: inspect the existing policy, collect relevant evidence, and explain how it affects the proposed behavior.

An unresolved question should not silently become a default because generation has begun.

There is an important distinction between asking the agent to investigate an unknown and asking it to decide an unanswered business question. It can inspect how cancellation works. It cannot infer, with authority, how much delay an operator is willing to tolerate.

The request should make that distinction visible.

## Test the Requirement’s Meaning

A test that verifies “the retry method was called three times” checks one implementation detail.

The requirement asks whether a temporary interruption can be recovered from, whether work is preserved, and whether the system stops under the right conditions.

Tests should provide evidence for those outcomes.

For implementation work, start with meaningful failing tests derived from the agreed examples. Then implement until the intended behavior passes. A failure because a method is missing is different from evidence that the system currently mishandles the scenario; choose the level of testing that makes that distinction useful.

Have someone review the examples as well as the code. An agent can generate both from the same mistaken interpretation.

## Stop When the Request Is Implementable

The brief does not need to anticipate every future use of the importer.

It needs enough detail to distinguish acceptable outcomes from plausible but unwanted ones, and enough boundaries to identify when a new decision is required.

A useful readiness question is: could two capable implementers read this brief and disagree about what success looks like?

They may choose different internal structures. That is fine. If they disagree about which failures are retried, whether completed work can repeat, or what cancellation means, the requirement still needs attention.

“Implement this” becomes a useful instruction when “this” has acquired an outcome, a boundary, examples, and evidence.

The next episode examines what happens when two teams each have a coherent interpretation—and their systems meet at an interface that never captured the disagreement.
