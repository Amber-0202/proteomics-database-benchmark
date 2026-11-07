# PostgreSQL schema and indexes

## Files

- `01_schema.sql`: all 45 table definitions and 105 separately declared constraints from the supplied schema-only dump. These comprise 34 primary keys, three unique constraints and 68 foreign keys; inline CHECK constraints remain in their table definitions.
- `02_indexes.sql`: the 20 explicit B-tree index statements from that same dump. Do not add duplicate indexes for primary-key or unique constraints.
- `original_schema_dump.sql`: an unchanged archival copy of `protehome_schema_terminal(1).sql`, exported from PostgreSQL 18.6 on 27 October 2026. It includes the original ownership commands, psql restriction wrappers and indexes.

The first two files provide one reconstruction route. The original dump is an alternative archival route; do not apply both routes to the same database. Splitting the supplied dump changes its packaging, not table, constraint or index definitions. The portable files omit `OWNER TO postgres` and the dump's psql wrappers so that the database owner running the scripts owns the new objects.

## Creating an empty schema

Use PostgreSQL 18 and a new empty database. From the repository root, with the local PostgreSQL service running and your normal connection settings:

```sh
createdb protehome_benchmark
psql -X -v ON_ERROR_STOP=1 -d protehome_benchmark -f postgresql/schema/01_schema.sql
psql -X -v ON_ERROR_STOP=1 -d protehome_benchmark -f postgresql/schema/02_indexes.sql
```

These commands create structure and indexes only. They do not load TP1 or PS1 records or assign the dataset identifiers expected by the queries. Data and import instructions are a later preparation step. When preparing a full bulk-data reconstruction, the explicit index file can be applied after the data load, before benchmarking.

The generated files were checked against the original structural statements and index inventory. A live PostgreSQL restoration and data reconstruction have not been run as part of this packaging step.

Command reference: https://www.postgresql.org/docs/18/app-psql.html
