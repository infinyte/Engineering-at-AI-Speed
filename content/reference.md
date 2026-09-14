# The integration field guide

Names are useful when their boundaries are clear. This reference separates established terminology from project-local meanings. Some industry terms vary across tools; describe the required behavior as well as naming it.

## Data, setup, and runtime

| Term | Working definition |
|---|---|
| Dataset | A collection of data, whether raw, curated, captured, or generated. |
| Seed data | Data used to initialize a system; it need not be small. |
| Random seed | Input that initializes a pseudorandom generator. It does not control all sources of nondeterminism. |
| Fixture | Known conditions for a test, potentially including data, configuration, dependencies, and cleanup. |
| Scenario | Starting conditions, actions, and environmental events used to exercise a situation. |
| Snapshot | Captured state at a point in time, within an explicit scope. Restoration and replay guarantees must be defined. |

## Vocabulary local to the API project

| Term | Meaning here | Boundary |
|---|---|---|
| Catalog | Curated starting definition used to initialize a world. | Not a universal meaning of catalog, and not necessarily a complete scenario. |
| World | Instantiated runtime environment and its state. | The name alone does not guarantee isolation, determinism, or completeness. |
| Operator | Management interface for world lifecycle, inspection, export, and clock control. | Does not imply the Kubernetes Operator pattern. |

![The catalog, world, snapshot, and operator describe separate responsibilities.](assets/world.svg)

Kubernetes uses Operator for software extensions built around custom resources and control loops. [Kubernetes Operator documentation](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## Dependency replacements

| Term | Working definition |
|---|---|
| Test double | Replacement for a production dependency used in testing. |
| Stub | Supplies configured responses. |
| Mock | Verifies expected interactions. |
| Spy | Records interactions for inspection. |
| Fake | Working implementation with simplifying shortcuts. |
| Emulator | Emphasizes compatible externally observable behavior within a stated scope. |
| Simulator | Models behavior under specified conditions; can also provide an emulated interface. |

The test-double distinctions follow the Meszaros/Fowler taxonomy. Product names may use “mock” more broadly. [Martin Fowler: Test Double](https://martinfowler.com/bliki/TestDouble.html).

## Contracts and evidence

| Term | Working definition |
|---|---|
| Schema | Structural rules and constraints for data or messages. |
| API contract | Stated interface expectations, potentially including operations, errors, and behavior. |
| Contract test | Executable checks of specified expectations at an integration boundary. |
| Conformance testing | Checks an implementation against a stated specification or standard. |
| Characterization testing | Captures the behavior of an existing system, including quirks. |
| Differential testing | Compares systems under equivalent inputs and relevant conditions. |
| Test oracle | Mechanism used to judge whether an outcome is acceptable. |
| Invariant | Property that must remain true within the defined model. |
| Corpus | Collection of test material such as captured exchanges and boundary cases. |
| Provenance | Origin and transformation history of evidence or data. |
| Golden master | Approved comparison baseline; approval does not prove correctness. |
| Fidelity | Closeness to a target along specified dimensions. |
| Parity | Agreement within an explicitly stated comparison scope. |

Contract-testing approaches differ. Consumer-driven testing requires provider verification to establish support for the consumer’s interactions. [Pact documentation](https://docs.pact.io/).

## Reproduction and failure

| Term | Working definition |
|---|---|
| Record and replay | Capture interactions and reproduce them later, subject to matching and scope rules. |
| Determinism | Same relevant initial conditions and inputs produce the same observable result within the execution model. |
| Virtual clock | Controlled time source for modeled or tested behavior. |
| Partial failure | Some parts of an operation succeed while others fail or become unreachable. |
| Idempotency | Repeating an operation has the same intended effect as performing it once. |
| Deduplication | Detecting repeated inputs or work to prevent unwanted duplicate effects. |
| Checkpoint | Persisted progress used to resume work. |
| Reconciliation | Comparing states and correcting missing or divergent data. |
| Fault injection | Deliberately introducing faults to test behavior under those conditions. |

Recorded responses do not automatically cover arbitrary request histories. [WireMock record and playback](https://wiremock.org/docs/record-playback/). Time control requires components to use the controlled abstraction. [Microsoft FakeTimeProvider guidance](https://learn.microsoft.com/en-us/dotnet/core/extensions/timeprovider-testing?tabs=dotnet-cli).

## Recovery and consistency

| Term | Working definition |
|---|---|
| Retry | Attempting an operation again under a defined policy. |
| Backoff | Increasing the interval between attempts. |
| Jitter | Varying intervals to reduce synchronized retries. |
| Circuit breaker | Temporarily restricting calls to a persistently failing dependency. |
| Backpressure | Slowing incoming work to match downstream capacity. |
| Eventual consistency | Replicas converge under the model’s assumptions when updates cease; reads can temporarily be stale. |

A timeout does not establish that the remote operation had no effect. [Microsoft Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry). Recovery mechanisms have different purposes. [Microsoft transient fault guidance](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults). Eventual consistency is a consistency model, not a label for arbitrary API inconsistencies. [Microsoft consistency levels](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels).

## Measurements

| Term | Working definition |
|---|---|
| Harness | Prepares, drives, and observes an experiment. |
| Workload | Operation mix, size, arrival pattern, concurrency, duration, and other conditions of demand. |
| Benchmark | Performance measurement under a defined workload and environment. |
| Load test | Examination under specified or expected demand. |
| Stress test | Examination beyond intended capacity. |
| Soak test | Sustained examination to expose accumulated problems. |
| Latency | Elapsed time for a defined operation. |
| Throughput | Completed work per unit time. |
| p95 / p99 | Percentiles of an observed latency distribution; define the measurement population. |
| Open workload | Arrivals scheduled independently of completion. |
| Closed workload | New work depends on completion of existing work. |
| AI eval | Evaluation of an AI system’s performance on defined tasks and criteria; distinct from API conformance or throughput. |

Choose a workload model that reflects the question being measured. [Grafana k6 workload models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).
