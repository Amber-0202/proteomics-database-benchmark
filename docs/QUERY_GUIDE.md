# Query guide

## Biological role and starting collection

| Query | Information returned | P1 starting collection | P2 starting collection |
| --- | --- | --- | --- |
| Q1 | Mean protein abundance and observation count by protein and condition | `samples` | `protein_measurements` |
| Q2 | Selected defective phosphopeptide summaries and corresponding protein observations | `phosphopeptide_summaries` | `phosphopeptide_summaries` |
| Q3 | Counts of defective and emergent phosphopeptide-summary records per gene | `phosphopeptide_summaries` | `phosphopeptide_summaries` |
| Q4 | Dataset-level Akt1 identifiers, conditions and distinct sample count | `samples` | `protein_measurements` |
| Q5 | Akt1 measurements from insulin-stimulated samples in the five resistance models | `samples` | `protein_measurements` |
| Q6 | Basal and insulin Akt1 means, observation counts and difference by model | `samples` | `protein_measurements` |
| Q7 | All Pcm1 summary records with site and per-model regulation annotations | `phosphopeptide_summaries` | `phosphopeptide_summaries` |
| Q8 | DEX-specific defective/emergent summaries, ranked primarily by annotated dysregulated-model count | `phosphopeptide_summaries` | `phosphopeptide_summaries` |

P1 database: `proteomics_pattern1`. P2 database: `proteomics_pattern2`. A foreign collection used by `$lookup` is specified in the pipeline and must exist in the selected database.

## Configurations

For Q1, run the P1 baseline and P2 pipelines. No separate optimised P1 Q1 was reported.

For Q2 and Q4-Q6, the folders contain baseline P1, optimised P1 and P2 versions.

For Q3 and Q7, the P1 and P2 JSON files are identical and represent the shared summary operation. They do not access the redesigned protein-measurement collection.

For Q8, baseline P1 is different from optimised P1. Optimised P1 and P2 use identical pipelines and share the measurement series reported in the thesis.

## PostgreSQL result inspection and timing

Each SQL file contains a complete statement without an active Explain prefix. To inspect returned data, run the file unchanged. To obtain the Explain plan and its Execution Time, add this prefix immediately before the initial `WITH` or `SELECT`:

```sql
EXPLAIN (ANALYZE, BUFFERS)
```

For example, place the prefix before the query body in `postgresql/queries/Q2.sql`. Do not place it after `WITH`, and do not insert a semicolon between the prefix and the query.

## MongoDB Compass result inspection and timing

1. Select the database and starting collection from the table above.
2. Open the Aggregations text editor.
3. Paste the entire JSON array from the desired file, including its opening and closing brackets.
4. Run the aggregation to inspect data, or use Explain and the execution-time measure specified in the thesis for timing.

The files use the deployed field names and value domains. Fields named `defectiveSites`, `emergentSites` and `totalDysregulatedSites` in Q3 are retained output names; they count summary records. The recorded handling of nulls, string markers, set-valued arrays, ordering and limits is preserved. The appendix and methodology discuss the result-validation scope; this packaging does not expand that scope.

## Preparation still required

The recorded schema and index snapshot are now supplied; see [schema and index preparation](SCHEMA_AND_INDEX_GUIDE.md). Populated datasets, import/migration scripts and measurement records remain to be added. The recorded index snapshot does not document every historical baseline/optimised index state. Keep the source configuration and actual plan evidence associated with each measured series when reconstructing experiments.
