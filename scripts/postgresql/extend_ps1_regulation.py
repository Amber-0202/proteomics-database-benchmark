# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os

from pathlib import Path
from getpass import getpass

import numpy as np
import pandas as pd
import psycopg


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

EXPECTED_PS1_ROWS = 39814

MODELS = [
    ("CI", 1),
    ("DEX", 2),
    ("TNF", 3),
    ("MPQ", 4),
    ("AA", 5),
]


# =========================================================
# Parsing helpers
# =========================================================

def parse_defect(value, phosphopeptide, model):

    if pd.isna(value):
        return False

    if isinstance(value, (bool, np.bool_)):
        return bool(value)

    text = str(value).strip().lower()

    if text in {
        "",
        "false",
        "f",
        "0",
        "no",
        "n",
        "none",
        "nan",
        "na",
    }:
        return False

    if text in {
        "true",
        "t",
        "1",
        "yes",
        "y",
    }:
        return True

    raise ValueError(
        f"{phosphopeptide}: "
        f"cannot interpret {model} defect value {value!r}"
    )


def parse_emergent(value, phosphopeptide, model):

    if pd.isna(value):
        return None

    if isinstance(value, (bool, np.bool_)):
        if value is False:
            return None

    text = str(value).strip().lower()

    if text in {
        "",
        "false",
        "f",
        "0",
        "no",
        "n",
        "none",
        "nan",
        "na",
    }:
        return None

    if text in {
        "up",
        "upregulated",
        "up-regulated",
        "increase",
        "increased",
    }:
        return "up"

    if text in {
        "down",
        "downregulated",
        "down-regulated",
        "decrease",
        "decreased",
    }:
        return "down"

    raise ValueError(
        f"{phosphopeptide}: "
        f"cannot interpret {model} emergent value {value!r}"
    )


def parse_count(value, label):

    if pd.isna(value):
        return 0

    number = float(value)

    if not number.is_integer():
        raise ValueError(
            f"{label}: expected integer, got {value!r}"
        )

    number = int(number)

    if number < 0 or number > 5:
        raise ValueError(
            f"{label}: outside expected range 0–5: {number}"
        )

    return number


def parse_ptm(value):

    if pd.isna(value):
        return None

    try:
        number = float(value)
    except Exception:
        return None

    if not np.isfinite(number):
        return None

    return number


# =========================================================
# Read source workbook
# =========================================================

print()
print("=" * 70)
print("READING PS1 REGULATION DATA")
print("=" * 70)


analysis = pd.read_excel(
    PS1_FILE,
    sheet_name="analysis",
    usecols=[
        "Phosphopeptide",
        "Multiplicity",
        "Number of defective models",
        "CI defect",
        "DEX defect",
        "TNF defect",
        "MPQ defect",
        "AA defect",
        "Number of emergent models",
        "CI emergent",
        "DEX emergent",
        "TNF emergent",
        "MPQ emergent",
        "AA emergent",
    ],
)


quant = pd.read_excel(
    PS1_FILE,
    sheet_name="quantification",
    usecols=[
        "Phosphopeptide",
        "PTM Localization",
    ],
)


# =========================================================
# Basic source checks
# =========================================================

if len(analysis) != EXPECTED_PS1_ROWS:

    raise ValueError(
        f"Expected {EXPECTED_PS1_ROWS} analysis rows, "
        f"found {len(analysis)}."
    )


if len(quant) != EXPECTED_PS1_ROWS:

    raise ValueError(
        f"Expected {EXPECTED_PS1_ROWS} quantification rows, "
        f"found {len(quant)}."
    )


analysis["Phosphopeptide"] = (
    analysis["Phosphopeptide"]
    .astype(str)
    .str.strip()
)

quant["Phosphopeptide"] = (
    quant["Phosphopeptide"]
    .astype(str)
    .str.strip()
)


if analysis["Phosphopeptide"].duplicated().any():

    raise ValueError(
        "Duplicate phosphopeptide IDs in analysis sheet."
    )


if quant["Phosphopeptide"].duplicated().any():

    raise ValueError(
        "Duplicate phosphopeptide IDs in quantification sheet."
    )


raw = analysis.merge(
    quant,
    on="Phosphopeptide",
    how="left",
    validate="one_to_one",
)


if len(raw) != EXPECTED_PS1_ROWS:

    raise ValueError(
        "Analysis/quantification merge row count mismatch."
    )


