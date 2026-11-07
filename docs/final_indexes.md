# Final Index Inventory

## Scope and evidence

This inventory records the supplied configuration; it does not propose new indexes. PostgreSQL definitions are taken from `protehome_schema_terminal.sql`, exported from PostgreSQL 18.6 on 27 October 2026. MongoDB definitions are transcribed from the supplied `getIndexes()` output for `proteomics_pattern1` and `proteomics_pattern2`. The index names and compound-key order are retained.

The MongoDB output describes the configuration at the time of collection. It does not establish when an index was created or whether a particular measured query used it. Use the corresponding execution plans to report index use, and identify any measured configuration that differed from this inventory.

## Inventory totals

| Implementation | Tables / collections | Explicit / non-default indexes | Constraint / default indexes | Total represented indexes |
|---|---:|---:|---:|---:|
| PostgreSQL | 45 tables | 20 explicit indexes | 34 primary-key + 3 unique-constraint indexes | 57 |
| MongoDB P1 | 3 collections | 14 non-default indexes | 3 default `_id_` indexes | 17 |
| MongoDB P2 | 4 collections | 7 non-default indexes | 4 default `_id_` indexes | 11 |

The PostgreSQL total is derived from the supplied schema dump, rather than a new live-catalog query. Primary-key and unique constraints create supporting unique B-tree indexes; they are therefore listed separately from the 20 explicit `CREATE INDEX` statements. The 68 foreign-key constraints are not counted as 68 additional indexes.

## PostgreSQL: explicitly created indexes

All 20 statements specify `USING btree`. None specifies `UNIQUE`, a partial-index predicate, `INCLUDE`, an expression key, an explicit collation, descending order, or non-default null ordering. Key columns are shown in their declared order.

| Table (public schema) | Index name | Ordered key columns |
|---|---|---|
| `ContrastGroup` | `idx_contrastgroup_detest` | `de_test` |
| `ContrastGroup` | `idx_contrastgroup_samplegroup` | `sample_group` |
| `DEResult` | `idx_deresult_analyte` | `analyte` |
| `DescriptorEntryPhosphosite` | `idx_descriptorentryphosphosite_accession_residue` | `accession_id, residue` |
| `DescriptorEntryPhosphosite` | `idx_descriptorentryphosphosite_analyte` | `analyte` |
| `DescriptorEntryUniProt` | `idx_descriptorentryuniprot_accession` | `accession_id` |
| `DescriptorEntryUniProt` | `idx_descriptorentryuniprot_analyte` | `analyte` |
| `ExperimentalCondition` | `idx_experimentalcondition_variable` | `variable` |
| `GroupCondition` | `idx_groupcondition_condition` | `condition` |
| `GroupCondition` | `idx_groupcondition_group` | `"group"` |
| `PhosphopeptideRegulation` | `idx_ppreg_gene_symbol` | `gene_symbol` |
| `PValue` | `idx_pvalue_deresult` | `de_result` |
| `PValue` | `idx_pvalue_method` | `adjustment_method` |
| `Quantification` | `idx_quantification_analyte` | `analyte` |
| `Quantification` | `idx_quantification_dataset_analyte` | `dataset, analyte` |
| `Quantification` | `idx_quantification_dataset_sample` | `dataset, sample` |
| `Quantification` | `idx_quantification_sample` | `sample` |
| `Sample` | `idx_sample_dataset_group` | `dataset, "group"` |
| `UniProtGene` | `idx_uniprotgene_entry` | `uniprot_entry` |
| `UniProtGene` | `idx_uniprotgene_gene` | `gene_name` |

### Exact CREATE INDEX statements

```sql
CREATE INDEX idx_contrastgroup_detest ON public."ContrastGroup" USING btree (de_test);
CREATE INDEX idx_contrastgroup_samplegroup ON public."ContrastGroup" USING btree (sample_group);
CREATE INDEX idx_deresult_analyte ON public."DEResult" USING btree (analyte);
CREATE INDEX idx_descriptorentryphosphosite_accession_residue ON public."DescriptorEntryPhosphosite" USING btree (accession_id, residue);
CREATE INDEX idx_descriptorentryphosphosite_analyte ON public."DescriptorEntryPhosphosite" USING btree (analyte);
CREATE INDEX idx_descriptorentryuniprot_accession ON public."DescriptorEntryUniProt" USING btree (accession_id);
CREATE INDEX idx_descriptorentryuniprot_analyte ON public."DescriptorEntryUniProt" USING btree (analyte);
CREATE INDEX idx_experimentalcondition_variable ON public."ExperimentalCondition" USING btree (variable);
CREATE INDEX idx_groupcondition_condition ON public."GroupCondition" USING btree (condition);
CREATE INDEX idx_groupcondition_group ON public."GroupCondition" USING btree ("group");
CREATE INDEX idx_ppreg_gene_symbol ON public."PhosphopeptideRegulation" USING btree (gene_symbol);
CREATE INDEX idx_pvalue_deresult ON public."PValue" USING btree (de_result);
CREATE INDEX idx_pvalue_method ON public."PValue" USING btree (adjustment_method);
CREATE INDEX idx_quantification_analyte ON public."Quantification" USING btree (analyte);
CREATE INDEX idx_quantification_dataset_analyte ON public."Quantification" USING btree (dataset, analyte);
CREATE INDEX idx_quantification_dataset_sample ON public."Quantification" USING btree (dataset, sample);
CREATE INDEX idx_quantification_sample ON public."Quantification" USING btree (sample);
CREATE INDEX idx_sample_dataset_group ON public."Sample" USING btree (dataset, "group");
CREATE INDEX idx_uniprotgene_entry ON public."UniProtGene" USING btree (uniprot_entry);
CREATE INDEX idx_uniprotgene_gene ON public."UniProtGene" USING btree (gene_name);
```

