# Import-material status

The original P1 and PostgreSQL initial-loading files requested in the previous preparation step have now been supplied. The eight organised scripts and their order are described in [Initial data loading](INITIAL_DATA_LOADING.md). They are no longer missing.

Materials still required:

1. The actual TP1 and PS1 Excel inputs, or a documented alternative restore route.
2. The original PostgreSQL metadata seed/import SQL or data export for datasets, samples, sample groups, conditions and other referenced metadata. The six Python loaders assume those records already exist. Do not infer new IDs or group assignments and describe them as the measured configuration.
3. Original benchmark measurement records and their execution/plan context.

The exact historical P1-to-P2 migration script remains unavailable; its supplied equivalent reconstruction is explicitly labelled. New initial loaders do not change that provenance. See [the migration guide](IMPORT_AND_MIGRATION_GUIDE.md).
