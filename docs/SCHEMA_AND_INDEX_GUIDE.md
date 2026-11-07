# Schema and index preparation

## What this step adds

This package adds PostgreSQL DDL and MongoDB collection/index setup for the recorded configuration. It uses the supplied schema dump and `final_indexes.md`; it does not propose new indexes or infer new schema validators.

| Implementation | Structures | Recorded indexes |
| --- | --- | --- |
| PostgreSQL | 45 tables | 20 explicit indexes plus 34 primary-key and three unique-constraint supporting indexes |
| MongoDB P1 | Three collections | 14 non-default indexes plus three default `_id_` indexes |
| MongoDB P2 | Four collections | Seven non-default indexes plus four default `_id_` indexes |

PostgreSQL setup is described in [the schema README](../postgresql/schema/README.md). The [original inventory](final_indexes.md) lists exact names, key order and evidence limitations.

## MongoDB collection and index setup

From the repository root, with a local MongoDB service and mongosh available:

```sh
mongosh "mongodb://localhost:27017" --file mongodb/pattern1/indexes.js
mongosh "mongodb://localhost:27017" --file mongodb/pattern2/indexes.js
```

Each script selects its recorded database (`proteomics_pattern1` or `proteomics_pattern2`), creates any missing named collections, then adds the recorded non-default indexes with their recorded names and key order. MongoDB supplies the default `_id_` indexes. No JSON-schema validators are added, because none were provided in this evidence. Document layout is established by the data loaders and migration. An equivalent P1-to-P2 reconstruction is now supplied; see [the migration guide](IMPORT_AND_MIGRATION_GUIDE.md). The initial P1/PostgreSQL loaders are supplied; see [initial data loading](INITIAL_DATA_LOADING.md).

The scripts do not load measurements or annotations and do not remove pre-existing indexes. Use a separate reconstruction instance to build the documented snapshot. For a populated instance, verify its inventory rather than assuming that an index setup script removes unrelated configuration.

Index command references:
- https://www.mongodb.com/docs/v7.0/core/indexes/create-index/
- https://www.mongodb.com/docs/v7.0/reference/command/createIndexes/

## Recorded snapshot and measured configurations

The supplied inventory records the collected configuration; it does not establish when each index was introduced or which historical baseline runs preceded it. The setup files recreate that recorded snapshot. They are not separate, verified historical baseline/optimised index profiles.

Keep the query variants from step 1 distinct, and use the thesis execution plans and method to interpret index use in the reported runs. Running every variant against the final index snapshot is a new experiment unless the corresponding measured configuration is known to match it. No original benchmark values are changed by this packaging.

## Provenance and checks

- PostgreSQL source: `protehome_schema_terminal(1).sql` (schema-only PostgreSQL/pg_dump 18.6 export).
- MongoDB source: the supplied final index inventory, which transcribes `getIndexes()` output.
- PostgreSQL table, constraint and explicit index expressions are retained unchanged.
- MongoDB names, key fields, directions and compound-key order are retained; the reported internal index version is not passed as a new create option.
- Source comparison and local syntax/mock checks do not constitute a live database restore or a new full workload execution.

The equivalent P1-to-P2 reconstruction is now supplied. Initial P1/PostgreSQL loaders are supplied. Data inputs, PostgreSQL metadata seed/export and original measurements remain to be added; see [initial data loading](INITIAL_DATA_LOADING.md).