## PostgreSQL: constraint-backed indexes

These entries preserve the constraint names and key order from the dump. Their supporting indexes are unique B-tree indexes. Do not create separate duplicate indexes for these constraints.

| Table (public schema) | Constraint / supporting index name | Constraint type | Ordered key columns |
|---|---|---|---|
| `AnalyteDescriptor` | `AnalyteDescriptor_pkey` | PRIMARY KEY | `id` |
| `Analyte` | `Analyte_pkey` | PRIMARY KEY | `id` |
| `CellLine` | `CellLine_pkey` | PRIMARY KEY | `id` |
| `ContrastGroup` | `ContrastGroup_pkey` | PRIMARY KEY | `id` |
| `DEResult` | `DEResult_pkey` | PRIMARY KEY | `id` |
| `DETest` | `DETest_pkey` | PRIMARY KEY | `id` |
| `DataSource` | `DataSource_pkey` | PRIMARY KEY | `id` |
| `Dataset` | `Dataset_pkey` | PRIMARY KEY | `id` |
| `DescriptorEntryPhosphosite` | `DescriptorEntryPhosphosite_pkey` | PRIMARY KEY | `id` |
| `DescriptorEntryUniProt` | `DescriptorEntryUniProt_pkey` | PRIMARY KEY | `id` |
| `ExperimentalCondition` | `ExperimentalCondition_pkey` | PRIMARY KEY | `id` |
| `ExperimentalVariable` | `ExperimentalVariable_pkey` | PRIMARY KEY | `id` |
| `File` | `File_pkey` | PRIMARY KEY | `id` |
| `InvitationCode` | `InvitationCode_pkey` | PRIMARY KEY | `id` |
| `Molecule` | `Molecule_pkey` | PRIMARY KEY | `chembl_id` |
| `Organism` | `Organism_pkey` | PRIMARY KEY | `taxonomy_id` |
| `PermissionNode` | `PermissionNode_pkey` | PRIMARY KEY | `id` |
| `PhosphopeptideModelRegulation` | `PhosphopeptideModelRegulation_pkey` | PRIMARY KEY | `analyte, model` |
| `PhosphopeptideRegulation` | `PhosphopeptideRegulation_phosphopeptide_id_key` | UNIQUE | `phosphopeptide_id` |
| `PhosphopeptideRegulation` | `PhosphopeptideRegulation_pkey` | PRIMARY KEY | `analyte` |
| `PhosphositeGroup` | `PhosphositeGroup_pkey` | PRIMARY KEY | `group_id` |
| `Phosphosite` | `Phosphosite_pkey` | PRIMARY KEY | `id` |
| `Project` | `Project_pkey` | PRIMARY KEY | `id` |
| `Quantification` | `Quantification_pkey` | PRIMARY KEY | `id` |
| `SampleGroup` | `SampleGroup_pkey` | PRIMARY KEY | `id` |
| `Sample` | `Sample_pkey` | PRIMARY KEY | `id` |
| `UniProtAccession` | `UniProtAccession_pkey` | PRIMARY KEY | `id` |
| `UniProtEntry` | `UniProtEntry_pkey` | PRIMARY KEY | `accession_id` |
| `UploadRecord` | `UploadRecord_pkey` | PRIMARY KEY | `id` |
| `UserGroup` | `UserGroup_pkey` | PRIMARY KEY | `id` |
| `User` | `User_pkey` | PRIMARY KEY | `id` |
| `WorkflowNode` | `WorkflowNode_pkey` | PRIMARY KEY | `id` |
| `GroupMembership` | `pk_groupmembership` | PRIMARY KEY | `"user", "group"` |
| `MoleculeName` | `pk_moleculename` | PRIMARY KEY | `name, chembl_id` |
| `Permission` | `pk_permission` | PRIMARY KEY | `"group", node` |
| `DEResult` | `uq_deresult_test_analyte` | UNIQUE | `contrast, analyte` |
| `Phosphosite` | `uq_phosphosite_accession_residue` | UNIQUE | `accession_id, residue` |

## MongoDB: index definitions

All reported indexes have index format version `v: 2`. Every key direction is `1` (ascending). All non-default entries except the six-field P2 index are single-field indexes. No additional `unique`, `sparse`, `partialFilterExpression`, `expireAfterSeconds`, `hidden`, or `collation` options appear in the supplied output. Default `_id_` indexes enforce `_id` uniqueness even though the output does not include an explicit `unique` property.

