# Import and migration materials

## Migration provenance

The supplied migration record explicitly states that the exact historical P1-to-P2 script was not preserved. `scripts/mongodb/reconstructed_p1_to_p2.js` is an equivalent reconstruction of the four transformations in that record and Appendix D.3. It must not be described as a recovered original script.

The pipeline expressions were compared with both the record and the appendix, including stage and object-key order. The wrapper replaces interactive `use(...)` commands with explicit database handles, consumes aggregation cursors, and adds checks for populated source collections, sample measurement arrays, different source/target names, and an empty target. The four projections/merges retain the documented expressions. The wrapper is a preparation-time addition.

No historical experiment was rerun while preparing this package. Syntax and mock-interface checks do not establish successful execution against the real dataset.

## Required starting point

P1 must already be populated from the actual TP1/PS1 inputs. Creating empty collections and indexes in step 2 does not satisfy that requirement. The supplied P1 and PostgreSQL initial loaders are now organised in the repository; see [initial data loading](INITIAL_DATA_LOADING.md). The P1 loader must run before this reconstruction.

For reconstruction, use a separate local MongoDB instance with populated P1 and empty or absent P2. This script refuses a populated target, because `$merge` alone would not remove stale records absent from the current source. It does not delete or clear any database. If interrupted after partial writes, it will refuse to run again against that now-populated target; investigate the partial reconstruction rather than treating the script as a resume procedure.

## Transformation

1. Copy `datasets` with `_id` retained.
2. Copy `phosphopeptide_summaries` with `_id` and annotation structure retained.
3. Copy samples with `totalProteomeMeasurements` excluded.
4. Unwind source measurements and project each into `protein_measurements` with its parent reference and context.

The measurement `_id` is the source sample ObjectId string, an underscore and the source array index. This identifies the array position at migration time; it is not a biological identifier or a guarantee across source-array reordering. Protein identifiers, abundance, unit and missing flags are copied without deriving new abundance values.

## Execution order after P1 loading

From the repository root, using mongosh on the reconstruction instance:

```sh
mongosh "mongodb://localhost:27017" --file scripts/mongodb/reconstructed_p1_to_p2.js
mongosh "mongodb://localhost:27017" --file scripts/mongodb/check_migration_counts.js
mongosh "mongodb://localhost:27017" --file mongodb/pattern2/indexes.js
```

The migration uses the database names recorded in the thesis. If adapting names for another reconstruction, update both migration and count-check settings consistently. The index setup file also selects the recorded P2 database name.

## Count checks

`check_migration_counts.js` is read-only. It compares current source-array and target-document counts at two scopes: all measurements and `CTRL_BASAL_1`. The historical references are 304,911 and 6,376. Its observed values and pass/fail status are computed at execution time, not filled in as experimental results in advance.

These checks mirror the recorded count-level validation. Equal counts do not establish equality of all values, completeness of cross-omics identifiers, or agreement of every Q1-Q8 result. The thesis's original validation scope remains unchanged.

## Documentation references

- `P1_to_P2_Migration_Procedure(1).docx`, Sections 6-8.
- Thesis Appendix D.3-D.4.
- MongoDB 7.0 `$merge`: https://www.mongodb.com/docs/v7.0/reference/operator/aggregation/merge/
- mongosh script execution: https://www.mongodb.com/docs/mongodb-shell/write-scripts/
