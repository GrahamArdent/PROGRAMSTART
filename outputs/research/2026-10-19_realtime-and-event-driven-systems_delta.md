# Research Delta - Realtime and event-driven systems

Review date: 2026-10-19
Owner: platform-architecture
Outcome: recommendation unchanged
Confidence: high

## Source changes

- Reviewed Apache Kafka's 2026 release announcements: <https://kafka.apache.org/blog/>.
- Kafka 4.2/4.3 patch lines include critical fixes, including a Kafka Streams RocksDB native-memory correction.

## Decision

Keep broker selection driven by ordering, durability, throughput, operational ownership, and schema governance. Patch-level currency is mandatory for Kafka deployments, but the release evidence does not justify replacing lighter managed pub/sub or queue options for simpler workloads.

## Follow-up

- Require upgrade-note review and workload replay before moving Kafka minor lines.
