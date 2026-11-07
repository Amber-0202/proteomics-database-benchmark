# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os

from pathlib import Path
from getpass import getpass
from io import StringIO

import numpy as np
import pandas as pd
import psycopg


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TP1_FILE = str(Path(os.environ.get("TP1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - TP1.xlsx")).expanduser())
PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

TP1_DATASET_ID = 1
PS1_DATASET_ID = 2

# These must match the Analyte IDs already imported
TP1_ANALYTE_START = 1
PS1_ANALYTE_START = 7171

EXPECTED_TP1_ANALYTES = 7170
EXPECTED_PS1_ANALYTES = 39814

EXPECTED_TP1_SAMPLES = 48
EXPECTED_PS1_SAMPLES = 52

EXPECTED_TP1_QUANT = 304911
EXPECTED_PS1_QUANT = 1136286
EXPECTED_TOTAL_QUANT = 1441197

# Number of analytes transformed at a time
CHUNK_SIZE = 1000


# =========================================================
# Database helpers
# =========================================================

def get_sample_map(cur, dataset_id):
    """
    Return:
        {
            "CTRL_BASAL_1": 1,
            "CTRL_BASAL_2": 2,
            ...
        }
    """

    cur.execute(
        '''
        SELECT id, name
        FROM "Sample"
        WHERE dataset = %s
        ORDER BY id;
        ''',
        (dataset_id,)
    )

    rows = cur.fetchall()

    return {
        name: sample_id
        for sample_id, name in rows
    }


# =========================================================
# Excel validation
# =========================================================

def read_and_validate_dataset(
    excel_file,
    dataset_id,
    metadata_columns,
    sample_map,
    expected_analytes,
    expected_samples,
    expected_quant
):
    """
    Read one raw workbook and confirm that:
      1. analyte count is correct
      2. sample columns exactly match PostgreSQL Sample rows
      3. measurement count is correct
      4. non-null measurement values are numeric and finite
    """

    print()
    print("=" * 65)
    print(f"Reading dataset {dataset_id}: {excel_file.name}")
    print("=" * 65)

    df = pd.read_excel(
        excel_file,
        sheet_name="quantification"
    )

    print("Rows:", len(df))

    # -----------------------------------------------------
    # Validate analyte rows
    # -----------------------------------------------------

    if len(df) != expected_analytes:
        raise ValueError(
            f"Dataset {dataset_id}: expected "
            f"{expected_analytes} analytes, "
            f"but found {len(df)}."
        )

    # -----------------------------------------------------
    # Check metadata columns exist
    # -----------------------------------------------------

    missing_metadata = [
        col
        for col in metadata_columns
        if col not in df.columns
    ]

    if missing_metadata:
        raise ValueError(
            f"Dataset {dataset_id}: missing metadata columns: "
            f"{missing_metadata}"
        )

    # -----------------------------------------------------
    # Identify sample columns
    # -----------------------------------------------------

    sample_columns = [
        col
        for col in df.columns
        if col not in metadata_columns
    ]

    print("Sample columns:", len(sample_columns))

    if len(sample_columns) != expected_samples:
        raise ValueError(
            f"Dataset {dataset_id}: expected "
            f"{expected_samples} sample columns, "
            f"but found {len(sample_columns)}."
        )

    if len(sample_columns) != len(set(sample_columns)):
        raise ValueError(
            f"Dataset {dataset_id}: duplicate sample "
            "column names found in Excel."
        )

    # -----------------------------------------------------
    # Compare Excel sample names with PostgreSQL
    # -----------------------------------------------------

    excel_samples = set(sample_columns)
    db_samples = set(sample_map.keys())

    missing_in_database = sorted(
        excel_samples - db_samples
    )

    extra_in_database = sorted(
        db_samples - excel_samples
    )

    if missing_in_database:
        raise ValueError(
            f"Dataset {dataset_id}: these Excel samples "
            f"are missing from PostgreSQL:\n"
            f"{missing_in_database}"
        )

    if extra_in_database:
        raise ValueError(
            f"Dataset {dataset_id}: PostgreSQL contains "
            f"samples not found in the Excel sheet:\n"
            f"{extra_in_database}"
        )

    print("Excel ↔ PostgreSQL sample mapping: OK")

    # -----------------------------------------------------
    # Make sure measurement values are numeric
    # -----------------------------------------------------

    for col in sample_columns:

        original = df[col]

        numeric = pd.to_numeric(
            original,
            errors="coerce"
        )

        # Original value existed, but could not be converted
        bad_mask = (
            original.notna()
            & numeric.isna()
        )

        if bad_mask.any():
            examples = (
                original[bad_mask]
                .head(10)
                .tolist()
            )

            raise ValueError(
                f"Dataset {dataset_id}: non-numeric values "
                f"found in sample column {col}: {examples}"
            )

        df[col] = numeric

    # -----------------------------------------------------
    # Count real measurements
    # -----------------------------------------------------

    measurement_count = int(
        df[sample_columns]
        .notna()
        .sum()
        .sum()
    )

    print(
        "Non-null measurements:",
        measurement_count
    )

    if measurement_count != expected_quant:
        raise ValueError(
            f"Dataset {dataset_id}: expected "
            f"{expected_quant} non-null measurements, "
            f"but found {measurement_count}."
        )

    print(
        f"Dataset {dataset_id} validation: OK"
    )

    return df, sample_columns


