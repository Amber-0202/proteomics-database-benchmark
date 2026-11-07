# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

import re
import math
import pandas as pd
from pymongo import MongoClient


# =========================================================
# 1. Configuration
# =========================================================

TP1_FILE = str(Path(os.environ.get("TP1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - TP1.xlsx")).expanduser())
PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("MONGO_P1_DB", "proteomics_pattern1")

EXPECTED_TP1_SAMPLES = 48
EXPECTED_PS1_ROWS = 39814


# =========================================================
# 2. Helper functions
# =========================================================

def clean_value(value):
    """
    Convert pandas/numpy missing values to Python None,
    and convert numpy scalar values to native Python values
    where possible.
    """

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    # Convert numpy scalar -> normal Python scalar
    try:
        if hasattr(value, "item") and not isinstance(
            value,
            (str, bytes)
        ):
            value = value.item()
    except Exception:
        pass

    return value


def safe_float(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        number = float(value)

        if math.isnan(number):
            return None

        return number

    except Exception:
        return None


def safe_int(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        return int(value)

    except Exception:
        return None


def parse_sample_column(column_name):
    """
    Examples:

    CTRL_BASAL_1
        -> model=CTRL
        -> insulinState=BASAL
        -> replicate=1

    CI_INS_2
        -> model=CI
        -> insulinState=INS
        -> replicate=2
    """

    parts = str(column_name).split("_")

    if len(parts) >= 3:

        model = parts[0]
        insulin_state = parts[1]
        replicate = parts[2]

    else:

        model = None
        insulin_state = None
        replicate = None

    return {
        "conditionId":
            f"{model}_{insulin_state}"
            if model and insulin_state
            else str(column_name),

        "model": model,

        "insulinState": insulin_state,

        "replicate": safe_int(replicate)
    }


def make_protein_analyte_id(gene, uniprot):

    gene = (
        str(gene)
        if clean_value(gene) is not None
        else "UNKNOWN_GENE"
    )

    uniprot = (
        str(uniprot)
        if clean_value(uniprot) is not None
        else "UNKNOWN_UNIPROT"
    )

    return f"{gene}_{uniprot}"


def make_phosphopeptide_id(
    gene,
    uniprot,
    site,
    multiplicity
):

    gene = (
        str(gene)
        if clean_value(gene) is not None
        else "UNKNOWN_GENE"
    )

    uniprot = (
        str(uniprot)
        if clean_value(uniprot) is not None
        else "UNKNOWN_UNIPROT"
    )

    site = (
        str(site)
        if clean_value(site) is not None
        else "UNKNOWN_SITE"
    )

    multiplicity = (
        str(multiplicity)
        if clean_value(multiplicity) is not None
        else "UNKNOWN_MULT"
    )

    return (
        f"{gene}_{uniprot}_"
        f"{site}_{multiplicity}"
    )


def emergent_value_present(value):
    """
    Used ONLY for source-data diagnostics.

    Does not change any source values.
    """

    value = clean_value(value)

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    text = str(value).strip().upper()

    return text not in {
        "",
        "FALSE",
        "0",
        "NO",
        "NONE",
        "NAN"
    }


# =========================================================
# 3. Read and validate TP1 BEFORE touching MongoDB
# =========================================================

print()
print("=" * 72)
print("READING TP1")
print("=" * 72)


tp1_excel = pd.ExcelFile(TP1_FILE)

print(
    "TP1 sheets:",
    tp1_excel.sheet_names
)


tp1_df = pd.read_excel(
    TP1_FILE,
    sheet_name="quantification"
)


print(
    "TP1 shape:",
    tp1_df.shape
)


print(
    "TP1 columns:"
)

print(
    tp1_df.columns.tolist()
)


possible_identity_cols = [
    "Gene_Uniprot",
    "Gene",
    "Uniprot",
    "UniProt",
    "Protein",
    "Protein IDs",
    "Protein names"
]


identity_cols = [
    col
    for col in tp1_df.columns
    if col in possible_identity_cols
]


sample_cols = []


for col in tp1_df.columns:

    col_str = str(col)

    if re.match(
        r"^(CTRL|CI|DEX|TNF|MPQ|AA)_"
        r"(BASAL|INS)_\d+$",
        col_str
    ):
        sample_cols.append(col)


print(
    "Detected identity columns:",
    identity_cols
)

print(
    "Detected sample columns:",
    sample_cols
)

print(
    "Detected sample count:",
    len(sample_cols)
)


if len(sample_cols) != EXPECTED_TP1_SAMPLES:

    raise RuntimeError(
        f"Expected {EXPECTED_TP1_SAMPLES} "
        f"TP1 samples, found {len(sample_cols)}."
    )


# =========================================================
# 4. Build TP1 sample-centred documents
# =========================================================

print()
print("=" * 72)
print("PREPARING TP1 SAMPLE DOCUMENTS")
print("=" * 72)


sample_documents = []


for sample_col in sample_cols:

    sample_id = str(sample_col)

    condition = parse_sample_column(
        sample_id
    )

    measurements = []


    for _, row in tp1_df.iterrows():

        gene = clean_value(
            row.get("Gene")
        )

        uniprot = clean_value(
            row.get("Uniprot")
        )


        if uniprot is None:

            uniprot = clean_value(
                row.get("UniProt")
            )


        abundance = safe_float(
            row.get(sample_col)
        )


        if abundance is None:
            continue


        measurement = {

            "proteinAnalyteId":
                make_protein_analyte_id(
                    gene,
                    uniprot
                ),

            "geneSymbol":
                gene,

            "uniprotId":
                uniprot,

            "abundance":
                abundance,

            "unit":
                "normalised_intensity",

            "missing":
                False
        }


        measurements.append(
            measurement
        )


    sample_doc = {

        "sampleId":
            sample_id,

        "datasetId":
            "TP1",

        "condition":
            condition,

        "sampleMetadata": {

            "assayType":
                "mass_spectrometry",

            "omicsLayer":
                "total_proteome"
        },

        "totalProteomeMeasurements":
            measurements
    }


    sample_documents.append(
        sample_doc
    )


print(
    "Prepared TP1 sample documents:",
    len(sample_documents)
)


total_measurements = sum(
    len(
        doc[
            "totalProteomeMeasurements"
        ]
    )
    for doc in sample_documents
)


print(
    "Prepared TP1 measurements:",
    total_measurements
)


# =========================================================
# 5. Read PS1 analysis sheet
# =========================================================

print()
print("=" * 72)
print("READING PS1 ANALYSIS DATA")
print("=" * 72)


ps1_excel = pd.ExcelFile(
    PS1_FILE
)


print(
    "PS1 sheets:",
    ps1_excel.sheet_names
)


ps1_analysis_df = pd.read_excel(
    PS1_FILE,
    sheet_name="analysis"
)


print(
    "PS1 analysis shape:",
    ps1_analysis_df.shape
)


if len(
    ps1_analysis_df
) != EXPECTED_PS1_ROWS:

    raise RuntimeError(
        f"Expected {EXPECTED_PS1_ROWS} "
        "PS1 analysis rows, found "
        f"{len(ps1_analysis_df)}."
    )


if "Phosphopeptide" not in (
    ps1_analysis_df.columns
):

    raise RuntimeError(
        "PS1 analysis sheet has no "
        "'Phosphopeptide' column."
    )


ps1_analysis_df[
    "Phosphopeptide"
] = (
    ps1_analysis_df[
        "Phosphopeptide"
    ]
    .astype(str)
    .str.strip()
)


if ps1_analysis_df[
    "Phosphopeptide"
].duplicated().any():

    duplicates = (
        ps1_analysis_df[
            ps1_analysis_df[
                "Phosphopeptide"
            ].duplicated(
                keep=False
            )
        ][
            "Phosphopeptide"
        ]
        .head(20)
        .tolist()
    )

    raise RuntimeError(
        "Duplicate phosphopeptide IDs "
        "in analysis sheet: "
        f"{duplicates}"
    )


# =========================================================
# 6. Read PTM Localization from quantification sheet
#
# THIS IS THE IMPORTANT FIX.
# =========================================================

print()
print("=" * 72)
print("READING PS1 PTM LOCALIZATION")
print("=" * 72)


ps1_quant_meta_df = pd.read_excel(
    PS1_FILE,
    sheet_name="quantification",
    usecols=[
        "Phosphopeptide",
        "PTM Localization"
    ]
)


print(
    "PS1 quantification metadata shape:",
    ps1_quant_meta_df.shape
)


if len(
    ps1_quant_meta_df
) != EXPECTED_PS1_ROWS:

    raise RuntimeError(
        f"Expected {EXPECTED_PS1_ROWS} "
        "PS1 quantification rows, found "
        f"{len(ps1_quant_meta_df)}."
    )


ps1_quant_meta_df[
    "Phosphopeptide"
] = (
    ps1_quant_meta_df[
        "Phosphopeptide"
    ]
    .astype(str)
    .str.strip()
)


if ps1_quant_meta_df[
    "Phosphopeptide"
].duplicated().any():

    duplicates = (
        ps1_quant_meta_df[
            ps1_quant_meta_df[
                "Phosphopeptide"
            ].duplicated(
                keep=False
            )
        ][
            "Phosphopeptide"
        ]
        .head(20)
        .tolist()
    )

    raise RuntimeError(
        "Duplicate phosphopeptide IDs "
        "in quantification sheet: "
        f"{duplicates}"
    )


# Convert localisation explicitly to numeric
ps1_quant_meta_df[
    "PTM Localization"
] = pd.to_numeric(
    ps1_quant_meta_df[
        "PTM Localization"
    ],
    errors="coerce"
)


# =========================================================
# 7. Validate PS1 IDs across both sheets
# =========================================================

analysis_ids = set(
    ps1_analysis_df[
        "Phosphopeptide"
    ]
)

quant_ids = set(
    ps1_quant_meta_df[
        "Phosphopeptide"
    ]
)


missing_in_quant = (
    analysis_ids - quant_ids
)

extra_in_quant = (
    quant_ids - analysis_ids
)


print(
    "IDs missing from quantification:",
    len(missing_in_quant)
)

print(
    "Extra IDs in quantification:",
    len(extra_in_quant)
)


if missing_in_quant:

    print(
        "Examples missing from quantification:"
    )

    for value in list(
        missing_in_quant
    )[:10]:

        print(
            " ",
            value
        )


if extra_in_quant:

    print(
        "Examples only in quantification:"
    )

    for value in list(
        extra_in_quant
    )[:10]:

        print(
            " ",
            value
        )


if (
    missing_in_quant
    or extra_in_quant
):

    raise RuntimeError(
        "PS1 analysis and quantification "
        "phosphopeptide IDs do not match."
    )


print(
    "Analysis ↔ quantification IDs: OK"
)


# =========================================================
# 8. Merge PTM Localization onto analysis rows
# =========================================================

ps1_df = ps1_analysis_df.merge(

    ps1_quant_meta_df,

    on="Phosphopeptide",

    how="left",

    validate="one_to_one"
)


if len(ps1_df) != EXPECTED_PS1_ROWS:

    raise RuntimeError(
        "PS1 merge row count mismatch."
    )


missing_ptm_count = int(
    ps1_df[
        "PTM Localization"
    ]
    .isna()
    .sum()
)


print()
print(
    "Merged PS1 rows:",
    len(ps1_df)
)

print(
    "Missing PTM Localization "
    "after merge:",
    missing_ptm_count
)


if missing_ptm_count != 0:

    bad_examples = (
        ps1_df[
            ps1_df[
                "PTM Localization"
            ].isna()
        ][
            "Phosphopeptide"
        ]
        .head(20)
        .tolist()
    )

    print(
        "Missing PTM examples:",
        bad_examples
    )

    raise RuntimeError(
        "PTM Localization merge "
        "contains missing values. "
        "Stopping before MongoDB rebuild."
    )


print(
    "PTM Localization merge: OK"
)


# =========================================================
# 9. Diagnose source emergent summary/model differences
#
# We PRESERVE them. We do NOT modify them.
# =========================================================

emergent_summary_mismatches = []


for _, row in ps1_df.iterrows():

    phosphopeptide_id = (
        row["Phosphopeptide"]
    )


    summary_count = (
        safe_int(
            row.get(
                "Number of emergent models"
            )
        )
        or 0
    )


    model_count = 0


    for model in [
        "CI",
        "DEX",
        "TNF",
        "MPQ",
        "AA"
    ]:

        if emergent_value_present(
            row.get(
                f"{model} emergent"
            )
        ):

            model_count += 1


    if summary_count != model_count:

        emergent_summary_mismatches.append(
            (
                phosphopeptide_id,
                summary_count,
                model_count
            )
        )


print()
print(
    "Known source emergent "
    "summary/model mismatches:",
    len(
        emergent_summary_mismatches
    )
)


if emergent_summary_mismatches:

    print(
        "These will be preserved independently."
    )

    print(
        "First examples:"
    )

    for item in (
        emergent_summary_mismatches[:10]
    ):

        print(
            f"  {item[0]}: "
            f"summary={item[1]}, "
            f"model-specific={item[2]}"
        )


# =========================================================
# 10. Build PS1 phosphopeptide summary documents
# =========================================================

print()
print("=" * 72)
print("PREPARING PS1 PHOSPHOPEPTIDE DOCUMENTS")
print("=" * 72)


phospho_docs = []


for _, row in ps1_df.iterrows():

    gene = clean_value(
        row.get("Gene")
    )

    uniprot = clean_value(
        row.get("Uniprot")
    )


    if uniprot is None:

        uniprot = clean_value(
            row.get("UniProt")
        )


    site = clean_value(
        row.get("Site")
    )

    multiplicity = clean_value(
        row.get("Multiplicity")
    )


    # -----------------------------------------------------
    # Prefer the canonical source phosphopeptide ID.
    # Only reconstruct if source ID is unexpectedly absent.
    # -----------------------------------------------------

    source_phosphopeptide_id = (
        clean_value(
            row.get(
                "Phosphopeptide"
            )
        )
    )


    if source_phosphopeptide_id is not None:

        phosphopeptide_id = str(
            source_phosphopeptide_id
        ).strip()

    else:

        phosphopeptide_id = (
            make_phosphopeptide_id(
                gene=gene,
                uniprot=uniprot,
                site=site,
                multiplicity=multiplicity
            )
        )


    defective_count = safe_int(
        row.get(
            "Number of defective models"
        )
    )


    emergent_count = safe_int(
        row.get(
            "Number of emergent models"
        )
    )


    # -----------------------------------------------------
    # Preserve the original summary-based semantics.
    #
    # Do NOT derive this from individual model fields,
    # because source summary/model annotations are not
    # universally identical.
    # -----------------------------------------------------

    if (
        defective_count is not None
        and defective_count > 0
    ):

        status = "defective"

    elif (
        emergent_count is not None
        and emergent_count > 0
    ):

        status = "emergent"

    else:

        status = "normal_or_unclassified"


    doc = {

        "phosphopeptideId":
            phosphopeptide_id,

        "geneSymbol":
            gene,

        "uniprotId":
            uniprot,

        "site":
            site,

        "multiplicity":
            safe_int(
                multiplicity
            ),

        # -------------------------------------------------
        # FIXED:
        # This value now comes from the merged
        # quantification-sheet metadata.
        # -------------------------------------------------

        "ptmLocalisation":
            safe_float(
                row.get(
                    "PTM Localization"
                )
            ),

        "insulinRegulationStatus":
            status,

        "defectiveModelCount":
            defective_count,

        "emergentModelCount":
            emergent_count,

        "defects": {

            "CI":
                clean_value(
                    row.get(
                        "CI defect"
                    )
                ),

            "DEX":
                clean_value(
                    row.get(
                        "DEX defect"
                    )
                ),

            "TNF":
                clean_value(
                    row.get(
                        "TNF defect"
                    )
                ),

            "MPQ":
                clean_value(
                    row.get(
                        "MPQ defect"
                    )
                ),

            "AA":
                clean_value(
                    row.get(
                        "AA defect"
                    )
                )
        },

        "emergent": {

            "CI":
                clean_value(
                    row.get(
                        "CI emergent"
                    )
                ),

            "DEX":
                clean_value(
                    row.get(
                        "DEX emergent"
                    )
                ),

            "TNF":
                clean_value(
                    row.get(
                        "TNF emergent"
                    )
                ),

            "MPQ":
                clean_value(
                    row.get(
                        "MPQ emergent"
                    )
                ),

            "AA":
                clean_value(
                    row.get(
                        "AA emergent"
                    )
                )
        },

        "linkedProteinAnalyteId":
            make_protein_analyte_id(
                gene,
                uniprot
            ),

        "datasetId":
            "PS1"
    }


    phospho_docs.append(
        doc
    )


print(
    "Prepared phosphopeptide documents:",
    len(phospho_docs)
)


if len(
    phospho_docs
) != EXPECTED_PS1_ROWS:

    raise RuntimeError(
        "Prepared phosphopeptide "
        "document count mismatch."
    )


prepared_ptm_nulls = sum(
    1
    for doc in phospho_docs
    if doc[
        "ptmLocalisation"
    ] is None
)


print(
    "Prepared documents with "
    "null PTM Localisation:",
    prepared_ptm_nulls
)


if prepared_ptm_nulls != 0:

    raise RuntimeError(
        "Prepared MongoDB documents "
        "still contain null "
        "PTM Localisation values."
    )


# =========================================================
# 11. Important Pcm1 pre-import check
# =========================================================

print()
print("=" * 72)
print("PCM1 QUERY 7 PRE-IMPORT CHECK")
print("=" * 72)


pcm1_test_ids = {
    "Pcm1_Q9R0L6_S119_2",
    "Pcm1_Q9R0L6_S1959_1"
}


pcm1_docs = {
    doc["phosphopeptideId"]: doc
    for doc in phospho_docs
    if doc["phosphopeptideId"]
    in pcm1_test_ids
}


for phosphopeptide_id in (
    sorted(pcm1_test_ids)
):

    doc = pcm1_docs.get(
        phosphopeptide_id
    )


    if doc is None:

        print(
            phosphopeptide_id,
            "NOT FOUND"
        )

    else:

        print(
            phosphopeptide_id,
            "-> PTM Localization:",
            doc["ptmLocalisation"]
        )


# =========================================================
# 12. All source validation passed
# =========================================================

print()
print("=" * 72)
print("SOURCE VALIDATION PASSED")
print("=" * 72)

print(
    "TP1 sample documents:",
    len(sample_documents)
)

print(
    "TP1 measurements:",
    total_measurements
)

print(
    "PS1 phosphopeptide documents:",
    len(phospho_docs)
)

print(
    "PS1 PTM nulls:",
    prepared_ptm_nulls
)

print(
    "Known emergent source mismatches:",
    len(
        emergent_summary_mismatches
    )
)


print()
print(
    "WARNING:"
)

print(
    "Running the rebuild will DELETE "
    "the current Pattern 1 collections "
    "and recreate them."
)


confirmation = input(
    "\nType REBUILD to replace the "
    "current MongoDB Pattern 1 data: "
)


if confirmation != "REBUILD":

    print()
    print(
        "Rebuild cancelled. "
        "MongoDB was not modified."
    )

    raise SystemExit


# =========================================================
# 13. Connect MongoDB
# =========================================================

print()
print("=" * 72)
print("CONNECTING TO MONGODB")
print("=" * 72)


client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)


try:

    client.admin.command(
        "ping"
    )

    print(
        "MongoDB connection: OK"
    )


    db = client[
        DB_NAME
    ]


    samples_col = db[
        "samples"
    ]

    phospho_summary_col = db[
        "phosphopeptide_summaries"
    ]

    datasets_col = db[
        "datasets"
    ]


    # =====================================================
    # 14. Clear old imported Pattern 1 data
    # =====================================================

    print()
    print("=" * 72)
    print("CLEARING OLD PATTERN 1 DATA")
    print("=" * 72)


    samples_deleted = (
        samples_col.delete_many(
            {}
        ).deleted_count
    )


    phospho_deleted = (
        phospho_summary_col.delete_many(
            {}
        ).deleted_count
    )


    datasets_deleted = (
        datasets_col.delete_many(
            {}
        ).deleted_count
    )


    print(
        "Old samples deleted:",
        samples_deleted
    )

    print(
        "Old phosphopeptides deleted:",
        phospho_deleted
    )

    print(
        "Old datasets deleted:",
        datasets_deleted
    )


    # =====================================================
    # 15. Insert dataset metadata
    # =====================================================

    datasets_col.insert_many(
        [
            {
                "datasetId":
                    "TP1",

                "datasetName":
                    "Total proteome "
                    "quantification dataset",

                "dataType":
                    "total_proteome",

                "sourceFile":
                    TP1_FILE
            },

            {
                "datasetId":
                    "PS1",

                "datasetName":
                    "Phosphoproteome "
                    "summary dataset",

                "dataType":
                    "phosphoproteome",

                "sourceFile":
                    PS1_FILE
            }
        ]
    )


    print(
        "Dataset metadata inserted."
    )


    # =====================================================
    # 16. Insert TP1 samples
    # =====================================================

    if sample_documents:

        samples_col.insert_many(
            sample_documents
        )


    print(
        f"Inserted "
        f"{len(sample_documents)} "
        "sample documents."
    )


    # =====================================================
    # 17. Insert PS1 phosphopeptide summaries
    # =====================================================

    if phospho_docs:

        phospho_summary_col.insert_many(
            phospho_docs
        )


    print(
        f"Inserted "
        f"{len(phospho_docs)} "
        "phosphopeptide summary documents."
    )


    # =====================================================
    # 18. Create SAME benchmark indexes
    #
    # Keep these aligned with your existing Pattern 1
    # benchmark design.
    # =====================================================

    print()
    print("=" * 72)
    print("CREATING INDEXES")
    print("=" * 72)


    samples_col.create_index(
        [("sampleId", 1)]
    )

    samples_col.create_index(
        [("datasetId", 1)]
    )

    samples_col.create_index(
        [("condition.conditionId", 1)]
    )

    samples_col.create_index(
        [("condition.model", 1)]
    )

    samples_col.create_index(
        [
            (
                "totalProteomeMeasurements."
                "geneSymbol",
                1
            )
        ]
    )

    samples_col.create_index(
        [
            (
                "totalProteomeMeasurements."
                "uniprotId",
                1
            )
        ]
    )


    phospho_summary_col.create_index(
        [("geneSymbol", 1)]
    )

    phospho_summary_col.create_index(
        [("uniprotId", 1)]
    )

    phospho_summary_col.create_index(
        [
            (
                "insulinRegulationStatus",
                1
            )
        ]
    )

    phospho_summary_col.create_index(
        [("defectiveModelCount", 1)]
    )

    phospho_summary_col.create_index(
        [("emergentModelCount", 1)]
    )


    print(
        "Indexes created."
    )


    # =====================================================
    # 19. Final database audit
    # =====================================================

    print()
    print("=" * 72)
    print("FINAL DATABASE AUDIT")
    print("=" * 72)


    sample_count = (
        samples_col.count_documents(
            {}
        )
    )


    phospho_count = (
        phospho_summary_col.count_documents(
            {}
        )
    )


    dataset_count = (
        datasets_col.count_documents(
            {}
        )
    )


    mongo_ptm_nulls = (
        phospho_summary_col.count_documents(
            {
                "datasetId": "PS1",
                "ptmLocalisation": None
            }
        )
    )


    print(
        "samples:",
        sample_count
    )

    print(
        "phosphopeptide_summaries:",
        phospho_count
    )

    print(
        "datasets:",
        dataset_count
    )

    print(
        "PS1 null/missing "
        "ptmLocalisation:",
        mongo_ptm_nulls
    )


    if (
        sample_count
        != EXPECTED_TP1_SAMPLES
    ):

        raise RuntimeError(
            "Final TP1 sample count mismatch."
        )


    if (
        phospho_count
        != EXPECTED_PS1_ROWS
    ):

        raise RuntimeError(
            "Final PS1 phosphopeptide "
            "count mismatch."
        )


    if dataset_count != 2:

        raise RuntimeError(
            "Dataset metadata count mismatch."
        )


    if mongo_ptm_nulls != 0:

        raise RuntimeError(
            "PTM Localization nulls "
            "still exist after import."
        )


    # =====================================================
    # 20. Query 7 Pcm1 verification
    # =====================================================

    print()
    print("=" * 72)
    print("FINAL PCM1 QUERY 7 CHECK")
    print("=" * 72)


    for phosphopeptide_id in [
        "Pcm1_Q9R0L6_S119_2",
        "Pcm1_Q9R0L6_S1959_1"
    ]:

        doc = (
            phospho_summary_col.find_one(
                {
                    "datasetId": "PS1",

                    "phosphopeptideId":
                        phosphopeptide_id
                },
                {
                    "_id": 0,

                    "phosphopeptideId": 1,

                    "ptmLocalisation": 1,

                    "insulinRegulationStatus": 1,

                    "defectiveModelCount": 1,

                    "emergentModelCount": 1
                }
            )
        )


        print(
            doc
        )


    # =====================================================
    # 21. Example documents
    # =====================================================

    print()
    print(
        "Example sample document:"
    )


    example_sample = (
        samples_col.find_one(
            {},
            {
                "_id": 0,

                "sampleId": 1,

                "condition": 1,

                "totalProteomeMeasurements": {
                    "$slice": 2
                }
            }
        )
    )


    print(
        example_sample
    )


    print()
    print(
        "Example phosphopeptide summary:"
    )


    example_phospho = (
        phospho_summary_col.find_one(
            {},
            {
                "_id": 0
            }
        )
    )


    print(
        example_phospho
    )


    print()
    print("=" * 72)
    print(
        "PATTERN 1 IMPORT COMPLETED SUCCESSFULLY"
    )
    print("=" * 72)


finally:

    client.close()