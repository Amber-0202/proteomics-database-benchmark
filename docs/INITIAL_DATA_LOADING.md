# Initial data loading

## Supplied scripts and preparation changes

These eight scripts were supplied by the project author as the MongoDB and PostgreSQL import materials. They are organised copies of those files, not newly inferred implementations. Download suffixes were removed, input paths and connection settings were made configurable, and default input paths were relocated to `data/raw/`. MongoDB dataset metadata retains workbook basenames. Data conversions, identifier assignments, missing-value handling, regulation parsing, SQL statements, assertions, and interactive write confirmations are retained. See [the manifest](initial_import_manifest.csv) for original names and SHA-256 checksums.

The P1-to-P2 migration remains a separately labelled equivalent reconstruction; supplying these initial loaders does not recover the missing historical migration script.

## Environment and inputs

From the repository root, install the import dependencies into your Python environment:

```sh
python -m pip install -r requirements-import.txt
```

The requirements file lists dependencies, not a frozen version record of the original experiment. PostgreSQL uses Psycopg 3 (`psycopg`), not `psycopg2`. MongoDB uses PyMongo. Excel input uses pandas/openpyxl. MongoDB migration and index setup additionally require mongosh.

Place `260316 Raw data - TP1.xlsx` and `260316 Raw data - PS1.xlsx` in `data/raw/`, or set `TP1_FILE` / `PS1_FILE`. Both `quantification` and `analysis` sheets are required. Use the exact project workbooks and preserve row order. Do not treat similarly named spreadsheet revisions as interchangeable.

Connection defaults are local MongoDB and PostgreSQL `localhost:5432`, database `protehome`, user `postgres`. Optional overrides are listed in [the environment example](import_environment.example). The example is not automatically loaded. PostgreSQL prompts for a password unless `PGPASSWORD` is set. MongoDB uses `MONGO_URI` and `MONGO_P1_DB`. Existing JavaScript migration/index scripts use the thesis database names; if overriding the P1 name, adapt those settings consistently.

## MongoDB P1, followed by P2

| Order | Script | Role | Existing confirmation |
| --- | --- | --- | --- |
| M1 | `scripts/mongodb/03_import_pattern1.py` | Reads TP1 measurements and PS1 analytical summaries; builds `datasets`, `samples` and `phosphopeptide_summaries` | `REBUILD` |
| M2 | `scripts/mongodb/04_fix_ptm_localisation.py` | Compares PS1 summary `ptmLocalisation` with source quantification values and repairs differences | `FIX` when changes are needed |

```sh
python scripts/mongodb/03_import_pattern1.py
python scripts/mongodb/04_fix_ptm_localisation.py
mongosh "mongodb://localhost:27017" --file mongodb/pattern1/indexes.js
mongosh "mongodb://localhost:27017" --file scripts/mongodb/reconstructed_p1_to_p2.js
mongosh "mongodb://localhost:27017" --file scripts/mongodb/check_migration_counts.js
mongosh "mongodb://localhost:27017" --file mongodb/pattern2/indexes.js
```

Use a reconstruction database. M1 replaces all documents in the three P1 collections after `REBUILD`; it is not an incremental import, and its multi-collection writes are not one atomic transaction. It creates some indexes, so run the separate P1 index setup to add the complete recorded index snapshot. That snapshot is not a complete record of historical baseline configurations.

The supplied M1 already reads PTM localisation from the PS1 quantification sheet. M2 is retained as the supplied verification/repair utility; a fresh import may need no changes. It writes only if differences are found and confirmed. Its optional repair is not a second data-modelling pattern. P2 is created by the separate migration reconstruction, which requires an empty target; see [the migration guide](IMPORT_AND_MIGRATION_GUIDE.md).

M1 retains expected values of 48 TP1 samples and 39,814 PS1 summary records. The existing migration checker additionally uses the historical 304,911 protein measurements and 6,376 measurements for `CTRL_BASAL_1`. These are retained checks, not newly observed results.

## PostgreSQL: prerequisites before the six scripts

Restore/create the schema using [the schema instructions](../postgresql/schema/README.md), then import the supplied [base metadata export](../postgresql/data/README.md):

```sh
psql -h localhost -p 5432 -U postgres -d protehome -v ON_ERROR_STOP=1 -f postgresql/data/00_base_metadata.sql
```