# =========================================================
# COPY one dataset
# =========================================================

def copy_dataset(
    cur,
    df,
    sample_columns,
    sample_map,
    dataset_id,
    analyte_start_id,
    expected_quant,
    quant_id_start
):
    """
    Convert wide Excel matrix into:

        id
        node
        analyte
        sample
        value
        dataset

    and COPY it into PostgreSQL in chunks.

    IMPORTANT:
    No normal SQL queries are executed while COPY is active.
    """

    print()
    print("=" * 65)
    print(
        f"Starting COPY for dataset {dataset_id}"
    )
    print("=" * 65)

    next_quant_id = quant_id_start
    inserted = 0

    copy_sql = '''
        COPY "Quantification" (
            id,
            node,
            analyte,
            sample,
            value,
            dataset
        )
        FROM STDIN
        WITH (
            FORMAT CSV,
            NULL ''
        )
    '''

    # -----------------------------------------------------
    # Enter COPY mode
    # -----------------------------------------------------

    with cur.copy(copy_sql) as copy:

        for start in range(
            0,
            len(df),
            CHUNK_SIZE
        ):

            end = min(
                start + CHUNK_SIZE,
                len(df)
            )

            # -------------------------------------------------
            # Get this block of quantification values
            # -------------------------------------------------

            block = (
                df.iloc[start:end][sample_columns]
                .copy()
            )

            # -------------------------------------------------
            # Add the Analyte IDs already used in database
            # -------------------------------------------------

            block.insert(
                0,
                "analyte",
                np.arange(
                    analyte_start_id + start,
                    analyte_start_id + end,
                    dtype=np.int64
                )
            )

            # -------------------------------------------------
            # Wide → long
            #
            # analyte | CTRL_1 | CTRL_2
            #
            # becomes
            #
            # analyte | sample_name | value
            # -------------------------------------------------

            long_df = block.melt(
                id_vars=["analyte"],
                var_name="sample_name",
                value_name="value"
            )

            # -------------------------------------------------
            # Do NOT insert missing measurements
            # -------------------------------------------------

            long_df = long_df.dropna(
                subset=["value"]
            )

            # -------------------------------------------------
            # Convert Sample.name → Sample.id
            # -------------------------------------------------

            long_df["sample"] = (
                long_df["sample_name"]
                .map(sample_map)
            )

            if long_df["sample"].isna().any():
                bad_samples = (
                    long_df.loc[
                        long_df["sample"].isna(),
                        "sample_name"
                    ]
                    .drop_duplicates()
                    .tolist()
                )

                raise ValueError(
                    f"Dataset {dataset_id}: failed to "
                    f"map sample names: {bad_samples}"
                )

            long_df["sample"] = (
                long_df["sample"]
                .astype(np.int64)
            )

            # -------------------------------------------------
            # Validate values
            # -------------------------------------------------

            long_df["value"] = pd.to_numeric(
                long_df["value"],
                errors="raise"
            )

            if not np.isfinite(
                long_df["value"].to_numpy(
                    dtype=float
                )
            ).all():

                raise ValueError(
                    f"Dataset {dataset_id}: "
                    "NaN/Infinity found after filtering."
                )

            n = len(long_df)

            # -------------------------------------------------
            # Quantification primary keys
            # -------------------------------------------------

            long_df.insert(
                0,
                "id",
                np.arange(
                    next_quant_id,
                    next_quant_id + n,
                    dtype=np.int64
                )
            )

            # Workflow node unavailable in raw data
            long_df.insert(
                1,
                "node",
                None
            )

            long_df["dataset"] = dataset_id

            # -------------------------------------------------
            # Final PostgreSQL column order
            # -------------------------------------------------

            output = long_df[
                [
                    "id",
                    "node",
                    "analyte",
                    "sample",
                    "value",
                    "dataset"
                ]
            ]

            # -------------------------------------------------
            # Write chunk as CSV text in memory
            # -------------------------------------------------

            buffer = StringIO()

            output.to_csv(
                buffer,
                index=False,
                header=False,
                na_rep=""
            )

            copy.write(
                buffer.getvalue()
            )

            # -------------------------------------------------
            # Update counters
            # -------------------------------------------------

            next_quant_id += n
            inserted += n

            print(
                f"Dataset {dataset_id}: "
                f"analytes {start + 1}-{end} | "
                f"measurements copied: {inserted}"
            )

    # COPY mode has ended here

    if inserted != expected_quant:
        raise RuntimeError(
            f"Dataset {dataset_id}: copied "
            f"{inserted} measurements, "
            f"expected {expected_quant}."
        )

    print()
    print(
        f"Dataset {dataset_id} COPY complete: "
        f"{inserted} measurements."
    )

    return next_quant_id


