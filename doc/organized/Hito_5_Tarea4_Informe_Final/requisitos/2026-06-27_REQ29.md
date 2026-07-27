# Requirement Details: NFR4.2

## Metadata
- **ID:** NFR4.2
- **Category:** Functional
- **Title:** Horizontal Scalability via Pub/Sub
- **Source File:** non_functional_requirements_enriched.md
- **Enriched:** Yes

## Description
The system's processing capacity must be horizontally scalable. By using a local Pub/Sub queue, additional worker processes can be spun up on the same machine (or network) to consume pending articles concurrently, strictly limited by available hardware (GPU/CPU).
