# Building a World Around a Terrible API

The assignment sounds simple: call an API, ingest the data, and make it useful in a new application.

Then you meet the API.

It is inconsistent enough that writing the integration also means figuring out which behavior you can depend on. You need somewhere to test your assumptions, reproduce failures, and measure whether your ingestion strategy is making progress.

Eventually, you find yourself building an emulator, a benchmarking harness, and a simulation environment.

You started out trying to import some records. Now you’re discussing how to create a world.

That is a reasonable engineering response to a difficult dependency. But it introduces a vocabulary that deserves more care than we usually give it.

Dataset. Seed. Fixture. Scenario. Catalog. World. Snapshot. Operator.

These words describe different responsibilities. Understanding them makes the architecture easier to reason about—and gives an AI agent a much better chance of building what you intended.

## Start with the job

Imagine an ingestion test with these requirements: begin with known inventory records, retrieve them through the API, make an update visible during the import, fail a request, and verify that recovery finishes without losing records or creating duplicates.

Then run the same exercise again.

A file full of sample JSON supplies part of the setup. We also need behavior, state, timing, controls, and a way to judge the result.

Each additional term gives a name to one of those responsibilities.

## The data and the setup

A **dataset** is a collection of data. It might contain inventory records, locations, products, or captured API responses. It can be raw, cleaned, curated, or generated. The word does not tell us how a running system will behave.

**Seed data** establishes an initial population. It might be three records or a substantial starting database.

A **random seed** initializes a pseudorandom generator. Under the same generator and conditions, it can help reproduce generated values. It does not, by itself, make an entire test deterministic.

That distinction matters when someone says, “Use the same seed.”

A **fixture** establishes known conditions for a test. It can include data, configuration, an initialized service, and cleanup afterward.

A **scenario** describes the situation being exercised: the starting conditions, actions, environmental changes, and expected outcomes.

For our example, the dataset contains the records. The fixture prepares the environment. The scenario describes the update and failure during the run.

These concepts can overlap in a framework’s implementation. Keeping their responsibilities distinct still helps us describe what we need.

## The catalog defines the starting environment

In our repository, a **catalog** is a curated definition used to create a runtime environment.

It contains authored business data and the starting model for what we call a world. “Load the showcase catalog” means selecting source material from which the environment can be initialized.

Think of it as an exercise blueprint. It might define facilities, inventory records, and relationships that make a particular integration case meaningful. The definition can be reused to create separate runtime instances.

**The catalog is the definition layer; the world is the instantiated state.**

The name is local to this project. Elsewhere, a catalog might describe products, services, database metadata, or datasets. Calling something a catalog does not universally mean “simulation blueprint.”

A starting-state definition also does not necessarily describe everything that happens during a scenario. A scenario can reference a catalog and separately specify actions, timing, and injected failures.

## The world is the running state

A **world**, in our repository, is the instantiated runtime environment. It contains the state against which requests operate, and that state may change as the exercise proceeds.

If the model includes delayed updates, queued work, or a controllable clock, those are relevant parts of the world too. They influence what a client observes, even when they are not visible in a response body.

“World” is useful because the environment is richer than a bag of records. But the name does not automatically establish isolation, determinism, or completeness. Those capabilities need specification and verification.

Two worlds created from the same catalog might start with equivalent business data. Whether they also receive identical identifiers, clock values, and schedules depends on initialization.

That detail becomes important the moment a test depends on it.

![A catalog initializes a world; snapshots capture and restore state; the operator manages the running environment.](assets/world.svg)

## The snapshot captures a position

A **snapshot** is a captured representation of state at a particular point. In our repository, that means a serialized representation of a world.

We might capture it immediately after initialization or halfway through an exercise. An initial state is still a state; a snapshot need not wait until a world has evolved.

The useful questions concern scope: what did we save, what can we restore, and what remains outside the snapshot?

Saving inventory records while omitting pending updates can restore the visible data without restoring the conditions that caused the next failure. Saving a clock value while restarting background work differently can change what happens next.

A snapshot supports restoration within its defined boundary. **Exact replay is a stronger requirement.**

