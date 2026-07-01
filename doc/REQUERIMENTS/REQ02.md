# Requirement Details: NFR1.1

## Metadata
- **ID:** NFR1.1
- **Category:** Functional
- **Title:** Zero Data Leakage
- **Source File:** non_functional_requirements_enriched.md
- **Enriched:** Yes

## Description
Due to the extreme sensitivity of financial compliance data (KYC, PEP), the architecture must strictly enforce local execution of the LLMs. No article text or entity data can be transmitted to external proprietary APIs (like OpenAI GPT, Google Cloud NLP, or AWS).
