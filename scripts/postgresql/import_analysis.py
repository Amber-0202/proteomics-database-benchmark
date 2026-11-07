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

TP1_FILE = str(Path(os.environ.get("TP1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - TP1.xlsx")).expanduser())
PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

TP1_ANALYTE_START = 1
PS1_ANALYTE_START = 7171

EXPECTED_TP1_ROWS = 7170
EXPECTED_PS1_ROWS = 39814

EXPECTED_DETEST = 19
EXPECTED_CONTRAST_GROUP = 34
EXPECTED_DERESULT = 160973
EXPECTED_PVALUE = 282452


# =========================================================
# Test definitions
# =========================================================

TESTS = [

    # =====================================================
    # TP1
    # =====================================================

    {
        "id": 1,
        "dataset": "TP1",
        "name": "TP1 Model ANOVA",
        "type": "F",
        "stat": "Model ANOVA Fval",
        "logfc": None,
        "raw_p": "Model ANOVA p",
        "adj_p": "Model ANOVA adj p",
    },

    {
        "id": 2,
        "dataset": "TP1",
        "name": "TP1 CI vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": "CI/CTRL FC",
        "raw_p": "CI/CTRL p",
        "adj_p": "CI/CTRL adj p",
    },

    {
        "id": 3,
        "dataset": "TP1",
        "name": "TP1 DEX vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": "DEX/CTRL FC",
        "raw_p": "DEX/CTRL p",
        "adj_p": "DEX/CTRL adj p",
    },

    {
        "id": 4,
        "dataset": "TP1",
        "name": "TP1 TNF vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": "TNF/CTRL FC",
        "raw_p": "TNF/CTRL p",
        "adj_p": "TNF/CTRL adj p",
    },

    {
        "id": 5,
        "dataset": "TP1",
        "name": "TP1 MPQ vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": "MPQ/CTRL FC",
        "raw_p": "MPQ/CTRL p",
        "adj_p": "MPQ/CTRL adj p",
    },

    {
        "id": 6,
        "dataset": "TP1",
        "name": "TP1 AA vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": "AA/CTRL FC",
        "raw_p": "AA/CTRL p",
        "adj_p": "AA/CTRL adj p",
    },

    {
        "id": 7,
        "dataset": "TP1",
        "name": "TP1 CTRL INS vs BAS",
        "type": "T",
        "stat": "CTRL INS/BAS t",
        "logfc": None,
        "raw_p": "CTRL INS/BAS p",
        "adj_p": "CTRL INS/BAS adj p",
    },

    {
        "id": 8,
        "dataset": "TP1",
        "name": "TP1 CI INS vs BAS",
        "type": "T",
        "stat": "CI INS/BAS t",
        "logfc": None,
        "raw_p": "CI INS/BAS p",
        "adj_p": "CI INS/BAS adj p",
    },

    {
        "id": 9,
        "dataset": "TP1",
        "name": "TP1 DEX INS vs BAS",
        "type": "T",
        "stat": "DEX INS/BAS t",
        "logfc": None,
        "raw_p": "DEX INS/BAS p",
        "adj_p": "DEX INS/BAS adj p",
    },

    {
        "id": 10,
        "dataset": "TP1",
        "name": "TP1 TNF INS vs BAS",
        "type": "T",
        "stat": "TNF INS/BAS t",
        "logfc": None,
        "raw_p": "TNF INS/BAS p",
        "adj_p": "TNF INS/BAS adj p",
    },

    {
        "id": 11,
        "dataset": "TP1",
        "name": "TP1 MPQ INS vs BAS",
        "type": "T",
        "stat": "MPQ INS/BAS t",
        "logfc": None,
        "raw_p": "MPQ INS/BAS p",
        "adj_p": "MPQ INS/BAS adj p",
    },

    {
        "id": 12,
        "dataset": "TP1",
        "name": "TP1 AA INS vs BAS",
        "type": "T",
        "stat": "AA INS/BAS t",
        "logfc": None,
        "raw_p": "AA INS/BAS p",
        "adj_p": "AA INS/BAS adj p",
    },

    # =====================================================
    # PS1
    # =====================================================

    {
        "id": 13,
        "dataset": "PS1",
        "name": "PS1 CTRL INS vs BAS",
        "type": "T",
        "stat": "CTRL INS/BAS t",
        "logfc": "CTRL INS/BAS log2FC",
        "raw_p": "CTRL INS/BAS p",
        "adj_p": "CTRL INS/BAS adj p",
    },

    {
        "id": 14,
        "dataset": "PS1",
        "name": "PS1 Insulin Response ANOVA",
        "type": "F",
        "stat": "Response anova F",
        "logfc": None,
        "raw_p": "Response anova p",
        "adj_p": "Response anova adj p",
    },

    {
        "id": 15,
        "dataset": "PS1",
        "name": "PS1 CI Response vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": None,
        "raw_p": "CI/CTRL response p",
        "adj_p": "CI/CTRL response adj p",
    },

    {
        "id": 16,
        "dataset": "PS1",
        "name": "PS1 DEX Response vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": None,
        "raw_p": "DEX/CTRL response p",
        "adj_p": "DEX/CTRL response adj p",
    },

    {
        "id": 17,
        "dataset": "PS1",
        "name": "PS1 TNF Response vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": None,
        "raw_p": "TNF/CTRL response p",
        "adj_p": "TNF/CTRL response adj p",
    },

    {
        "id": 18,
        "dataset": "PS1",
        "name": "PS1 MPQ Response vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": None,
        "raw_p": "MPQ/CTRL response p",
        "adj_p": "MPQ/CTRL response adj p",
    },

    {
        "id": 19,
        "dataset": "PS1",
        "name": "PS1 AA Response vs CTRL (Dunnett)",
        "type": "D",
        "stat": None,
        "logfc": None,
        "raw_p": "AA/CTRL response p",
        "adj_p": "AA/CTRL response adj p",
    },
]


