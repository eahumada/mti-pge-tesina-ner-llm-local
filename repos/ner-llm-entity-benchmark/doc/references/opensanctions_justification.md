# Academic Justification for the Use of OpenSanctions Datasets in NER for Financial Compliance and AML

## Executive Summary
This document provides a technical and academic justification for the selection of **OpenSanctions.org** as the primary data source for developing and evaluating Named Entity Recognition (NER) and Entity Resolution (ER) benchmarks within the context of Financial Compliance and Anti-Money Laundering (AML). OpenSanctions is selected over proprietary alternatives due to its **full provenance traceability**, **open-source pipeline**, **standardized graph schema (FollowTheMoney)**, and **alignment with academic reproducibility standards**.

---

## 1. Data Provenance and Technical Pipeline
The validity of any AML dataset depends on the integrity of its pipeline. OpenSanctions employs a rigorous, multi-stage transformation process that ensures high data fidelity:

### 1.1 The Ingestion Layer (Zavod)
Raw data is ingested from official government and intergovernmental sources via specialized crawlers. This "Zavod" layer focuses on parsing and cleaning fragmented data into a structured format, assigning stable source-scoped identifiers (e.g., `ofac-81717`) to ensure the original record remains accessible.

### 1.2 The Statement-Based Provenance Model
Unlike many datasets that store only the "final" version of an entity, OpenSanctions utilizes a **statement-based data model**. Every property (name, date of birth, address) is stored as an individual statement containing:
- The original value before cleaning.
- The specific dataset source.
- Temporal metadata (`first_seen`, `last_seen`).
- The canonical ID of the merged entity.

This architecture allows researchers to audit any specific data point and trace it back to its original official source, a critical requirement for academic rigor and regulatory compliance.

### 1.3 Deduplication and Resolution (Nomenklatura)
To handle the "entity alias" problem common in AML, the `nomenklatura` framework implements a sophisticated entity resolution pipeline:
- **Blocking**: Using inverted indices to identify potential candidates.
- **Comparison**: Applying matching algorithms to generate merge candidates.
- **Resolution**: Utilizing a resolver graph to determine canonical IDs (NK-IDs or Wikidata Q-IDs).

---

## 2. Transparency and Reproducibility
In academic research, a "black-box" dataset is a liability. OpenSanctions mitigates this through extreme transparency:

### 2.1 Open-Source Infrastructure
The entire data processing stack is published on GitHub under the **MIT License**. This allows a thesis committee or peer reviewers to inspect the exact logic used to transform raw government PDFs/CSV files into the structured database, ensuring that the results are not artifacts of an opaque proprietary algorithm.

### 2.2 Non-Commercial Accessibility
By providing the dataset for free to non-commercial users, OpenSanctions removes the financial and legal barriers (such as restrictive NDAs) associated with proprietary compliance sets, ensuring that the research is accessible and the benchmarks are reproducible by other scholars.

---

## 3. Global Coverage and Representativeness
For an NER model to be robust, it must be trained on a representative global distribution of entities. OpenSanctions aggregates 88+ sanctions sources from over 211 countries, including the primary "Gold Standard" lists:

| Jurisdiction | Key Datasets Aggregated | Scope |
| :--- | :--- | :--- |
| **United Nations** | UN SC Consolidated Sanctions | 15+ programs (Iraq, North Korea, Iran, etc.) |
| **European Union** | EU Financial Sanctions Files (FSF) | 41+ programs, including human rights and Russia |
| **United States** | OFAC SDN and Consolidated Lists | Specially Designated Nationals and non-SDN lists |
| **United Kingdom** | UK FCDO and HMT/OFSI Lists | Global Anti-Corruption and regional programs |

This breadth ensures that the resulting NER benchmarks cover a diverse array of naming conventions, scripts (transliteration), and entity types (individuals, vessels, crypto-wallets).

---

## 4. Standardization via the FollowTheMoney (FtM) Schema
The use of the **FollowTheMoney (FtM)** schema provides a critical advantage for the evaluation of structured NER:

### 4.1 Graph-Based Ontology
FtM moves beyond simple "flat" NER (Labeling `PER`, `ORG`, `LOC`) by defining a rich ontology of **Matchable Schemata** (e.g., `Person`, `Company`, `CryptoWallet`) and **Contextual Schemata** (e.g., `Ownership`, `Sanction`, `Family`).

### 4.2 Support for Structured Evaluation
For a thesis in Financial Compliance, the goal is often not just to *find* a name, but to *link* it to a risk profile. The FtM schema allows the NER task to be evaluated as a mapping problem:
$$\text{Unstructured Text} \xrightarrow{NER} \text{FtM Property} \xrightarrow{ER} \text{Canonical Entity}$$
This enables the measurement of **Entity Resolution accuracy**, not just token-level F1 scores.

---

## 5. Academic Validity vs. Proprietary Datasets
When compared to proprietary tools (e.g., LSEG World-Check), OpenSanctions is the superior choice for a scholarly thesis for the following reasons:

### 5.1 Verifiability vs. Authority
Proprietary datasets rely on "authority"—the user trusts the result because of the vendor's brand. OpenSanctions relies on "verifiability"—the user trusts the result because the evidence is provided. In an academic context, verifiability is the only valid metric.

### 5.2 Auditability in Regulatory Compliance
Regulatory bodies (e.g., FINMA, FCA) increasingly demand that screening decisions be **reconstructible**. By using an open dataset, this thesis aligns with the industry shift toward "Explainable AI" (XAI) in compliance, where every match must be justified by a traceable source.

### 5.3 Structural Validity for LLMs
Recent research (e.g., *OpenSanctions Pairs*, 2026) demonstrates that high-fidelity, structured open data allows LLMs to achieve near-perfect F1 scores (up to 98.95%) in entity matching. This proves that the structural quality of the open dataset is sufficient for state-of-the-art AI benchmarking.

---

## Conclusion
The combination of **complete provenance**, **open-source auditing**, **global coverage**, and the **FtM standardized schema** makes OpenSanctions the most rigorous choice for a thesis on NER for Financial Compliance. It transforms the dataset from a simple "list of names" into a verifiable, structured knowledge graph suitable for high-stakes academic evaluation.

## References
- [Data Enrichment - OpenSanctions](https://www.opensanctions.org/docs/enrichment/)
- [Identifiers and Deduplication - OpenSanctions](https://www.opensanctions.org/docs/identifiers/)
- [Statement Data Model - OpenSanctions](https://www.opensanctions.org/docs/statements/)
- [Replication FAQ - OpenSanctions](https://www.opensanctions.org/faq/6/replication/)
- [About OpenSanctions](https://www.opensanctions.org/docs/about/)
- [Consolidated Sanctions - OpenSanctions](https://www.opensanctions.org/datasets/sanctions/)
- [FollowTheMoney GitHub](https://github.com/opensanctions/followthemoney)
- [Nomenklatura GitHub](https://github.com/opensanctions/nomenklatura/)
- [OpenSanctions Pairs: Large-Scale Entity Matching with LLMs (arXiv 2026)](https://doi.org/10.48550/arxiv.2603.11051)
- [OpenSanctions vs LSEG World-Check Analysis](https://nnsflow.com/blog/opensanctions-vs-worldcheck)
