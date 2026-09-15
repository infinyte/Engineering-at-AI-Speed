# When Everyone Can Implement, Who Owns the Architecture?

*Engineering at AI Speed · Episode 6*

**The ability to create a change has expanded. Responsibility for its consequences still needs an owner.**

Imagine a product owner using an AI agent to improve a product-search workflow.

The prototype works. It imports sample records, removes what appear to be duplicates, and presents a clean search experience.

At the same time, an engineer is improving ingestion from multiple retailers. That implementation deliberately preserves separate source listings because similar products are not necessarily the same entity.

Both people are advancing the product. Both can generate code that runs.

Then someone asks whether the search workflow should merge those listings.

The product owner assumed that was obvious. The engineer assumed the existing identity rules settled it. Neither realized the other was making a decision at the same boundary.

This is an illustrative example, but the organizational question is practical: when more people can implement, who has the authority and responsibility to settle the architectural consequences?

## Implementation Used to Contain an Informal Checkpoint

In many teams, a person describing a business need depended on an engineer to turn it into software.

That translation often included more than coding. The engineer asked questions, interpreted terminology, checked existing conventions, and noticed when a request crossed a system boundary.

It was an imperfect arrangement. Useful knowledge could become concentrated in a few people. A team could mistake “the person who knows the code” for “the person who should make every decision.”

Still, the dependency created an informal checkpoint. Someone with implementation context usually encountered the request before it became a repository change.

AI allows more people to move past that checkpoint. A product owner can build a prototype. An analyst can automate a recurring task. A designer can implement an interaction and test whether it communicates the intended behavior.

Those are valuable capabilities. The translation work remains necessary, but we can no longer assume it will happen simply because coding passes through a particular person.

## Authorship Does Not Settle Ownership

The person who writes a change is not automatically the right person to decide every consequence of that change.

That was true before AI. A senior engineer can misunderstand a business rule. A product owner can understand an operational consequence that never appears in the code. A support specialist may know exactly why an apparently redundant field cannot disappear.

Architectural decisions draw on different kinds of knowledge.

In the listing example, product needs to explain the experience users require. Someone must understand the source data and its identity limits. Engineering must assess how a matching decision propagates through persistence, interfaces, and downstream consumers.

The agent can investigate and propose options. It does not become the accountable owner because it generated the implementation.

> Code authorship tells us who produced the change. Decision ownership tells us who must answer for the guarantee it changes.

The team needs both to be clear.

## Assign Ownership to Decisions

“Architecture belongs to the architects” is not enough guidance for a person deciding whether to merge two listings.

Which decisions can they make within the existing boundaries? Which ones require input? Who can resolve a disagreement, and how quickly?

A useful starting point is a small decision-rights table. The roles below are an example; one person may hold several roles in a smaller team.

| Decision | Accountable owner | Required input | What contributors can decide within the boundary |
|---|---|---|---|
| User outcome and acceptance | Product owner | Engineering and affected users or operations | Implementation details that preserve the agreed outcome |
| Shared identity and data meaning | Named domain owner | Product and affected service owners | Local representations that preserve the shared definition |
| Service behavior and internal design | Service owner | Consumers when a contract or guarantee changes | Internal structure within existing contracts and constraints |
| Cross-service interface change | Named interface owner | Provider and affected consumer owners | Compatible implementation changes under the agreed contract |
| Access and data exposure | Named security or data-policy owner | Product and service owners | Changes already permitted by the established policy |
| Production release readiness | Release or service owner | Verification evidence and operational readiness | Changes within an explicitly delegated release process |

The value is not in the table’s size. It is in whether a contributor can find the right decision-maker before the work expands.

“Everyone owns it” can express a healthy sense of care. It is a poor escalation address.

## Ownership Must Be Available

There is an easy way to make this model fail: appoint one architect as the mandatory approver for everything and then fill that person’s calendar.

The team has replaced an informal bottleneck with a documented one.

Decision owners need to publish the boundaries within which others can work. They also need a practical way to answer questions outside those boundaries, with a delegate when they are unavailable.

Most changes should not require a fresh architectural verdict. A contributor should be able to improve an internal function, adjust a display, or extend a tested behavior when the relevant guarantees remain intact.

The reason to involve an owner is a decision that changes or exceeds those guarantees—not the mere presence of generated code.

For example: improving search ranking within an agreed listing model is different from silently merging listings into canonical products. The first may fit existing authority. The second changes the meaning of the data.

## Make Architectural Knowledge Accessible

A boundary that exists only in a senior engineer’s memory is difficult for other people to follow and impossible for an agent to reliably retrieve.

Put important definitions, decisions, and constraints where contributors work. Link them from the feature brief and repository guidance. Include an owner and enough rationale to explain why the boundary exists.

“Do not merge retailer listings automatically” is more useful when accompanied by the reason: similar names and package sizes do not establish shared product identity, and downstream systems depend on source-specific records remaining distinct.

That explanation helps people recognize related cases. It also lets them challenge the rule intelligently when the product’s needs change.

Documentation can become stale. Ownership includes keeping the decision current, recording exceptions, and retiring constraints that no longer apply.

An old rule with no reachable owner can be as obstructive as having no rule at all.

## Give Exploration Room Without Losing Its Status

A prototype can answer a valuable question before the production design is settled.

The product owner in our example might build a search experience that groups similar listings to see whether users find it helpful. That experiment does not have to wait until every identity question is resolved.

But its assumptions need to be visible. Grouping sample data for a demonstration should not quietly become an authoritative merge policy in production.

Keep the experiment’s purpose, data limitations, and intended lifespan clear. Before adopting it, identify which decisions need production owners and what evidence supports them.

The same rule applies to engineers. Calling an experiment a technical spike does not settle the decisions it postponed.

Exploration earns its value by teaching us something. Adoption requires evaluating what remains unresolved.

## Handover Includes Consequences

When a contributor offers an AI-generated change for integration, the handover should explain more than which files changed.

What behavior is different? Which existing guarantees does it rely on? Which assumptions were made? What evidence supports the result? Who will maintain and operate it?

For the search change, that might be: the interface groups listings visually but preserves source identities, makes no canonical identity claim, and allows users to inspect the underlying listings.

That statement gives reviewers something meaningful to assess. It also gives the domain owner a clear decision if the product later wants persistent merging.

Ownership becomes practical when it follows a concrete consequence through the system.

## Accountability Should Support Participation

The purpose of decision ownership is to help more people contribute without forcing each person to rediscover the entire architecture.

A product owner should be able to build a useful experiment. An analyst should be able to improve a workflow. An engineer should be able to act within established constraints without waiting for ceremonial permission.

They all need a visible answer when a change reaches beyond those constraints.

Start with the next shared decision your team encounters. Name the accountable owner, identify who must contribute, write down the boundary, and make the result available to the people and agents doing the work.

Architecture remains a collaborative activity. Accountability makes that collaboration easier to navigate.

As implementation becomes more widely available, we need fewer assumptions about who will happen to catch a problem—and clearer responsibility for the guarantees the system makes.

In the next episode, we will turn those guarantees into constraints that can be checked: schemas, contracts, invariants, tests, and repository rules that make architectural decisions executable.