# =========================================================
# Read workbook
# =========================================================

def read_analysis(
    path,
    identifier,
    required_columns,
    expected_rows
):

    print()
    print("=" * 65)
    print("Reading:", path.name)
    print("=" * 65)

    with pd.ExcelFile(path) as xls:

        analysis = pd.read_excel(
            xls,
            sheet_name="analysis",
            usecols=[
                identifier,
                *required_columns
            ]
        )

        quant_keys = pd.read_excel(
            xls,
            sheet_name="quantification",
            usecols=[identifier]
        )

    if len(analysis) != expected_rows:
        raise ValueError(
            f"{path.name}: expected {expected_rows} "
            f"analysis rows, found {len(analysis)}."
        )

    if len(quant_keys) != expected_rows:
        raise ValueError(
            f"{path.name}: quantification row count mismatch."
        )

    # The Analyte IDs were created from quantification row order.
    # Therefore analysis order MUST match quantification order.
    a = analysis[identifier].astype(str).reset_index(drop=True)
    q = quant_keys[identifier].astype(str).reset_index(drop=True)

    if not a.equals(q):
        mismatch = np.flatnonzero(
            (a != q).to_numpy()
        )

        first = int(mismatch[0])

        raise ValueError(
            f"{path.name}: analysis and quantification "
            f"row order differs at row {first + 2}."
        )

    # Convert all statistical columns to numeric
    for col in required_columns:

        analysis[col] = pd.to_numeric(
            analysis[col],
            errors="raise"
        )

    print("Rows:", len(analysis))
    print("Analysis ↔ quantification row alignment: OK")

    return analysis


# =========================================================
# Helpers
# =========================================================

def value_or_none(value):

    if pd.isna(value):
        return None

    value = float(value)

    if not np.isfinite(value):
        raise ValueError(
            f"Non-finite statistical value found: {value}"
        )

    return value


