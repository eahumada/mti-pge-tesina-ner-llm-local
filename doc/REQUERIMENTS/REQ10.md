# Requirement Details: FR1.6

## Metadata
- **ID:** FR1.6
- **Category:** Functional
- **Title:** Resumability
- **Source File:** functional_requirements.md
- **Enriched:** No

## Description
The system must be capable of pausing and resuming execution. Using the Pub/Sub state, if the process crashes, it must resume from the last unacknowledged message without reprocessing previously completed batches.
