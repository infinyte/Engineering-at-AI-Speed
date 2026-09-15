# The Friction We Lost

*Engineering at AI Speed · Episode 3*

**Some development friction was carrying information. What happens when we remove the delay but still need the conversation?**

Imagine asking an AI agent to add resumable ingestion to an application.

The request sounds straightforward: import the records, save progress, and pick up where you left off if the process stops.

The agent gets to work. It adds a progress table, updates the import loop, writes tests, and produces a working implementation.

Then someone reviewing the change asks: “What happens if the records are saved, but the process crashes before progress is updated?”

Good question.

Someone else asks the inverse: “What happens if progress is updated before the records are safely saved?”

Also a good question.

The answers affect whether the importer repeats work or skips it. They belong in the design of resumability. But in this example, they arrive after the implementation.

The code got there before the conversation did.

## The Conversation Used to Have More Places to Happen

In a more manual workflow, that question might have surfaced while an engineer investigated the existing importer. It might have come up during a design discussion, test planning, or a conversation with whoever owned the destination database.

There were several opportunities to notice that “save progress” concealed a decision about failure behavior.

None of those opportunities guaranteed that someone would ask. Traditional development has an impressive history of taking a long time to get things wrong.

But implementation consumed enough effort that investigation and coordination often happened along the way.

AI changes that relationship. An agent can make implementation choices and express them in code while people are still deciding what the request means.

The uncertainty has not disappeared. It has acquired an implementation.

In the first episode, we looked at how an ambiguous word can become architecture. In the second, we used a difficult API integration to distinguish the data, setup, runtime state, and controls in a test environment.

Now we need to examine the process around those decisions: where did we used to discover that we disagreed, and what replaces that discovery when implementation accelerates?

## Some Friction Was Carrying Information

“Reduce friction” has been a sensible objective for a long time.

Slow builds, repetitive setup, confusing deployment procedures, and unnecessary handoffs consume time that could go toward useful work. There is no virtue in making an engineer wait forty minutes for feedback that could arrive in forty seconds.

But development friction was a mixed bag.

A meeting might be a calendar obligation with no useful outcome. It might also be the place where the person who understood a failure mode finally met the person changing the system.

A design document might be written once and ignored forever. It might also force its author to notice that two requirements could not both be satisfied.

A code review might obsess over formatting. It might also reveal that a locally reasonable change violates a guarantee another component depends on.

The visible activity and its useful function are different things.

> Some friction was carrying information.

If we remove an activity, we should understand whether it was doing useful work—and where that work will happen afterward.

## Waiting Does Not Produce Understanding

A ticket sitting in a queue is not becoming more precise.

A pull request waiting three days for review is not accumulating architectural insight through exposure to office air.

Time only helps when something useful happens inside it: a question is asked, a dependency is investigated, an assumption is challenged, or a decision is made.

That distinction matters because the wrong response to AI speed is to insert an arbitrary pause and call the process safer.

What would we expect to learn during that pause? Who needs to contribute? What decision might change because of the answer?

If we cannot answer those questions, the pause is difficult to justify.

The goal is to make useful inquiry deliberate. Development should not depend on an engineer happening to discover a consequential assumption while doing something else.

## What Was the Old Process Actually Doing?

Before replacing a development step, examine the function it performed when it worked well.

| Familiar activity | Useful function it sometimes performed | A lighter way to preserve that function |
|---|---|---|
| Requirements discussion | Exposed different interpretations of the request | Record the intended outcome and one boundary example; have the relevant people resolve disagreement |
| Design review | Made consequential choices visible | Write a short decision note for changes involving ownership, persistence, contracts, or failure behavior |
| Implementation investigation | Revealed dependencies and existing conventions | Have the agent identify the relevant system boundaries and cite the code it inspected before making changes |
| Test planning | Asked how the feature could fail | Choose a representative failure case and define the expected outcome before implementation expands |
| Integration handoff | Reconciled assumptions between components | Exercise one shared example across the boundary early |
| Code review | Challenged the implementation against intent | Review a bounded change alongside its decisions and evidence |

These are possible replacements, not six mandatory steps for every task.

The point is to identify what we need to learn and arrange a direct way to learn it.

A short written exchange can resolve a decision. A meeting can be the most efficient option when several people hold different parts of the answer. The format should serve the question.