print(
    f"PS1 phosphopeptides loaded: {len(raw)}"
)


# =========================================================
# Parse all annotations
# =========================================================

print()
print("=" * 70)
print("VALIDATING MODEL-SPECIFIC ANNOTATIONS")
print("=" * 70)


metadata_by_id = {}
model_rows_by_id = {}

emergent_mismatches = []
defective_mismatches = []


for _, row in raw.iterrows():

    phosphopeptide_id = row["Phosphopeptide"]


    # -----------------------------------------------------
    # Multiplicity
    # -----------------------------------------------------

    multiplicity_raw = row["Multiplicity"]

    if pd.isna(multiplicity_raw):

        raise ValueError(
            f"{phosphopeptide_id}: missing Multiplicity"
        )


    multiplicity_float = float(
        multiplicity_raw
    )

    if not multiplicity_float.is_integer():

        raise ValueError(
            f"{phosphopeptide_id}: "
            f"invalid Multiplicity {multiplicity_raw!r}"
        )


    multiplicity = int(
        multiplicity_float
    )


    # -----------------------------------------------------
    # PTM Localization
    # -----------------------------------------------------

    ptm_localisation = parse_ptm(
        row["PTM Localization"]
    )


    # -----------------------------------------------------
    # Stored summary counts
    # -----------------------------------------------------

    stored_defective_count = parse_count(
        row["Number of defective models"],
        f"{phosphopeptide_id} defective count",
    )


    stored_emergent_count = parse_count(
        row["Number of emergent models"],
        f"{phosphopeptide_id} emergent count",
    )


    # -----------------------------------------------------
    # Model-specific annotations
    # -----------------------------------------------------

    parsed_models = []

    actual_defective_count = 0
    actual_emergent_count = 0


    for model, model_order in MODELS:

        defective = parse_defect(
            row[f"{model} defect"],
            phosphopeptide_id,
            model,
        )


        emergent_direction = parse_emergent(
            row[f"{model} emergent"],
            phosphopeptide_id,
            model,
        )


        if defective:
            actual_defective_count += 1


        if emergent_direction is not None:
            actual_emergent_count += 1


        parsed_models.append(
            (
                model,
                model_order,
                defective,
                emergent_direction,
            )
        )


    # -----------------------------------------------------
    # Defective counts ARE internally consistent
    # -----------------------------------------------------

    if (
        stored_defective_count
        != actual_defective_count
    ):

        defective_mismatches.append(
            (
                phosphopeptide_id,
                stored_defective_count,
                actual_defective_count,
            )
        )


    # -----------------------------------------------------
    # Emergent counts are NOT always equal to model flags.
    #
    # IMPORTANT:
    # We intentionally preserve BOTH independently because
    # MongoDB also stores/projects these independently.
    # -----------------------------------------------------

    if (
        stored_emergent_count
        != actual_emergent_count
    ):

        emergent_mismatches.append(
            (
                phosphopeptide_id,
                stored_emergent_count,
                actual_emergent_count,
            )
        )


    metadata_by_id[
        phosphopeptide_id
    ] = (
        multiplicity,
        ptm_localisation,
        stored_defective_count,
        stored_emergent_count,
    )


    model_rows_by_id[
        phosphopeptide_id
    ] = parsed_models


# =========================================================
# Defective mismatch is unexpected -> stop
# =========================================================

if defective_mismatches:

    print()
    print(
        "Unexpected defective-count mismatches:"
    )

    for item in defective_mismatches[:20]:
        print(item)

    raise ValueError(
        "Defective summary counts do not match "
        "model-specific defect flags."
    )


print(
    "Defective summary ↔ model flags: OK"
)


# =========================================================
# Emergent mismatches are preserved, not corrected
# =========================================================

print()
print(
    "Emergent summary/model mismatches:",
    len(emergent_mismatches),
)


if emergent_mismatches:

    print()
    print(
        "These are present in the source workbook "
        "and will be preserved as-is."
    )

    print(
        "First examples:"
    )

    for item in emergent_mismatches[:10]:

        print(
            f"  {item[0]}: "
            f"summary={item[1]}, "
            f"model-specific={item[2]}"
        )


print()
print(
    "Validated phosphopeptides:",
    len(metadata_by_id),
)

print(
    "Model-specific rows to create:",
    len(metadata_by_id) * 5,
)


# =========================================================
# PostgreSQL connection
# =========================================================

password = os.environ.get("PGPASSWORD") or getpass("PostgreSQL password: ")


