# NER Benchmark Project Directives
## RAG Integration Policy
- **Strict Additive Documentation**: Never overwrite or delete existing documentation when adding new session findings. All documents (`BENCHMARKS.md`, `TODO.md`, `ROADMAP.md`, etc.) must be strictly additive. Verify via git history that no previous content is lost.
- **Comparative Study Value**: A difference of up to 0.02 in F1 Score when comparing Baseline vs RAG is tolerable and considered highly relevant information. Always preserve the RAG infrastructure and indexing work to allow alternate runs (with and without RAG) side-by-side.
- **Metric Degradation Rule**: A drop of up to 0.02 in F1 score is acceptable for the sake of comparison. However, continue evaluating whether further lists degrade precision. The goal is to accurately present the results of the study with and without RAG.
- **Optimal Analysis**: Always analyze the optimal configuration carefully before rolling out to the full 16-model benchmark sweep.