## Replace the Missing Conversation in the Importer Example

Return to resumable ingestion.

Before asking for the complete implementation, ask the agent to explain where destination writes become durable, where progress is recorded, and what happens if the process stops between those events.

That explanation should reference the existing system. A generic paragraph about reliable imports is not enough.

Suppose the agent proposes saving records and then recording progress. It should make the consequence explicit: a crash between those operations may cause the same records to be processed again.

Now we can ask the important question: is repeated processing safe in this application?

The answer might depend on identifiers, uniqueness rules, updates, or side effects. Writing the same business record twice might also trigger a notification twice. “We handle duplicates” needs a boundary.

If the proposed design records progress first, ask how it prevents a crash from causing unsaved records to be skipped.

There may be a transaction boundary that solves part of the problem. There may be a design based on safe reprocessing and reconciliation. The right choice depends on the systems involved.

We do not need to resolve every distributed-systems question before making progress. We need to resolve the question that determines what “resume” means here.

Then exercise a narrow case: interrupt the import at the relevant boundary, restart it, and inspect the resulting records and effects.

The sequence becomes:

**Request → expose the recovery assumption → decide the guarantee → demonstrate one interrupted run → expand the implementation.**

That is a useful replacement for the conversation that might once have happened incidentally during several days of coding.

## A Checkpoint Needs to Change Something

There is a danger in turning this advice into another checklist that everyone completes without thinking.

“Agent described the approach.” Check.

“Risks considered.” Check.

“Tests included.” Check.

An agent can produce plausible text for all three. The presence of those sections does not establish that a consequential question was answered.

A useful checkpoint has a question, an owner, and a consequence.

The **question** identifies the uncertainty. The **owner** is someone responsible for resolving it, with access to the relevant knowledge. The **consequence** explains how the answer changes the work.

For the importer, the question is whether repeated processing is safe. The answer may change the persistence strategy, the side-effect handling, and the acceptance test.

If the answer could never alter the implementation, ask whether the checkpoint is serving a purpose.

## Scale the Process to the Decision

Correcting a heading, adjusting spacing, and changing a checkpoint strategy should not require the same ceremony.

The amount of explicit coordination should follow the uncertainty and the consequences of being wrong.

Look especially closely when a change affects persisted data, shared interfaces, access boundaries, ownership, or behavior during failure. Those decisions tend to involve assumptions that extend beyond the immediate code.

A small, reversible presentation change may need a preview and a focused check. A change to how several systems identify the same entity deserves a conversation about the meaning of that identity.

This also applies to exploration. Sometimes the fastest way to understand an uncertain requirement is to build a disposable prototype. Make its assumptions and status clear, and evaluate what it taught you before adopting it into the system.

Fast experiments are useful. Treating their unresolved decisions as settled architecture is where the trouble starts.

## Run a Friction Audit

Take one recurring development activity that your team has shortened, removed, or largely delegated to AI.

Ask four questions:

1. **What useful information did this activity sometimes uncover?**
2. **Where does that information surface in our current process?**
3. **What is the smallest explicit action that would expose it earlier?**
4. **How will we tell whether that action helped?**

Keep the answer concrete.

“Improve communication” gives nobody a next step.

“Before changes to import recovery, identify the write/checkpoint boundary and agree on the result of a crash between them” does.

Try the replacement on a real change. Did it expose an assumption? Did the answer change the design? Did it prevent a disagreement from spreading into more code? Or did it add work without revealing anything useful?

Adjust accordingly. A process should be open to evidence about its own usefulness.

## Make the Useful Work Intentional

AI gives us an opportunity to change the economics of implementation. We can explore more options, create working examples sooner, and automate work that used to consume substantial effort.

The conversations about meaning and consequences still matter.

Some used to happen because the work took long enough for people to cross paths. Some happened because implementation forced someone to investigate. Some never happened at all.

We can improve on that arrangement.

Identify the information the team needs. Make the consequential assumptions visible. Resolve them with the people who understand their effects. Ask for evidence while the implementation is still small enough to change easily.

**Keep the speed. Give the important questions a reliable place to happen.**

In the next episode, we will make that practical at the point of assignment: what needs to be in a request before “implement this” becomes a useful instruction?
