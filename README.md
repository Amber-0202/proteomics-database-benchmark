# Proteomics Database Benchmark

Code and experimental materials supporting the thesis *Understanding the Impact of MongoDB Data Modelling Patterns on Query Performance for Proteomics Data*, by Jinqiu Pan, University of Sydney.

## Current contents

The repository currently contains the final benchmark queries, the PostgreSQL schema, and the recorded PostgreSQL and MongoDB index definitions. Data import and migration scripts, datasets, and measurement records will be added separately. This snapshot creates database structures and provides queries, but does not yet populate the prototype data.

| Path | Contents |
| --- | --- |
| `postgresql/queries/` | Eight PostgreSQL query bodies, Q1-Q8 |
| `postgresql/schema/` | Complete schema-only export, portable table/constraint setup, and explicit indexes |
| `mongodb/pattern1/indexes.js`, `mongodb/pattern2/indexes.js` | Collection and index setup for the recorded snapshot |
| `docs/SCHEMA_AND_INDEX_GUIDE.md` | Setup order, provenance and recorded-configuration scope |
| `docs/final_indexes.md` | Supplied index inventory |
| `mongodb/pattern1/baseline/` | Eight P1 baseline pipelines, Q1-Q8 |
| `mongodb/pattern1/optimised/` | Five separately evaluated P1 optimisations: Q2, Q4, Q5, Q6 and Q8 |
| `mongodb/pattern2/` | Eight P2 pipelines, Q1-Q8 |
| `docs/QUERY_GUIDE.md` | Query roles, starting collections and execution instructions |
| `docs/query_manifest.csv` | Original file/pipeline names and checksums for the organised query files |

There are 29 query files representing the 26 distinct code listings in the thesis appendix. Q3 and Q7 share their implementation between P1 and P2; optimised P1 Q8 shares its implementation with P2 Q8. Those three pipelines are copied into the applicable folders for convenience. Their copies do not denote additional independent timing series.

## Source and consistency checks

The SQL expressions were compared with the supplied `query1.sql`, `query2.sql`, `query3.sql` and `Q4.sql` through `Q8.sql`. Their query bodies match the final Appendix A listings after removing timing prefixes, comments and presentation whitespace.

The MongoDB expressions were compared with the original Compass export `SavedPipelines(1).zip` and the final Appendix A listings. Every selected pipeline matches, including stage order and object-key order. The organised files use strict JSON formatting; comments and Compass editor metadata are omitted. Predicates, values, projections, grouping expressions, sort keys and limits are retained.

Duplicate saved items and the alternative `opimized_Q8 (copy)` entry are excluded. The selected optimised Q8 is the export named `opimized_Q8`, matching `P2_Q8(same as opimized Q8)` and the final appendix.

These are file consistency checks, not a new execution of the database experiments or a new all-query result-equivalence test. The thesis describes the original validation coverage and measurement procedure.

## Running the queries

These queries require the populated prototype and the index configuration described in the thesis. Start with [schema and index preparation](docs/SCHEMA_AND_INDEX_GUIDE.md); data population instructions will follow. See [the query guide](docs/QUERY_GUIDE.md) for the correct database and starting collection. The supplied index snapshot does not document all historical baseline index states.

- PostgreSQL: run one `.sql` file in the prototype database. The files return query results. To inspect the timing and plan used by the benchmark, prepend `EXPLAIN (ANALYZE, BUFFERS)` to the statement.
- MongoDB Compass: select the documented database and collection, open the Aggregations text editor, and paste the complete array from the corresponding `.json` file. The JSON files are pipeline arrays, not Compass saved-pipeline metadata files.
- For timing, follow the thesis protocol: five warm-up executions and ten recorded executions using the stated PostgreSQL and Compass Explain instrumentation. Do not compare an ordinary result-retrieval wall-clock time with the thesis timings.

## Prototype identifiers and scope

P1 uses `proteomics_pattern1`; P2 uses `proteomics_pattern2`. In the recorded PostgreSQL deployment, numeric dataset ID `1` denotes TP1. The database's PostgreSQL name is deployment-specific.

The queries retain their recorded identifiers and output limits: the selected protein label is `Akt1`, Q7 selects `Pcm1`, and Q8 selects `DEX`. They are prototype operations, not a complete multi-study exploration application. Q3 counts phosphopeptide-summary records, not deduplicated biological phosphorylation sites.

Data source and reconstruction instructions will accompany the data and import scripts when those materials are added.