conn = psycopg.connect(
    host=os.environ.get("PGHOST", "localhost"),
    port=int(os.environ.get("PGPORT", "5432")),
    dbname=os.environ.get("PGDATABASE", "protehome"),
    user=os.environ.get("PGUSER", "postgres"),
    password=password,
)


try:

    with conn.cursor() as cur:

        # =================================================
        # Read existing regulation helper table
        # =================================================

        cur.execute(
            '''
            SELECT
                analyte,
                phosphopeptide_id,
                defective_model_count,
                emergent_model_count

            FROM "PhosphopeptideRegulation";
            '''
        )


        db_rows = cur.fetchall()


        if len(db_rows) != EXPECTED_PS1_ROWS:

            raise RuntimeError(
                f"Expected {EXPECTED_PS1_ROWS} rows in "
                "PhosphopeptideRegulation, "
                f"found {len(db_rows)}."
            )


        db_map = {}

        for (
            analyte,
            phosphopeptide_id,
            defective_count,
            emergent_count,
        ) in db_rows:

            db_map[
                phosphopeptide_id
            ] = (
                analyte,
                defective_count,
                emergent_count,
            )


        source_ids = set(
            metadata_by_id.keys()
        )

        db_ids = set(
            db_map.keys()
        )


        if source_ids != db_ids:

            print()
            print(
                "Missing in PostgreSQL:",
                list(source_ids - db_ids)[:10],
            )

            print(
                "Missing in source:",
                list(db_ids - source_ids)[:10],
            )

            raise RuntimeError(
                "Source/PostgreSQL phosphopeptide IDs "
                "do not match."
            )


        print()
        print(
            "Source ↔ PostgreSQL phosphopeptide IDs: OK"
        )


        # =================================================
        # Make sure aggregate summary values already stored
        # in PostgreSQL still match source summary columns
        # =================================================

        for phosphopeptide_id in source_ids:

            (
                _,
                db_defective_count,
                db_emergent_count,
            ) = db_map[
                phosphopeptide_id
            ]


            (
                _,
                _,
                source_defective_count,
                source_emergent_count,
            ) = metadata_by_id[
                phosphopeptide_id
            ]


            if (
                db_defective_count
                != source_defective_count
            ):

                raise RuntimeError(
                    f"{phosphopeptide_id}: "
                    "PostgreSQL defective count "
                    "differs from source summary."
                )


            if (
                db_emergent_count
                != source_emergent_count
            ):

                raise RuntimeError(
                    f"{phosphopeptide_id}: "
                    "PostgreSQL emergent count "
                    "differs from source summary."
                )


        print(
            "Existing aggregate counts: OK"
        )


        # =================================================
        # Extend helper table
        # =================================================

        cur.execute(
            '''
            ALTER TABLE "PhosphopeptideRegulation"

            ADD COLUMN IF NOT EXISTS
                multiplicity SMALLINT;
            '''
        )


        cur.execute(
            '''
            ALTER TABLE "PhosphopeptideRegulation"

            ADD COLUMN IF NOT EXISTS
                ptm_localisation DOUBLE PRECISION;
            '''
        )


        # =================================================
        # Model-level normalized relation
        # =================================================

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            "PhosphopeptideModelRegulation" (

                analyte BIGINT NOT NULL,

                model VARCHAR(3) NOT NULL,

                model_order SMALLINT NOT NULL,

                defective BOOLEAN
                    NOT NULL
                    DEFAULT FALSE,

                emergent_direction VARCHAR(4),

                PRIMARY KEY (
                    analyte,
                    model
                ),

                CONSTRAINT
                    fk_ppmodelreg_analyte
                FOREIGN KEY (analyte)
                REFERENCES "Analyte"(id),

                CONSTRAINT
                    ck_ppmodelreg_model
                CHECK (
                    model IN (
                        'CI',
                        'DEX',
                        'TNF',
                        'MPQ',
                        'AA'
                    )
                ),

                CONSTRAINT
                    ck_ppmodelreg_order
                CHECK (
                    model_order BETWEEN 1 AND 5
                ),

                CONSTRAINT
                    ck_ppmodelreg_emergent
                CHECK (
                    emergent_direction
                    IN ('up', 'down')
                    OR
                    emergent_direction IS NULL
                )
            );
            '''
        )


        # =================================================
        # Prevent accidental duplicate import
        # =================================================

        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "PhosphopeptideModelRegulation";
            '''
        )


        existing_model_rows = (
            cur.fetchone()[0]
        )


        print(
            "Existing model-regulation rows:",
            existing_model_rows,
        )


        if existing_model_rows != 0:

            raise RuntimeError(
                "PhosphopeptideModelRegulation "
                "already contains rows. "
                "Import stopped."
            )


        # =================================================
        # Prepare rows
        # =================================================

        extension_rows = []
        model_insert_rows = []


        for phosphopeptide_id in source_ids:

            analyte = (
                db_map[
                    phosphopeptide_id
                ][0]
            )


            (
                multiplicity,
                ptm_localisation,
                _,
                _,
            ) = metadata_by_id[
                phosphopeptide_id
            ]


            extension_rows.append(
                (
                    analyte,
                    multiplicity,
                    ptm_localisation,
                )
            )


            for (
                model,
                model_order,
                defective,
                emergent_direction,
            ) in model_rows_by_id[
                phosphopeptide_id
            ]:

                model_insert_rows.append(
                    (
                        analyte,
                        model,
                        model_order,
                        defective,
                        emergent_direction,
                    )
                )


        expected_model_rows = (
            EXPECTED_PS1_ROWS * 5
        )


        if (
            len(model_insert_rows)
            != expected_model_rows
        ):

            raise RuntimeError(
                "Model row count preparation error."
            )


        # =================================================
        # Confirmation
        # =================================================

        print()
        print("=" * 70)
        print("PRE-IMPORT CHECK PASSED")
        print("=" * 70)

        print(
            "Phosphopeptide rows to update:",
            len(extension_rows),
        )

        print(
            "Model annotation rows to insert:",
            len(model_insert_rows),
        )

        print(
            "Known emergent summary/model mismatches:",
            len(emergent_mismatches),
        )


        answer = input(
            "\nType EXTEND to continue: "
        )


        if answer != "EXTEND":

            conn.rollback()

            print(
                "Extension cancelled."
            )

            raise SystemExit


        # =================================================
        # Metadata staging table
        # =================================================

        cur.execute(
            '''
            CREATE TEMP TABLE
            tmp_ps1_extension (

                analyte BIGINT PRIMARY KEY,

                multiplicity SMALLINT NOT NULL,

                ptm_localisation
                    DOUBLE PRECISION

            ) ON COMMIT DROP;
            '''
        )


        print()
        print(
            "COPYing Multiplicity / PTM Localization..."
        )


        with cur.copy(
            '''
            COPY tmp_ps1_extension (
                analyte,
                multiplicity,
                ptm_localisation
            )
            FROM STDIN
            '''
        ) as copy:

            for row in extension_rows:

                copy.write_row(row)


        # =================================================
        # Update helper table
        # =================================================

        cur.execute(
            '''
            UPDATE
                "PhosphopeptideRegulation" pr

            SET
                multiplicity =
                    src.multiplicity,

                ptm_localisation =
                    src.ptm_localisation

            FROM
                tmp_ps1_extension src

            WHERE
                pr.analyte = src.analyte;
            '''
        )


        if cur.rowcount != EXPECTED_PS1_ROWS:

            raise RuntimeError(
                f"Expected {EXPECTED_PS1_ROWS} updates, "
                f"got {cur.rowcount}."
            )


        # =================================================
        # Insert model-specific values
        # =================================================

        print(
            "COPYing model-specific annotations..."
        )


        with cur.copy(
            '''
            COPY "PhosphopeptideModelRegulation" (
                analyte,
                model,
                model_order,
                defective,
                emergent_direction
            )
            FROM STDIN
            '''
        ) as copy:

            for row in model_insert_rows:

                copy.write_row(row)


        # =================================================
        # Index useful for Query 7
        # =================================================

        cur.execute(
            '''
            CREATE INDEX IF NOT EXISTS
                idx_ppreg_gene_symbol

            ON "PhosphopeptideRegulation"
                (gene_symbol);
            '''
        )


        # =================================================
        # Final audit
        # =================================================

        print()
        print("=" * 70)
        print("FINAL DATABASE AUDIT")
        print("=" * 70)


        cur.execute(
            '''
            SELECT
                COUNT(*),

                COUNT(*) FILTER (
                    WHERE multiplicity IS NULL
                ),

                COUNT(*) FILTER (
                    WHERE ptm_localisation
                    IS NOT NULL
                )

            FROM
                "PhosphopeptideRegulation";
            '''
        )


        (
            total_regulation_rows,
            missing_multiplicity,
            ptm_values_present,
        ) = cur.fetchone()


        print(
            "PhosphopeptideRegulation:",
            total_regulation_rows,
        )

        print(
            "Missing multiplicity:",
            missing_multiplicity,
        )

        print(
            "PTM Localization values present:",
            ptm_values_present,
        )


        cur.execute(
            '''
            SELECT
                COUNT(*),
                COUNT(DISTINCT analyte)

            FROM
                "PhosphopeptideModelRegulation";
            '''
        )


        (
            model_row_count,
            model_analytes,
        ) = cur.fetchone()


        print(
            "Model regulation rows:",
            model_row_count,
        )

        print(
            "Model regulation analytes:",
            model_analytes,
        )


        # -------------------------------------------------
        # Every phosphopeptide should have five model rows
        # -------------------------------------------------

        cur.execute(
            '''
            SELECT COUNT(*)

            FROM (
                SELECT
                    analyte

                FROM
                    "PhosphopeptideModelRegulation"

                GROUP BY analyte

                HAVING COUNT(*) <> 5
            ) x;
            '''
        )


        wrong_model_counts = (
            cur.fetchone()[0]
        )


        print(
            "Analytes without exactly 5 models:",
            wrong_model_counts,
        )


        # -------------------------------------------------
        # Defective aggregate/model counts SHOULD match
        # -------------------------------------------------

        cur.execute(
            '''
            WITH model_counts AS (

                SELECT
                    analyte,

                    COUNT(*) FILTER (
                        WHERE defective = TRUE
                    ) AS defect_count

                FROM
                    "PhosphopeptideModelRegulation"

                GROUP BY analyte
            )

            SELECT COUNT(*)

            FROM
                "PhosphopeptideRegulation" pr

            JOIN model_counts mc
                ON mc.analyte = pr.analyte

            WHERE
                pr.defective_model_count
                <> mc.defect_count;
            '''
        )


        defective_db_mismatches = (
            cur.fetchone()[0]
        )


        print(
            "Defective aggregate/model mismatches:",
            defective_db_mismatches,
        )


        # -------------------------------------------------
        # Emergent mismatches are informational ONLY
        # -------------------------------------------------

        cur.execute(
            '''
            WITH model_counts AS (

                SELECT
                    analyte,

                    COUNT(*) FILTER (
                        WHERE emergent_direction
                        IS NOT NULL
                    ) AS emergent_count

                FROM
                    "PhosphopeptideModelRegulation"

                GROUP BY analyte
            )

            SELECT COUNT(*)

            FROM
                "PhosphopeptideRegulation" pr

            JOIN model_counts mc
                ON mc.analyte = pr.analyte

            WHERE
                pr.emergent_model_count
                <> mc.emergent_count;
            '''
        )


        emergent_db_mismatches = (
            cur.fetchone()[0]
        )


        print(
            "Emergent aggregate/model mismatches "
            "(preserved from source):",
            emergent_db_mismatches,
        )


        # =================================================
        # Required checks
        # =================================================

        if (
            total_regulation_rows
            != EXPECTED_PS1_ROWS
        ):

            raise RuntimeError(
                "Regulation row count mismatch."
            )


        if missing_multiplicity != 0:

            raise RuntimeError(
                "Missing multiplicity values found."
            )


        if (
            model_row_count
            != expected_model_rows
        ):

            raise RuntimeError(
                "Model relation row count mismatch."
            )


        if (
            model_analytes
            != EXPECTED_PS1_ROWS
        ):

            raise RuntimeError(
                "Model relation analyte count mismatch."
            )


        if wrong_model_counts != 0:

            raise RuntimeError(
                "Some analytes do not have "
                "exactly five model rows."
            )


        if defective_db_mismatches != 0:

            raise RuntimeError(
                "Defective counts do not match."
            )


    # =====================================================
    # Commit
    # =====================================================

    conn.commit()


    print()
    print("=" * 70)
    print(
        "PS1 regulation extension "
        "completed successfully."
    )
    print("=" * 70)

    print()
    print(
        "NOTE: emergent aggregate/model mismatches "
        "were intentionally preserved."
    )


except BaseException:

    conn.rollback()

    print()
    print("=" * 70)
    print(
        "EXTENSION STOPPED — "
        "transaction rolled back."
    )
    print("=" * 70)

    raise


finally:

    conn.close()