def validate_pvalue(value):

    if value is None:
        return

    # tiny floating point overshoot is tolerated
    if value < -1e-12 or value > 1.000000000001:
        raise ValueError(
            f"Invalid p-value found: {value}"
        )


# =========================================================
# Determine required raw columns
# =========================================================

tp1_columns = set()
ps1_columns = set()

for test in TESTS:

    destination = (
        tp1_columns
        if test["dataset"] == "TP1"
        else ps1_columns
    )

    for key in [
        "stat",
        "logfc",
        "raw_p",
        "adj_p"
    ]:

        col = test[key]

        if col is not None:
            destination.add(col)


# =========================================================
# Read + validate raw analysis sheets
# =========================================================

tp1 = read_analysis(
    path=TP1_FILE,
    identifier="Gene_Uniprot",
    required_columns=sorted(tp1_columns),
    expected_rows=EXPECTED_TP1_ROWS
)

ps1 = read_analysis(
    path=PS1_FILE,
    identifier="Phosphopeptide",
    required_columns=sorted(ps1_columns),
    expected_rows=EXPECTED_PS1_ROWS
)


# =========================================================
# Prepare statistical results
# =========================================================

deresult_rows = []
pvalue_rows = []

next_result_id = 1

print()
print("=" * 65)
print("PREPARING ANALYSIS RESULTS")
print("=" * 65)

for test in TESTS:

    if test["dataset"] == "TP1":

        df = tp1
        analyte_start = TP1_ANALYTE_START

    else:

        df = ps1
        analyte_start = PS1_ANALYTE_START

    relevant_columns = [
        col
        for col in [
            test["stat"],
            test["logfc"],
            test["raw_p"],
            test["adj_p"]
        ]
        if col is not None
    ]

    mask = (
        df[relevant_columns]
        .notna()
        .any(axis=1)
    )

    row_indexes = np.flatnonzero(
        mask.to_numpy()
    )

    test_result_count = 0
    test_pvalue_count = 0

    for row_index in row_indexes:

        row = df.iloc[row_index]

        analyte_id = (
            analyte_start
            + int(row_index)
        )

        stat_value = (
            value_or_none(
                row[test["stat"]]
            )
            if test["stat"] is not None
            else None
        )

        logfc_value = (
            value_or_none(
                row[test["logfc"]]
            )
            if test["logfc"] is not None
            else None
        )

        raw_p = (
            value_or_none(
                row[test["raw_p"]]
            )
            if test["raw_p"] is not None
            else None
        )

        adj_p = (
            value_or_none(
                row[test["adj_p"]]
            )
            if test["adj_p"] is not None
            else None
        )

        validate_pvalue(raw_p)
        validate_pvalue(adj_p)

        result_id = next_result_id

        deresult_rows.append(
            (
                result_id,
                test["id"],
                analyte_id,
                stat_value,
                logfc_value
            )
        )

        if raw_p is not None:

            pvalue_rows.append(
                (
                    "RA",
                    raw_p,
                    result_id
                )
            )

            test_pvalue_count += 1

        if adj_p is not None:

            pvalue_rows.append(
                (
                    "AD",
                    adj_p,
                    result_id
                )
            )

            test_pvalue_count += 1

        next_result_id += 1
        test_result_count += 1

    print(
        f'{test["id"]:>2} '
        f'{test["name"]:<42} '
        f'REsults={test_result_count:<6} '
        f'PValues={test_pvalue_count}'
    )


print()
print("Prepared DEResult:", len(deresult_rows))
print("Prepared PValue:", len(pvalue_rows))


if len(deresult_rows) != EXPECTED_DERESULT:

    raise RuntimeError(
        "DEResult expected "
        f"{EXPECTED_DERESULT}, "
        f"prepared {len(deresult_rows)}."
    )


if len(pvalue_rows) != EXPECTED_PVALUE:

    raise RuntimeError(
        "PValue expected "
        f"{EXPECTED_PVALUE}, "
        f"prepared {len(pvalue_rows)}."
    )


