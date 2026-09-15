# Two Correct Implementations of Two Different Ideas

*Engineering at AI Speed · Episode 5*

**Two passing test suites can conceal a disagreement about the system they are supposed to build together.**

Imagine two people building parts of the same inventory application.

One is responsible for ingesting product listings from retailers. The other is building the search experience. Both use AI agents. Both work from requirements that sound reasonable.

The ingestion component preserves each retailer’s product identifier. The search component stores products using a field called `productId` as its unique key.

Each implementation passes its tests.

Then they connect the components.

Retailer North has a product numbered 417. Retailer South also has a product numbered 417. They are different products.

The search component treats the second record as an update to the first.

Nothing about the identifier’s format was invalid. The components disagreed about its scope.

Relative to their separate assumptions, both implementations were locally correct. The combined system was wrong.

## The Interface Matched. The Meaning Didn’t.

Suppose both sides agreed on a message containing `retailerId`, `productId`, and `name`, all strings.

That agreement settles part of the interface. It does not establish whether `productId` is globally unique, unique within a retailer, or a reference to some canonical product maintained elsewhere.

The ingestion developer reads it as a source identifier. The search developer reads it as an application identity.

Both can point to the same schema.

This is the uncomfortable part of integration: matching field names and types can coexist with incompatible interpretations.

Schemas are valuable. They make structural rules explicit. Their descriptions and constraints can capture more meaning too. But a structurally valid message does not, by itself, prove that both sides understand the business concept the same way.

Someone has to establish what the values mean and how consumers may use them.

## Local Evidence Has a Boundary

The ingestion tests may correctly establish that every source record preserves its retailer and product identifiers.

The search tests may correctly establish that a repeated `productId` updates an existing search record.

Those tests answer different questions.

If the search fixtures happen to contain globally distinct product identifiers, they never challenge the assumption that matters. If the ingestion tests stop at serialization, they never observe what the consumer does with those identifiers.

The tests can be well written and still leave the shared meaning untested.

AI makes this problem easier to scale. Separate agents can generate producers, consumers, fixtures, and tests from separate interpretations. Each produces a coherent little universe.

Integration is where those universes discover they have different laws of physics.

## Start With the Collision

In the example, the first useful shared test is not a large load run. It is two records:

| Retailer | Source product ID | Product |
|---|---|---|
| North | 417 | Cedar Mint |
| South | 417 | Harbor Citrus |

What should search contain after both records are ingested?

If the intended collection represents retailer listings, the answer is two distinct listings. A repeated local identifier across retailers must not merge them.

Now send an updated record for North’s 417. That should update North’s listing while leaving South’s listing intact.

Those examples reveal the identity boundary more effectively than “support multiple retailers.”

They also expose the next question: does a source identifier remain stable over the listing’s lifetime? If the provider can reuse an identifier for a different entity, retailer plus source ID may not be sufficient. Investigate that behavior instead of assuming the example has solved every identity problem.

One precise case gives the team a place to begin.

## Write an Agreement at the Boundary

The producer and consumer need a shared account of the information crossing between them.

For this illustrative system, that agreement might be:

| Concern | Shared meaning |
|---|---|
| Entity | A retailer listing, not a canonical product shared across retailers. |
| Identity scope | A source listing identifier is scoped to its retailer. The receiving system must preserve that scope. |
| Repeated identity | A later accepted record for the same listing updates that listing under the agreed ordering rule. |
| Cross-retailer matching | Matching similar listings to a canonical product is a separate capability. |
| Missing listing | Absence from one response does not establish deletion. Removal requires an explicit source signal or a separately defined complete-inventory rule. |
| Provenance | Preserve the source retailer and source identifier so a result can be traced back. |
| Unresolved behavior | Confirm identifier reuse and update-ordering behavior before relying on them. |

This is broader than the shape of a message, but it does not need to describe the whole application.

It records the assumptions that have to agree at this boundary.

Names can help. `sourceProductId` communicates more than `productId` in this case. But a clearer name still needs a definition. Renaming the field without changing the consumer’s identity logic would leave the defect intact.

## Share Examples, Then Verify Both Sides

Once the meaning is agreed, connect it to executable checks.

The producer must emit identifiers with the required source context. The consumer must preserve distinct listings. A narrow integrated exercise should demonstrate the result when both components run together.

Contract testing can help establish that the messages a consumer needs are supported by its provider. In consumer-driven approaches such as Pact, provider verification is part of that evidence; a consumer passing against its own double is not enough. [Pact: Introduction to contract testing](https://docs.pact.io/).

The chosen tests still need to express the relevant assumptions. A contract example using only one retailer will not automatically expose a collision across retailers. Nor does verifying message compatibility establish every downstream business outcome.

Use contract checks for the interaction and targeted integration checks for the behavior that spans the components.

The evidence should follow the claim.

## Integrate Before the Interpretation Spreads

Imagine discovering the collision after the search key has been reused in saved searches, reporting tables, caches, and user-facing links.

The original disagreement was small. Its consequences are now distributed throughout the application.

An adapter might help translate between representations. It cannot recover a distinction that was discarded unless some other evidence preserves it.

That is why a thin vertical slice matters: send a small, deliberately challenging example through the real path before expanding the feature.

For the listing system, that path might be source response, ingestion, persistence, search indexing, and a query that returns the two intended results.

This does not require production scale. It requires enough integration to expose the assumption.

Ask for that evidence before asking the agents to implement every filter, report, and endpoint that depends on the identity model.

## Investigate Disagreement Without Assigning It to the Wrong Layer

When two implementations collide, resist the immediate urge to patch whichever component is easier to change.

First, write down what each side believes. Then identify the business behavior the combined system must preserve.

If one interpretation violates an existing agreement, repair that implementation and add evidence that catches the violation.

If there was no agreement, make the decision explicit before treating either side as authoritative. Assess the records, interfaces, and consumers already affected. A compatibility layer or migration may be needed once the interpretation has escaped into persisted data.

The objective is a coherent system. Defending the first implementation to reach the repository will not necessarily get you one.

## Ask the Question at the Join

Before two independently developed components meet, ask both implementers to describe the same boundary example.

What entity is this? What identifies it? What does a repeated message mean? What does absence mean? Which ordering assumptions are safe? Who owns correcting a conflict?

Compare the answers while they are still short enough to read together.

Then preserve the agreed examples in tests that exercise the appropriate boundaries. Make them available to every agent working on either side.

Two implementations agreeing with themselves is a start. A working integration requires agreement about the things they share.

The next episode asks who is responsible for establishing that agreement when implementation is available to everyone on the team.
