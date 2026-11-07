# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os

from pathlib import Path
from datetime import datetime
import math

import pandas as pd
from pymongo import MongoClient, UpdateOne


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("MONGO_P1_DB", "proteomics_pattern1")
COLLECTION_NAME = "phosphopeptide_summaries"

DATASET_ID = "PS1"

EXPECTED_ROWS = 39814


# =========================================================
# Helper
# =========================================================

def values_equal(a, b):

    if a is None and b is None:
        return True

    if a is None or b is None:
        return False

    try:
        return math.isclose(
            float(a),
            float(b),
            rel_tol=1e-12,
            abs_tol=1e-12
        )

    except Exception:
        return False


# =========================================================
# STEP 1 — Read source Excel
# =========================================================

print()
print("=" * 72)
print("READING ORIGINAL PS1 PTM LOCALIZATION")
print("=" * 72)


source = pd.read_excel(
    PS1_FILE,
    sheet_name="quantification",
    usecols=[
        "Phosphopeptide",
        "PTM Localization"
    ]
)


source["Phosphopeptide"] = (
    source["Phosphopeptide"]
    .astype(str)
    .str.strip()
)


if len(source) != EXPECTED_ROWS:

    raise RuntimeError(
        f"Expected {EXPECTED_ROWS} rows, "
        f"found {len(source)}."
    )


if source["Phosphopeptide"].duplicated().any():

    raise RuntimeError(
        "Duplicate Phosphopeptide IDs "
        "found in source workbook."
    )


source["PTM Localization"] = pd.to_numeric(
    source["PTM Localization"],
    errors="coerce"
)


source_null_count = int(
    source["PTM Localization"]
    .isna()
    .sum()
)


print(
    "Source phosphopeptides:",
    len(source)
)

print(
    "Source PTM Localization nulls:",
    source_null_count
)


if source_null_count != 0:

    raise RuntimeError(
        "Unexpected missing PTM Localization "
        "values in source Excel."
    )


source_map = {

    row["Phosphopeptide"]:
        float(row["PTM Localization"])

    for _, row in source.iterrows()
}


print(
    "Source validation: OK"
)


