# Original workbook inputs

Download the project-supplied Excel workbooks from the [benchmark input release](https://github.com/Amber-0202/proteomics-database-benchmark/releases/tag/benchmark-data-v1). They are release assets of this same repository; they are not included in GitHub's automatically generated source-code ZIP.

| Release asset | Filename required in this directory | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `TP1.xlsx` | `260316 Raw data - TP1.xlsx` | 7383597 | `a759522cdcc85b253e259031ee54d4f8aa1818bf8b6e8bcc235b0cc71b0cfd6c` |
| `PS1.xlsx` | `260316 Raw data - PS1.xlsx` | 29481373 | `2656ed282077391e7c0c5929d6fbfb04865932850a7fa72d940916e286e94d5a` |

Download the two assets, rename them as shown, and place them beside this README before running the loaders. Alternatively, set `TP1_FILE` and `PS1_FILE` to their local paths. The release filenames are shortened for downloading; workbook contents are unchanged. The larger PS1 workbook is distributed as a release asset rather than through the browser's repository-file uploader.

Both `quantification` and `analysis` sheets are used. Preserve source identifiers, column names and row order: PostgreSQL analyte IDs depend on source row positions. Checksums identify the exact supplied workbook versions.

## Biological source

The TP1 and PS1 study descriptions supplied to the project identify the source as Fazakerley, D.J., van Gerwen, J., Cooke, K.C. et al. *Phosphoproteomics reveals rewiring of the insulin signaling network and multi-nodal defects in insulin resistance*. Nature Communications 14, 923 (2023), https://doi.org/10.1038/s41467-023-36549-2. TP1 is described as originating from Supplementary Data 1 and PS1 from Supplementary Data 3.

These assets are the project-supplied workbook versions consumed by the loaders. Their published-study origin does not imply byte identity with the publisher's original supplementary files. No workbook values, ordering or sheets were changed for repository preparation.

See [initial data loading](../../docs/INITIAL_DATA_LOADING.md) for metadata setup and execution order.
