# Base metadata

`00_base_metadata.sql` is the author-supplied export of the benchmark's Project, Dataset, experimental-structure and Sample records. The supplied SQL is retained byte-for-byte. It contains one transaction, seven INSERT statements, and no schema changes or data-clearing commands.

| Table | Rows |
| --- | --- |
| Project | 1 |
| Dataset | 2 |
| ExperimentalVariable | 2 |
| ExperimentalCondition | 8 |
| SampleGroup | 12 |
| GroupCondition | 24 |
| Sample | 100 (48 TP1, 52 PS1) |

Run once after `postgresql/schema/01_schema.sql`, before the six Python loaders:

```sh
psql -h localhost -p 5432 -U postgres -d protehome -v ON_ERROR_STOP=1 -f postgresql/data/00_base_metadata.sql
```

Use your deployment's connection settings if different. This is not an upsert: re-running it against existing rows raises key conflicts. Its BEGIN/COMMIT transaction keeps a failing run from committing partial inserts.

The PS1 sample names use `BAS` while the shared basal sample-group names use `BASAL`; these are retained source names. Sample names were checked against the original quantification-sheet column headers in the supplied TP1 and PS1 workbooks. Internal references, row counts and inserted columns were checked against the schema. No live PostgreSQL import was executed during preparation.

The export does **not** include `Organism`. The supplied Python loaders reference taxonomy ID 10090 through `UniProtEntry.organism`; import or verify the original Organism row before running those loaders. No organism metadata has been fabricated in this SQL. The raw workbooks and recorded benchmark measurements are separate repository materials.