# =========================================================
# Main
# =========================================================

password = os.environ.get("PGPASSWORD") or getpass("PostgreSQL password: ")

conn = psycopg.connect(
    host=os.environ.get("PGHOST", "localhost"),
    port=int(os.environ.get("PGPORT", "5432")),
    dbname=os.environ.get("PGDATABASE", "protehome"),
    user=os.environ.get("PGUSER", "postgres"),
    password=password
)


try:

    with conn.cursor() as cur:

        # =====================================================
        # 1. Database safety checks
        # =====================================================

        cur.execute(
            'SELECT COUNT(*) FROM "Quantification";'
        )

        existing_quant = cur.fetchone()[0]

        print()
        print(
            "Existing Quantification rows:",
            existing_quant
        )

        if existing_quant != 0:
            raise RuntimeError(
                "Quantification table is not empty. "
                "Import stopped to prevent duplicates."
            )

        # -----------------------------------------------------
        # Verify analyte counts
        # -----------------------------------------------------

        cur.execute(
            '''
            SELECT dataset, COUNT(*)
            FROM "Analyte"
            GROUP BY dataset
            ORDER BY dataset;
            '''
        )

        analyte_counts = dict(
            cur.fetchall()
        )

        tp1_analyte_count = (
            analyte_counts.get(
                TP1_DATASET_ID,
                0
            )
        )

        ps1_analyte_count = (
            analyte_counts.get(
                PS1_DATASET_ID,
                0
            )
        )

        print(
            "TP1 analytes in PostgreSQL:",
            tp1_analyte_count
        )

        print(
            "PS1 analytes in PostgreSQL:",
            ps1_analyte_count
        )

        if (
            tp1_analyte_count
            != EXPECTED_TP1_ANALYTES
        ):
            raise RuntimeError(
                "TP1 Analyte count is incorrect."
            )

        if (
            ps1_analyte_count
            != EXPECTED_PS1_ANALYTES
        ):
            raise RuntimeError(
                "PS1 Analyte count is incorrect."
            )

        # =====================================================
        # 2. Fetch sample maps BEFORE COPY
        # =====================================================

        tp1_sample_map = get_sample_map(
            cur,
            TP1_DATASET_ID
        )

        ps1_sample_map = get_sample_map(
            cur,
            PS1_DATASET_ID
        )

        print()
        print(
            "TP1 samples in PostgreSQL:",
            len(tp1_sample_map)
        )

        print(
            "PS1 samples in PostgreSQL:",
            len(ps1_sample_map)
        )

        if (
            len(tp1_sample_map)
            != EXPECTED_TP1_SAMPLES
        ):
            raise RuntimeError(
                "TP1 Sample count is incorrect."
            )

        if (
            len(ps1_sample_map)
            != EXPECTED_PS1_SAMPLES
        ):
            raise RuntimeError(
                "PS1 Sample count is incorrect."
            )

        # =====================================================
        # 3. Read + validate Excel BEFORE COPY
        # =====================================================

        tp1_df, tp1_sample_columns = (
            read_and_validate_dataset(
                excel_file=TP1_FILE,
                dataset_id=TP1_DATASET_ID,
                metadata_columns=[
                    "Gene_Uniprot",
                    "Gene",
                    "Uniprot"
                ],
                sample_map=tp1_sample_map,
                expected_analytes=(
                    EXPECTED_TP1_ANALYTES
                ),
                expected_samples=(
                    EXPECTED_TP1_SAMPLES
                ),
                expected_quant=(
                    EXPECTED_TP1_QUANT
                )
            )
        )

        ps1_df, ps1_sample_columns = (
            read_and_validate_dataset(
                excel_file=PS1_FILE,
                dataset_id=PS1_DATASET_ID,
                metadata_columns=[
                    "Phosphopeptide",
                    "Gene",
                    "Uniprot",
                    "Site",
                    "Multiplicity",
                    "PTM Localization"
                ],
                sample_map=ps1_sample_map,
                expected_analytes=(
                    EXPECTED_PS1_ANALYTES
                ),
                expected_samples=(
                    EXPECTED_PS1_SAMPLES
                ),
                expected_quant=(
                    EXPECTED_PS1_QUANT
                )
            )
        )

        # =====================================================
        # 4. Confirmation
        # =====================================================

        print()
        print("=" * 65)
        print("PRE-IMPORT CHECK PASSED")
        print("=" * 65)

        print(
            "Expected TP1 Quantification:",
            EXPECTED_TP1_QUANT
        )

        print(
            "Expected PS1 Quantification:",
            EXPECTED_PS1_QUANT
        )

        print(
            "Expected total Quantification:",
            EXPECTED_TOTAL_QUANT
        )

        answer = input(
            "\nType IMPORT to begin Quantification COPY: "
        )

        if answer != "IMPORT":

            print("Import cancelled.")

            conn.rollback()

            raise SystemExit

        # =====================================================
        # 5. COPY TP1
        # =====================================================

        next_quant_id = 1

        next_quant_id = copy_dataset(
            cur=cur,
            df=tp1_df,
            sample_columns=tp1_sample_columns,
            sample_map=tp1_sample_map,
            dataset_id=TP1_DATASET_ID,
            analyte_start_id=TP1_ANALYTE_START,
            expected_quant=EXPECTED_TP1_QUANT,
            quant_id_start=next_quant_id
        )

        # -----------------------------------------------------
        # Now COPY is closed, normal SQL is safe again
        # -----------------------------------------------------

        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "Quantification"
            WHERE dataset = %s;
            ''',
            (TP1_DATASET_ID,)
        )

        tp1_db_count = cur.fetchone()[0]

        print()
        print(
            "TP1 rows currently in transaction:",
            tp1_db_count
        )

        if (
            tp1_db_count
            != EXPECTED_TP1_QUANT
        ):
            raise RuntimeError(
                "TP1 database count mismatch "
                "after COPY."
            )

        # =====================================================
        # 6. COPY PS1
        # =====================================================

        next_quant_id = copy_dataset(
            cur=cur,
            df=ps1_df,
            sample_columns=ps1_sample_columns,
            sample_map=ps1_sample_map,
            dataset_id=PS1_DATASET_ID,
            analyte_start_id=PS1_ANALYTE_START,
            expected_quant=EXPECTED_PS1_QUANT,
            quant_id_start=next_quant_id
        )

        # =====================================================
        # 7. Final database audit BEFORE COMMIT
        # =====================================================

        cur.execute(
            '''
            SELECT dataset, COUNT(*)
            FROM "Quantification"
            GROUP BY dataset
            ORDER BY dataset;
            '''
        )

        dataset_counts = dict(
            cur.fetchall()
        )

        final_tp1 = dataset_counts.get(
            TP1_DATASET_ID,
            0
        )

        final_ps1 = dataset_counts.get(
            PS1_DATASET_ID,
            0
        )

        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "Quantification";
            '''
        )

        final_total = cur.fetchone()[0]

        cur.execute(
            '''
            SELECT MIN(id), MAX(id)
            FROM "Quantification";
            '''
        )

        min_quant_id, max_quant_id = (
            cur.fetchone()
        )

        print()
        print("=" * 65)
        print("FINAL DATABASE CHECK")
        print("=" * 65)

        print(
            "TP1 Quantification:",
            final_tp1
        )

        print(
            "PS1 Quantification:",
            final_ps1
        )

        print(
            "Total Quantification:",
            final_total
        )

        print(
            "Quantification ID range:",
            min_quant_id,
            "to",
            max_quant_id
        )

        if final_tp1 != EXPECTED_TP1_QUANT:
            raise RuntimeError(
                "Final TP1 count mismatch."
            )

        if final_ps1 != EXPECTED_PS1_QUANT:
            raise RuntimeError(
                "Final PS1 count mismatch."
            )

        if final_total != EXPECTED_TOTAL_QUANT:
            raise RuntimeError(
                "Final total count mismatch."
            )

        if min_quant_id != 1:
            raise RuntimeError(
                "Quantification minimum ID is not 1."
            )

        if (
            max_quant_id
            != EXPECTED_TOTAL_QUANT
        ):
            raise RuntimeError(
                "Quantification maximum ID "
                "does not match row count."
            )

    # =========================================================
    # 8. Commit only after EVERYTHING passes
    # =========================================================

    conn.commit()

    print()
    print("=" * 65)
    print(
        "Quantification import completed successfully."
    )
    print("=" * 65)


except BaseException:

    # Includes ordinary exceptions and Ctrl+C
    conn.rollback()

    print()
    print("=" * 65)
    print(
        "IMPORT STOPPED — transaction rolled back."
    )
    print(
        "No partial Quantification import was committed."
    )
    print("=" * 65)

    raise


finally:

    conn.close()