# =========================================================
# STEP 2 — Connect MongoDB
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

    collection = db[
        COLLECTION_NAME
    ]


    # =====================================================
    # STEP 3 — Read current MongoDB PS1 documents
    # =====================================================

    print()
    print("=" * 72)
    print("CHECKING CURRENT MONGODB DATA")
    print("=" * 72)


    mongo_docs = list(
        collection.find(
            {
                "datasetId":
                    DATASET_ID
            },
            {
                "_id": 1,
                "phosphopeptideId": 1,
                "ptmLocalisation": 1
            }
        )
    )


    print(
        "MongoDB PS1 documents:",
        len(mongo_docs)
    )


    if len(mongo_docs) != EXPECTED_ROWS:

        raise RuntimeError(
            f"Expected {EXPECTED_ROWS} MongoDB "
            f"documents, found {len(mongo_docs)}."
        )


    mongo_ids = []


    for doc in mongo_docs:

        phosphopeptide_id = doc.get(
            "phosphopeptideId"
        )

        if phosphopeptide_id is None:

            raise RuntimeError(
                "MongoDB document found without "
                "phosphopeptideId."
            )

        mongo_ids.append(
            str(
                phosphopeptide_id
            ).strip()
        )


    if len(
        mongo_ids
    ) != len(
        set(mongo_ids)
    ):

        raise RuntimeError(
            "Duplicate phosphopeptideId "
            "values found in MongoDB."
        )


    source_ids = set(
        source_map.keys()
    )

    mongo_id_set = set(
        mongo_ids
    )


    missing_in_mongo = (
        source_ids
        - mongo_id_set
    )


    extra_in_mongo = (
        mongo_id_set
        - source_ids
    )


    print(
        "IDs missing from MongoDB:",
        len(missing_in_mongo)
    )

    print(
        "Extra IDs in MongoDB:",
        len(extra_in_mongo)
    )


    if (
        missing_in_mongo
        or extra_in_mongo
    ):

        raise RuntimeError(
            "Excel ↔ MongoDB IDs do not match. "
            "No update performed."
        )


    print(
        "Excel ↔ MongoDB IDs: OK"
    )


    # =====================================================
    # STEP 4 — Detect actual mismatches
    # =====================================================

    mismatches = []


    for doc in mongo_docs:

        phosphopeptide_id = str(
            doc["phosphopeptideId"]
        ).strip()


        mongo_value = doc.get(
            "ptmLocalisation"
        )


        source_value = source_map[
            phosphopeptide_id
        ]


        if not values_equal(
            mongo_value,
            source_value
        ):

            mismatches.append(
                {
                    "_id":
                        doc["_id"],

                    "phosphopeptideId":
                        phosphopeptide_id,

                    "mongo_value":
                        mongo_value,

                    "source_value":
                        source_value
                }
            )


    mongo_null_count = (
        collection.count_documents(
            {
                "datasetId":
                    DATASET_ID,

                "ptmLocalisation":
                    None
            }
        )
    )


    missing_field_count = (
        collection.count_documents(
            {
                "datasetId":
                    DATASET_ID,

                "ptmLocalisation": {
                    "$exists":
                        False
                }
            }
        )
    )


    print()
    print(
        "PTM Localization mismatches:",
        len(mismatches)
    )

    print(
        "Current null/missing values:",
        mongo_null_count
    )

    print(
        "Field completely missing:",
        missing_field_count
    )


    # =====================================================
    # Show examples
    # =====================================================

    if mismatches:

        print()
        print(
            "First mismatch examples:"
        )

        print(
            "-" * 72
        )


        for item in mismatches[:20]:

            print(
                item["phosphopeptideId"],
                "| MongoDB:",
                item["mongo_value"],
                "| Source:",
                item["source_value"]
            )


    # =====================================================
    # Query 7 Pcm1 diagnostic
    # =====================================================

    print()
    print("=" * 72)
    print("QUERY 7 PCM1 CHECK")
    print("=" * 72)


    pcm1_ids = [
        "Pcm1_Q9R0L6_S119_2",
        "Pcm1_Q9R0L6_S1959_1"
    ]


    for phosphopeptide_id in pcm1_ids:

        doc = collection.find_one(
            {
                "datasetId":
                    DATASET_ID,

                "phosphopeptideId":
                    phosphopeptide_id
            },
            {
                "_id": 0,
                "phosphopeptideId": 1,
                "ptmLocalisation": 1
            }
        )


        print()
        print(
            phosphopeptide_id
        )

        print(
            "  MongoDB:",
            None
            if doc is None
            else doc.get(
                "ptmLocalisation"
            )
        )

        print(
            "  Source :",
            source_map.get(
                phosphopeptide_id
            )
        )


    # =====================================================
    # Already correct?
    # =====================================================

    if not mismatches:

        print()
        print("=" * 72)
        print(
            "NO PTM LOCALIZATION "
            "MISMATCHES FOUND"
        )
        print("=" * 72)

        raise SystemExit


    # =====================================================
    # STEP 5 — Backup mismatched values
    # =====================================================

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )


    backup_file = (
        PROJECT_ROOT
        / (
            "mongodb_ptm_localisation_backup_"
            f"{timestamp}.csv"
        )
    )


    backup_df = pd.DataFrame(
        [
            {
                "phosphopeptideId":
                    item[
                        "phosphopeptideId"
                    ],

                "old_ptmLocalisation":
                    item[
                        "mongo_value"
                    ],

                "source_ptmLocalisation":
                    item[
                        "source_value"
                    ]
            }

            for item in mismatches
        ]
    )


    backup_df.to_csv(
        backup_file,
        index=False
    )


    print()
    print("=" * 72)
    print("BACKUP CREATED")
    print("=" * 72)

    print(
        backup_file
    )


    # =====================================================
    # STEP 6 — Confirmation
    # =====================================================

    print()
    print("=" * 72)
    print("READY TO FIX MONGODB")
    print("=" * 72)

    print(
        "Database:",
        DB_NAME
    )

    print(
        "Collection:",
        COLLECTION_NAME
    )

    print(
        "Dataset:",
        DATASET_ID
    )

    print(
        "Documents requiring update:",
        len(mismatches)
    )


    print()
    print(
        "ONLY this field will be changed:"
    )

    print(
        "    ptmLocalisation"
    )

    print()
    print(
        "The samples collection "
        "will NOT be modified."
    )


    confirmation = input(
        "\nType FIX to update MongoDB: "
    )


    if confirmation != "FIX":

        print()
        print(
            "Update cancelled."
        )

        raise SystemExit


    # =====================================================
    # STEP 7 — Bulk update
    # =====================================================

    operations = []


    for item in mismatches:

        operations.append(
            UpdateOne(
                {
                    "datasetId":
                        DATASET_ID,

                    "phosphopeptideId":
                        item[
                            "phosphopeptideId"
                        ]
                },
                {
                    "$set": {
                        "ptmLocalisation":
                            float(
                                item[
                                    "source_value"
                                ]
                            )
                    }
                }
            )
        )


    print()
    print(
        "Updating MongoDB..."
    )


    result = collection.bulk_write(
        operations,
        ordered=False
    )


    print()
    print("=" * 72)
    print("BULK UPDATE RESULT")
    print("=" * 72)

    print(
        "Matched:",
        result.matched_count
    )

    print(
        "Modified:",
        result.modified_count
    )


    # =====================================================
    # STEP 8 — Verify full collection
    # =====================================================

    print()
    print("=" * 72)
    print("POST-UPDATE VERIFICATION")
    print("=" * 72)


    after_docs = list(
        collection.find(
            {
                "datasetId":
                    DATASET_ID
            },
            {
                "_id": 0,
                "phosphopeptideId": 1,
                "ptmLocalisation": 1
            }
        )
    )


    remaining_mismatches = []


    for doc in after_docs:

        phosphopeptide_id = str(
            doc["phosphopeptideId"]
        ).strip()


        mongo_value = doc.get(
            "ptmLocalisation"
        )


        source_value = source_map[
            phosphopeptide_id
        ]


        if not values_equal(
            mongo_value,
            source_value
        ):

            remaining_mismatches.append(
                (
                    phosphopeptide_id,
                    mongo_value,
                    source_value
                )
            )


    null_after = (
        collection.count_documents(
            {
                "datasetId":
                    DATASET_ID,

                "ptmLocalisation":
                    None
            }
        )
    )


    print(
        "Documents checked:",
        len(after_docs)
    )

    print(
        "Remaining mismatches:",
        len(
            remaining_mismatches
        )
    )

    print(
        "Remaining null/missing values:",
        null_after
    )


    if remaining_mismatches:

        print()
        print(
            "Remaining mismatch examples:"
        )

        for item in (
            remaining_mismatches[:20]
        ):

            print(
                item
            )


        raise RuntimeError(
            "Verification failed."
        )


    if null_after != 0:

        raise RuntimeError(
            "Null PTM Localization values "
            "remain after update."
        )


    # =====================================================
    # STEP 9 — Final Pcm1 verification
    # =====================================================

    print()
    print("=" * 72)
    print("FINAL PCM1 QUERY 7 CHECK")
    print("=" * 72)


    for phosphopeptide_id in pcm1_ids:

        doc = collection.find_one(
            {
                "datasetId":
                    DATASET_ID,

                "phosphopeptideId":
                    phosphopeptide_id
            },
            {
                "_id": 0,
                "phosphopeptideId": 1,
                "ptmLocalisation": 1
            }
        )


        print(
            phosphopeptide_id,
            "->",
            doc.get(
                "ptmLocalisation"
            )
        )


    print()
    print("=" * 72)
    print(
        "MONGODB PTM LOCALIZATION "
        "FIX COMPLETED SUCCESSFULLY"
    )
    print("=" * 72)


finally:

    client.close()