### proteomics_pattern1

#### datasets

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |

#### phosphopeptide_summaries

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |
| `geneSymbol_1` | `{"geneSymbol": 1}` | Non-default |
| `uniprotId_1` | `{"uniprotId": 1}` | Non-default |
| `insulinRegulationStatus_1` | `{"insulinRegulationStatus": 1}` | Non-default |
| `defectiveModelCount_1` | `{"defectiveModelCount": 1}` | Non-default |
| `emergentModelCount_1` | `{"emergentModelCount": 1}` | Non-default |
| `defects.DEX_1` | `{"defects.DEX": 1}` | Non-default |
| `emergent.DEX_1` | `{"emergent.DEX": 1}` | Non-default |

#### samples

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |
| `sampleId_1` | `{"sampleId": 1}` | Non-default |
| `datasetId_1` | `{"datasetId": 1}` | Non-default |
| `condition.conditionId_1` | `{"condition.conditionId": 1}` | Non-default |
| `condition.model_1` | `{"condition.model": 1}` | Non-default |
| `totalProteomeMeasurements.geneSymbol_1` | `{"totalProteomeMeasurements.geneSymbol": 1}` | Non-default |
| `totalProteomeMeasurements.uniprotId_1` | `{"totalProteomeMeasurements.uniprotId": 1}` | Non-default |
| `totalProteomeMeasurements.proteinAnalyteId_1` | `{"totalProteomeMeasurements.proteinAnalyteId": 1}` | Non-default |

### proteomics_pattern2

#### datasets

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |

#### phosphopeptide_summaries

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |
| `insulinRegulationStatus_1` | `{"insulinRegulationStatus": 1}` | Non-default |
| `geneSymbol_1` | `{"geneSymbol": 1}` | Non-default |
| `defects.DEX_1` | `{"defects.DEX": 1}` | Non-default |
| `emergent.DEX_1` | `{"emergent.DEX": 1}` | Non-default |

#### protein_measurements

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |
| `geneSymbol_1` | `{"geneSymbol": 1}` | Non-default |
| `proteinAnalyteId_1` | `{"proteinAnalyteId": 1}` | Non-default |
| `condition.conditionId_1_condition.model_1_condition.insulinState_1_geneSymbol_1_uniprotId_1_abundance_1` | `{"condition.conditionId": 1, "condition.model": 1, "condition.insulinState": 1, "geneSymbol": 1, "uniprotId": 1, "abundance": 1}` | Non-default |

#### samples

| Index name | Ordered key specification | Classification |
|---|---|---|
| `_id_` | `{"_id": 1}` | Default `_id_` |

## Differences relevant to interpretation

- The P1 and P2 index sets are not identical. On `phosphopeptide_summaries`, both have non-default indexes on `geneSymbol`, `insulinRegulationStatus`, `defects.DEX`, and `emergent.DEX`. P1 additionally has `uniprotId`, `defectiveModelCount`, and `emergentModelCount` indexes.
- P1 `samples` has four non-default indexes on sample metadata and three on fields inside `totalProteomeMeasurements`. P2 `samples` has only the default `_id_` index.
- P2 `protein_measurements` has single-field indexes on `geneSymbol` and `proteinAnalyteId`, together with the six-field compound index shown above. Its compound-key order is part of the recorded configuration.
- The document examples show measurement arrays in P1 and scalar measurement fields in P2. Multikey status and actual query use should be verified from the corresponding execution plans; these properties are not supplied by this `getIndexes()` listing.

## Thesis-ready configuration description

The PostgreSQL schema included 20 explicitly created B-tree indexes, in addition to indexes supporting 34 primary-key constraints and three unique constraints. MongoDB Pattern 1 contained 17 indexes across three collections, including three default `_id_` indexes; Pattern 2 contained 11 indexes across four collections, including four default `_id_` indexes. Pattern 1 indexed selected sample metadata and protein identifiers within the embedded measurement array. Pattern 2 indexed `geneSymbol` and `proteinAnalyteId` in the separate measurement collection and also included a compound index on `condition.conditionId`, `condition.model`, `condition.insulinState`, `geneSymbol`, `uniprotId`, and `abundance`, in that order. Both patterns indexed `geneSymbol`, `insulinRegulationStatus`, `defects.DEX`, and `emergent.DEX` in the phosphopeptide summary collection, while Pattern 1 additionally indexed `uniprotId`, `defectiveModelCount`, and `emergentModelCount`.

## Sources

1. User-supplied PostgreSQL schema export: `protehome_schema_terminal.sql` (database and pg_dump version 18.6; export completed 27 October 2026).
2. User-supplied MongoDB `getIndexes()` output for the seven collections listed above (28 October 2026).
3. PostgreSQL 18 documentation, Constraints: https://www.postgresql.org/docs/18/ddl-constraints.html (primary-key and unique-constraint supporting indexes; foreign-key indexing behavior).
4. MongoDB documentation, Default _id Index: https://www.mongodb.com/docs/manual/core/index-unique/#unique-index-on-a-single-field
