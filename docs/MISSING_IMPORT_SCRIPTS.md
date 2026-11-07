# Import-material status

The original P1 and PostgreSQL initial-loading files requested in the previous preparation step have now been supplied. The eight organised scripts and their order are described in [Initial data loading](INITIAL_DATA_LOADING.md). They are no longer missing.

Materials still required:

1. The actual TP1 and PS1 Excel inputs, or a documented alternative restore route.
2. The original `Organism` record for taxonomy ID 10090, referenced by the entity loaders. Project, datasets, sample groups, conditions and all 100 samples are now supplied in [`postgresql/data/00_base_metadata.sql`](../postgresql/data/README.md). No new IDs or group assignments were inferred.
3. Original benchmark measurement records and their execution/plan context.

The exact historical P1-to-P2 migration script remains unavailable; its supplied equivalent reconstruction is explicitly labelled. New initial loaders do not change that provenance. See [the migration guide](IMPORT_AND_MIGRATION_GUIDE.md).