Use your own deployment connection settings if different. This export supplies the Project, Dataset, experimental-structure and Sample rows required by the six Python scripts. It is a one-time transactional insert, not an upsert. **The referenced Organism record (taxonomy ID 10090) is still required separately** before the entity loaders; it is not included in this export. A schema-only dump does not populate metadata.

The supplied base export retains the recorded values below, except for the separately required Organism record:

- `Dataset` IDs 1 (TP1) and 2 (PS1), plus any referenced project/structure records;
- `Organism` taxonomy ID 10090 and any referenced records;
- `Sample`: 48 TP1 and 52 PS1 records whose names match the workbook quantification columns;
- `SampleGroup`, including `CTRL_BASAL`, `CTRL_INS`, and basal/insulin groups for `CI`, `DEX`, `TNF`, `MPQ` and `AA`;
- `ExperimentalCondition`, `ExperimentalVariable` and `GroupCondition` mappings used by the benchmark, with their recorded IDs and relationships.

The SQL is the supplied metadata export, retained without modifying its records. Its 100 sample names match the source quantification-sheet headers (48 TP1, 52 PS1); PS1 uses `BAS` in sample names while sample groups use `BASAL`. The analysis loader resolves groups by name across `SampleGroup`; preserve the recorded group mapping and avoid ambiguous duplicate names. The scripts do not invent sample assignments or group/condition metadata.

## PostgreSQL execution order

After schema and metadata prerequisites are satisfied, run from the repository root:

| Order | Script | Main imported records | Dependency |
| --- | --- | --- | --- |
| P1 | `scripts/postgresql/import_tp1_entities.py` | TP1 `Analyte`, UniProt descriptor and identifier/gene records | TP1 dataset, organism and empty TP1 entity tables |
| P2 | `scripts/postgresql/import_ps1_entities.py` | PS1 analytes, phosphosites and phosphosite descriptors | P1; current maximum analyte ID must be 7170 |
| P3 | `scripts/postgresql/import_quantification.py` | TP1 and PS1 `Quantification` | P1/P2 plus all recorded samples |
| P4 | `scripts/postgresql/import_analysis.py` | `DETest`, `ContrastGroup`, `DEResult`, `PValue` | P1/P2 plus recorded sample groups |
| P5 | `scripts/postgresql/import_ps1_regulation.py` | `PhosphopeptideRegulation` and TP1 protein links | P1/P2; empty regulation relation |
| P6 | `scripts/postgresql/extend_ps1_regulation.py` | Multiplicity/PTM metadata and `PhosphopeptideModelRegulation` | P5; empty model-regulation relation |

```sh
python scripts/postgresql/import_tp1_entities.py
python scripts/postgresql/import_ps1_entities.py
python scripts/postgresql/import_quantification.py
python scripts/postgresql/import_analysis.py
python scripts/postgresql/import_ps1_regulation.py
python scripts/postgresql/extend_ps1_regulation.py
```

Run each command separately and inspect its checks before confirming. P1-P5 retain `IMPORT`; P6 retains `EXTEND`. Existing duplicate-import checks and transaction handling remain in place. These scripts are intended for the recorded prototype, not arbitrary repeated imports into a populated database. P5/P6 retain conditional auxiliary-table/column DDL; this is redundant where the supplied final schema already contains those structures.

The scripts retain row-based analyte IDs: TP1 1-7170, PS1 starting at 7171. P3 retains expected quantification counts of 304,911 (TP1) and 1,136,286 (PS1), total 1,441,197. P4 retains checks for 19 tests, 34 contrast-group rows, 160,973 differential results and 282,452 p-values. P6 prepares five model rows per PS1 phosphopeptide (199,070 rows). These expected counts describe the supplied scripts; they have not been remeasured during repository preparation.

Source emergent-summary/model-flag discrepancies are reported and preserved by the existing loaders. Do not replace summary counts with newly recomputed counts to force agreement. Cross-omics links also retain the supplied mapping rules: MongoDB constructs protein identifiers from gene/UniProt fields, while PostgreSQL resolves linked TP1 analytes through UniProt. This packaging does not establish all-query semantic equivalence.

## Validation during repository preparation

See [the preparation check record](IMPORT_VERIFICATION.md). No database imports, repairs, migrations or benchmark experiments were executed while organising these files. The base metadata export is now included. Actual workbooks, the referenced Organism row and original measurement records must still accompany the repository before it can be described as a complete reproduction package.
