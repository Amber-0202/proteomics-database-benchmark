# Initial data-loading materials still required

The migration reconstruction is supplied. The original initial loaders below were not found among the project files reviewed for this preparation step. Their absence from this repository does not mean they never existed.

## MongoDB Pattern 1 loader

Provide the actual `.py`, `.ipynb`, `.js` or other source used to:

- Read the selected TP1 abundance spreadsheet/matrix and parse the 48 sample names into model, stimulation state and replicate.
- Create the two dataset records and P1 sample documents, including embedded measurements and their source identifiers.
- Read the selected PS1 analysis sheet into `phosphopeptide_summaries`.
- Construct phosphopeptide identifiers, protein identifiers and `linkedProteinAnalyteId`, handle missing values, and map regulation flags/directions.

Include the input filenames, sheet names/header-row settings, any intermediate files and any manual edits required after the initial run. Do not substitute a newly guessed mapping for the historical one.

## PostgreSQL loader

Provide the actual Python, SQL/COPY scripts, notebooks, or saved import procedure used to populate the implemented schema, particularly:

- `Dataset`, `Analyte`, `Sample`, `Quantification`, sample groups and experimental conditions.
- UniProt/gene annotation relations used by the queries.
- `PhosphopeptideRegulation` and `PhosphopeptideModelRegulation`, including protein-analyte links.
- Identifier assignments, including TP1 dataset ID 1, and loading order for foreign keys.

A schema-only dump creates structure but does not replace these data-loading materials.

## If the original loaders were not retained

Record that explicitly. A database export plus documented restore instructions can provide the measured prototype data as an alternative reconstruction route. Any newly reconstructed loader must be labelled accordingly and checked against the exported measured database before being presented as reproducing it. Do not claim the original import code has been recovered.

Actual input datasets/exports and timing records will be organised in a subsequent step. Review local connection settings before sharing source files, and replace personal passwords with configurable settings.
