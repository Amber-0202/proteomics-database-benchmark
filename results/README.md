# Recorded benchmark results

`comparison_final_updated.pdf` is an unchanged copy of the author-supplied `comparison_final_updated(3).pdf`. It is the retained comparison report for Q1-Q8 across PostgreSQL, MongoDB P1 baseline, the separately reported P1 optimisations, and P2. It includes per-run timing values and summary statistics, as well as written interpretations of execution plans.

The PDF is the supplied measurement record. Per-query screenshots and raw Explain output files are not included. The written plan descriptions in the PDF are reported observations, not newly collected execution-plan artifacts. No screenshots, logs or timing observations were reconstructed or fabricated.

The report describes five warm-up executions, excluded from statistics, and ten measured values for each reported series. Q3 and Q7 use shared P1/P2 series; optimised Q8/P2 Q8 also share a series. Shared values must not be treated as independently measured duplicates. Missing configuration cells do not mean zero runtime. Displayed MongoDB 0 ms values reflect millisecond reporting resolution.

Some PDF query titles retain the term "phosphosite" from the supplied comparison report. For Q2/Q3, the implemented records are phosphopeptide summaries, as described in the thesis and query guide. The original PDF is preserved rather than edited to alter its historical wording.

See `docs/materials_manifest.json` for the source filename, size and SHA-256 checksum. This repository preparation did not rerun the benchmark or expand the thesis's original result-equivalence validation coverage.
