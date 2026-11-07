# Import-material status

The requested materials are now supplied:

| Material | Location |
| --- | --- |
| Two MongoDB P1 import/repair scripts | `scripts/mongodb/` |
| Six PostgreSQL loaders | `scripts/postgresql/` |
| Base project, dataset, condition, group and sample metadata | `postgresql/data/00_base_metadata.sql` |
| Original exported Organism record and generated import SQL | `postgresql/data/organism.csv`, `postgresql/data/01_organism.sql` |
| Actual TP1/PS1 workbooks | Same-repository release assets, linked from [data/raw](../data/raw/README.md) |
| Supplied per-run timings and comparison summary | [results/comparison_final_updated.pdf](../results/comparison_final_updated.pdf) |

See [initial loading](INITIAL_DATA_LOADING.md) for the execution order. The workbook assets must be downloaded separately from the release and renamed as documented before using the Python loaders.

## Evidence boundaries

Per-query screenshots and raw Explain output files were not retained in this package. The supplied comparison PDF serves as the recorded timing report; its written execution-plan descriptions are reported observations. No missing screenshots or logs were fabricated.

The exact historical P1-to-P2 migration script remains unavailable. The separately supplied equivalent reconstruction remains labelled accordingly; adding data files and initial loaders does not change its provenance.

Repository preparation did not execute a fresh end-to-end reconstruction, rerun historical timing experiments, verify every historical baseline index state, or establish new all-query semantic equivalence.