# =========================================================
# Database connection
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

        # =================================================
        # Safety checks
        # =================================================

        tables = [
            "DETest",
            "ContrastGroup",
            "DEResult",
            "PValue"
        ]

        for table in tables:

            cur.execute(
                f'SELECT COUNT(*) FROM "{table}";'
            )

            count = cur.fetchone()[0]

            print(
                f"Existing {table}:",
                count
            )

            if count != 0:

                raise RuntimeError(
                    f'{table} is not empty. '
                    'Import stopped to prevent duplicates.'
                )

        # =================================================
        # Get SampleGroup IDs by name
        # =================================================

        cur.execute(
            '''
            SELECT id, name
            FROM "SampleGroup";
            '''
        )

        sample_group_map = {
            name: group_id
            for group_id, name in cur.fetchall()
        }


        required_groups = {

            "CTRL_BASAL",
            "CTRL_INS",

            "CI_BASAL",
            "CI_INS",

            "DEX_BASAL",
            "DEX_INS",

            "TNF_BASAL",
            "TNF_INS",

            "MPQ_BASAL",
            "MPQ_INS",

            "AA_BASAL",
            "AA_INS",
        }


        missing_groups = (
            required_groups
            - set(sample_group_map)
        )

        if missing_groups:

            raise RuntimeError(
                "Missing SampleGroups: "
                f"{sorted(missing_groups)}"
            )


        # =================================================
        # Build DETest
        # =================================================

        detest_rows = [
            (
                test["id"],
                None,               # root_node placeholder
                test["name"],
                test["type"]
            )
            for test in TESTS
        ]


        # =================================================
        # Build ContrastGroup
        # =================================================

        contrast_rows = []

        next_contrast_id = 1


        def add_contrast(
            test_id,
            group_name,
            multiplier
        ):

            global next_contrast_id

            contrast_rows.append(
                (
                    next_contrast_id,
                    test_id,
                    sample_group_map[group_name],
                    multiplier
                )
            )

            next_contrast_id += 1


        # -------------------------------------------------
        # TP1: six clear INS - BAS t-test contrasts
        # -------------------------------------------------

        tp1_t_tests = {
            7: "CTRL",
            8: "CI",
            9: "DEX",
            10: "TNF",
            11: "MPQ",
            12: "AA",
        }


        for test_id, model in tp1_t_tests.items():

            add_contrast(
                test_id,
                f"{model}_BASAL",
                -1.0
            )

            add_contrast(
                test_id,
                f"{model}_INS",
                1.0
            )


        # -------------------------------------------------
        # PS1 CTRL INS - BAS
        # -------------------------------------------------

        add_contrast(
            13,
            "CTRL_BASAL",
            -1.0
        )

        add_contrast(
            13,
            "CTRL_INS",
            1.0
        )


        # -------------------------------------------------
        # PS1 Dunnett insulin-response contrasts
        #
        # (Model_INS - Model_BAS)
        # -
        # (CTRL_INS - CTRL_BAS)
        #
        # = Model_INS
        # - Model_BAS
        # - CTRL_INS
        # + CTRL_BAS
        # -------------------------------------------------

        ps1_response_tests = {
            15: "CI",
            16: "DEX",
            17: "TNF",
            18: "MPQ",
            19: "AA",
        }


        for test_id, model in ps1_response_tests.items():

            add_contrast(
                test_id,
                "CTRL_BASAL",
                1.0
            )

            add_contrast(
                test_id,
                "CTRL_INS",
                -1.0
            )

            add_contrast(
                test_id,
                f"{model}_BASAL",
                -1.0
            )

            add_contrast(
                test_id,
                f"{model}_INS",
                1.0
            )


        if len(contrast_rows) != EXPECTED_CONTRAST_GROUP:

            raise RuntimeError(
                "Expected "
                f"{EXPECTED_CONTRAST_GROUP} "
                "ContrastGroup rows, got "
                f"{len(contrast_rows)}."
            )


        # =================================================
        # Confirmation
        # =================================================

        print()
        print("=" * 65)
        print("PRE-IMPORT CHECK PASSED")
        print("=" * 65)

        print("DETest:", len(detest_rows))
        print("ContrastGroup:", len(contrast_rows))
        print("DEResult:", len(deresult_rows))
        print("PValue:", len(pvalue_rows))

        print()
        print(
            "PValue codes: "
            "RA = raw p-value, "
            "AD = adjusted p-value"
        )

        answer = input(
            "\nType IMPORT to insert analysis layer: "
        )

        if answer != "IMPORT":

            print("Import cancelled.")

            conn.rollback()

            raise SystemExit


        # =================================================
        # 1. DETest
        # =================================================

        print()
        print("Inserting DETest...")

        cur.executemany(
            '''
            INSERT INTO "DETest" (
                id,
                root_node,
                name,
                type
            )
            VALUES (%s, %s, %s, %s);
            ''',
            detest_rows
        )


        # =================================================
        # 2. ContrastGroup
        # =================================================

        print("Inserting ContrastGroup...")

        cur.executemany(
            '''
            INSERT INTO "ContrastGroup" (
                id,
                de_test,
                sample_group,
                multiplier
            )
            VALUES (%s, %s, %s, %s);
            ''',
            contrast_rows
        )


        # =================================================
        # 3. DEResult via COPY
        # =================================================

        print(
            "COPYing DEResult "
            f"({len(deresult_rows)} rows)..."
        )

        with cur.copy(
            '''
            COPY "DEResult" (
                id,
                contrast,
                analyte,
                test_statistic,
                logfc
            )
            FROM STDIN
            '''
        ) as copy:

            for row in deresult_rows:
                copy.write_row(row)


        # =================================================
        # 4. PValue via COPY
        # =================================================

        print(
            "COPYing PValue "
            f"({len(pvalue_rows)} rows)..."
        )

        with cur.copy(
            '''
            COPY "PValue" (
                adjustment_method,
                value,
                de_result
            )
            FROM STDIN
            '''
        ) as copy:

            for row in pvalue_rows:
                copy.write_row(row)


        # =================================================
        # Final checks BEFORE commit
        # =================================================

        actual_counts = {}

        for table in tables:

            cur.execute(
                f'SELECT COUNT(*) FROM "{table}";'
            )

            actual_counts[table] = (
                cur.fetchone()[0]
            )


        print()
        print("=" * 65)
        print("FINAL ANALYSIS DATABASE CHECK")
        print("=" * 65)

        for table, count in actual_counts.items():

            print(
                f"{table}: {count}"
            )


        if (
            actual_counts["DETest"]
            != EXPECTED_DETEST
        ):
            raise RuntimeError(
                "DETest count mismatch."
            )


        if (
            actual_counts["ContrastGroup"]
            != EXPECTED_CONTRAST_GROUP
        ):
            raise RuntimeError(
                "ContrastGroup count mismatch."
            )


        if (
            actual_counts["DEResult"]
            != EXPECTED_DERESULT
        ):
            raise RuntimeError(
                "DEResult count mismatch."
            )


        if (
            actual_counts["PValue"]
            != EXPECTED_PVALUE
        ):
            raise RuntimeError(
                "PValuße count mismatch."
            )


    # =====================================================
    # Commit only when all checks pass
    # =====================================================

    conn.commit()

    print()
    print("=" * 65)
    print(
        "Analysis layer import completed successfully."
    )
    print("=" * 65)


except BaseException:

    conn.rollback()

    print()
    print("=" * 65)
    print(
        "ANALYSIS IMPORT STOPPED — "
        "transaction rolled back."
    )
    print(
        "No partial analysis data was committed."
    )
    print("=" * 65)

    raise


finally:

    conn.close()