Replay may also require inputs, timing, random choices, a fault schedule, and compatible implementation versions. Recorded HTTP exchanges provide useful examples, but they do not automatically model every new sequence a client might attempt. [WireMock: Record and Playback](https://wiremock.org/docs/record-playback/).

Think of a flight simulator: a saved position tells us where the aircraft was. Reproducing the remainder of the exercise also requires the conditions and events that affected the flight.

A **virtual clock** lets a test advance modeled time explicitly. Components must use that clock for their time-dependent behavior to be controlled. .NET’s `FakeTimeProvider` supports this approach. [Microsoft: Testing with FakeTimeProvider](https://learn.microsoft.com/en-us/dotnet/core/extensions/timeprovider-testing?tabs=dotnet-cli).

## The operator provides the controls

Our repository calls its management interface the **operator**. It supports loading and unloading worlds, advancing the clock, exporting documents, and inspecting state.

This is the environment’s control surface.

The importer uses the API it is integrating against. The test harness uses the management interface to arrange the surrounding conditions. Those are different responsibilities and access boundaries.

The broader architectural term is **control plane**: the mechanisms used to configure and manage the environment.

“Operator” remains our chosen name. It should not imply that we implement the Kubernetes Operator pattern, which has a specific meaning involving custom resources and a control loop. [Kubernetes: Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## How the pieces fit together

| Concept | Responsibility |
|---|---|
| Dataset | Supplies a collection of data |
| Seed data | Initializes a population |
| Fixture | Establishes known test conditions |
| Scenario | Describes the exercise |
| Catalog | Defines reusable starting material for a world |
| World | Holds the instantiated runtime state |
| Snapshot | Captures state within a defined scope |
| Operator | Manages and inspects the runtime environment |

A fixture can create a world from a catalog. A scenario can drive requests and introduce failures. The operator can advance time or capture a snapshot. A later test can restore that snapshot, provided it understands what restoration guarantees.

These are different parts of how the environment is assembled and operated.

## The emulator still needs evidence

An **emulator** aims to reproduce relevant externally observable behavior so the integration can use it as a substitute. A **simulator** models behavior under specified conditions. The same environment can serve both purposes, and terminology varies among tools.

Giving the environment a rich model does not establish that it behaves like the provider.

For each important behavior, distinguish:

- **Documented:** The provider says this is how it works.
- **Observed:** We captured evidence that it behaved this way.
- **Assumed:** We modeled it without sufficient confirmation.

An assumption can be useful for testing. It should remain visible as an assumption.

**Characterization tests** capture existing behavior. **Differential tests** compare systems under equivalent inputs and relevant conditions. A **test oracle** determines whether an outcome is acceptable. A captured response, specification, or invariant can contribute to that judgment.

A **corpus** collects test material; **provenance** records where it came from and how it was transformed.

Matching a captured response establishes something narrower than supporting an entire workflow. “Parity achieved” should identify what was compared and what remains unsupported.

A beautiful model can be consistently wrong. Evidence connects it to the difficult dependency we started with.

## The benchmark measures a particular experiment

A **harness** prepares and runs the experiment. A **workload** describes the work presented to the system. A **benchmark** measures performance under stated conditions.

For ingestion, useful measurements include successfully committed records per second, duplicate counts, completeness, retry volume, and memory use.

**Latency** measures elapsed time for a defined operation; **throughput** measures completed work per unit time. A p95 or p99 describes a percentile of the measured latency distribution, so the population and measurement boundary matter.

The environment makes measurements repeatable and defines their limits. An emulator that responds immediately does not tell us how an importer will perform against a slow provider. Advancing a virtual clock by an hour does not measure an hour of production throughput.

Workload generation matters as well. An open model schedules arrivals independently of completion; a closed model waits for existing work to finish. Choosing the wrong model can hide the effects of a slowdown. [Grafana k6: Open and closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).

Name both what you controlled and what you measured.

## Give the agent the architecture

“Generate some test data and mock the API” leaves most of this design implicit.

A more useful assignment is:

> Use the inventory catalog to create an isolated world. Run the importer through the emulated API. During the scenario, make an update visible between page requests and inject one recoverable failure. Verify completeness and absence of duplicate destination entities. Capture the starting state and execution details needed to reproduce the result.

That makes responsibilities visible. It also exposes unresolved questions: what counts as a duplicate, what makes a failure recoverable, and which execution details must be captured?

Answering those questions before generation is usually cheaper than discovering incompatible answers in the resulting code.

The catalog defines the starting material. The world holds the running state. The snapshot captures a position. The operator provides the controls.

Once those responsibilities are clear, we can ask better questions about the system—and get more useful code back.
