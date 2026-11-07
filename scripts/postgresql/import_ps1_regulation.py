# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os

from pathlib import Path
from getpass import getpass
import re

import numpy as np
import pandas as pd
import psycopg


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())

PS1_DATASET_ID = 2
TP1_DATASET_ID = 1

PS1_ANALYTE_START = 7171
EXPECTED_PS1_ROWS = 39814


# =========================================================
# Helper: safely parse model-count columns
# =========================================================

def parse_count_column(series, column_name):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    )

    # Something existed in the raw sheet but was not numeric
    bad_mask = (
        series.notna()
        & numeric.isna()
    )

    if bad_mask.any():

        examples = (
            series[bad_mask]
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"{column_name}: non-numeric values found: "
            f"{examples}"
        )

    numeric = numeric.fillna(0)

    # Must be integer-like
    if not np.allclose(
        numeric.to_numpy(),
        np.round(numeric.to_numpy())
    ):
        raise ValueError(
            f"{column_name}: non-integer values found."
        )

    numeric = numeric.astype(int)

    # There are five IR models:
    # CI, DEX, TNF, MPQ, AA
    if ((numeric < 0) | (numeric > 5)).any():

        raise ValueError(
            f"{column_name}: values outside 0–5 found."
        )

    return numeric


# =========================================================
# Read PS1 raw data
# =========================================================

print()
print("=" * 65)
print("Reading PS1 regulation annotations")
print("=" * 65)


analysis = pd.read_excel(
    PS1_FILE,
    sheet_name="analysis"
)


quant_meta = pd.read_excel(
    PS1_FILE,
    sheet_name="quantification",
    usecols=[
        "Phosphopeptide",
        "Gene",
        "Uniprot",
        "Site"
    ]
)


required_analysis_columns = [
    "Phosphopeptide",
    "Number of defective models",
    "Number of emergent models"
]


missing_columns = [
    col
    for col in required_analysis_columns
    if col not in analysis.columns
]


if missing_columns:

    print()
    print("Available analysis columns:")
    for col in analysis.columns:
        print(" -", col)

    raise ValueError(
        "Missing required analysis columns: "
        f"{missing_columns}"
    )


# =========================================================
# Basic row checks
# =========================================================

if len(analysis) != EXPECTED_PS1_ROWS:

    raise ValueError(
        f"Expected {EXPECTED_PS1_ROWS} analysis rows, "
        f"found {len(analysis)}."
    )


if len(quant_meta) != EXPECTED_PS1_ROWS:

    raise ValueError(
        f"Expected {EXPECTED_PS1_ROWS} quantification rows, "
        f"found {len(quant_meta)}."
    )


# =========================================================
# Ensure analysis order matches quantification order
# =========================================================

analysis_ids = (
    analysis["Phosphopeptide"]
    .astype(str)
    .str.strip()
    .reset_index(drop=True)
)


quant_ids = (
    quant_meta["Phosphopeptide"]
    .astype(str)
    .str.strip()
    .reset_index(drop=True)
)


if not analysis_ids.equals(quant_ids):

    mismatch = np.flatnonzero(
        (analysis_ids != quant_ids).to_numpy()
    )

    first = int(mismatch[0])

    raise ValueError(
        "PS1 analysis and quantification row order "
        f"do not match at row {first + 2}."
    )


print(
    "Analysis ↔ quantification row alignment: OK"
)


# =========================================================
# Parse defective / emergent counts
# =========================================================

defective_count = parse_count_column(
    analysis["Number of defective models"],
    "Number of defective models"
)


emergent_count = parse_count_column(
    analysis["Number of emergent models"],
    "Number of emergent models"
)


# Under the biological definitions, a phosphopeptide should
# not simultaneously belong to defective and emergent classes.
both_mask = (
    (defective_count > 0)
    & (emergent_count > 0)
)


if both_mask.any():

    bad_rows = quant_meta.loc[
        both_mask,
        ["Phosphopeptide", "Uniprot", "Site"]
    ]

    print()
    print(
        "Rows simultaneously defective and emergent:"
    )

    print(
        bad_rows.head(20).to_string(index=False)
    )

    raise ValueError(
        "Found phosphopeptides classified as both "
        "defective and emergent. Import stopped."
    )


# For this helper table:
#
# defective count > 0 -> "defective"
# emergent count  > 0 -> "emergent"
# otherwise            -> NULL
#
# We deliberately do NOT invent another biological category.

regulation_status = []

for d, e in zip(
    defective_count,
    emergent_count
):

    if d > 0:
        regulation_status.append(
            "defective"
        )

    elif e > 0:
        regulation_status.append(
            "emergent"
        )

    else:
        regulation_status.append(
            None
        )


print()
print(
    "Defective phosphopeptides:",
    int((defective_count > 0).sum())
)

print(
    "Emergent phosphopeptides:",
    int((emergent_count > 0).sum())
)

print(
    "Neither defective nor emergent:",
    int(
        (
            (defective_count == 0)
            & (emergent_count == 0)
        ).sum()
    )
)


# =========================================================
# Connect PostgreSQL
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
        # Create benchmark auxiliary table
        # =================================================

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            "PhosphopeptideRegulation" (

                analyte BIGINT PRIMARY KEY,

                phosphopeptide_id TEXT
                    NOT NULL
                    UNIQUE,

                gene_symbol TEXT,

                uniprot_id VARCHAR(11)
                    NOT NULL,

                site VARCHAR(32)
                    NOT NULL,

                insulin_regulation_status VARCHAR(20),

                defective_model_count INTEGER
                    NOT NULL,

                emergent_model_count INTEGER
                    NOT NULL,

                linked_protein_analyte_id BIGINT,

                CONSTRAINT
                    fk_phosphopeptideregulation_analyte
                FOREIGN KEY (analyte)
                REFERENCES "Analyte"(id),

                CONSTRAINT
                    fk_phosphopeptideregulation_linkedprotein
                FOREIGN KEY (linked_protein_analyte_id)
                REFERENCES "Analyte"(id),

                CONSTRAINT
                    ck_phosphopeptideregulation_status
                CHECK (
                    insulin_regulation_status
                    IN ('defective', 'emergent')
                    OR
                    insulin_regulation_status IS NULL
                ),

                CONSTRAINT
                    ck_phosphopeptideregulation_defectivecount
                CHECK (
                    defective_model_count
                    BETWEEN 0 AND 5
                ),

                CONSTRAINT
                    ck_phosphopeptideregulation_emergentcount
                CHECK (
                    emergent_model_count
                    BETWEEN 0 AND 5
                ),

                CONSTRAINT
                    ck_phosphopeptideregulation_notboth
                CHECK (
                    NOT (
                        defective_model_count > 0
                        AND
                        emergent_model_count > 0
                    )
                )
            );
            '''
        )


        # =================================================
        # Prevent duplicate imports
        # =================================================

        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "PhosphopeptideRegulation";
            '''
        )

        existing = cur.fetchone()[0]

        print()
        print(
            "Existing PhosphopeptideRegulation rows:",
            existing
        )

        if existing != 0:

            raise RuntimeError(
                "PhosphopeptideRegulation is not empty. "
                "Import stopped to prevent duplicates."
            )


        # =================================================
        # Read PS1 biological mappings already in DB
        # =================================================

        cur.execute(
            '''
            SELECT
                a.id,
                dep.accession_id,
                dep.amino_acid,
                dep.residue

            FROM "Analyte" a

            JOIN "DescriptorEntryPhosphosite" dep
                ON dep.analyte = a.id

            WHERE a.dataset = %s

            ORDER BY a.id;
            ''',
            (PS1_DATASET_ID,)
        )

        ps1_db_rows = cur.fetchall()


        if len(ps1_db_rows) != EXPECTED_PS1_ROWS:

            raise RuntimeError(
                "Expected "
                f"{EXPECTED_PS1_ROWS} PS1 analyte mappings, "
                f"found {len(ps1_db_rows)}."
            )


        # =================================================
        # Get TP1 UniProt -> protein Analyte mapping
        # =================================================

        cur.execute(
            '''
            SELECT
                deu.accession_id,
                deu.analyte

            FROM "DescriptorEntryUniProt" deu

            JOIN "Analyte" a
                ON a.id = deu.analyte

            WHERE a.dataset = %s

            ORDER BY deu.analyte;
            ''',
            (TP1_DATASET_ID,)
        )

        tp1_rows = cur.fetchall()


        tp1_map = {}

        for accession, analyte_id in tp1_rows:

            if accession in tp1_map:

                raise RuntimeError(
                    "TP1 contains more than one "
                    f"protein analyte for UniProt {accession}."
                )

            tp1_map[accession] = analyte_id


        print(
            "TP1 UniProt → protein mappings:",
            len(tp1_map)
        )


        # =================================================
        # Build helper rows
        # =================================================

        insert_rows = []

        linked_count = 0
        unlinked_count = 0


        for i in range(EXPECTED_PS1_ROWS):

            expected_analyte_id = (
                PS1_ANALYTE_START + i
            )

            (
                db_analyte_id,
                db_accession,
                db_amino_acid,
                db_residue
            ) = ps1_db_rows[i]


            # ---------------------------------------------
            # Validate relational Analyte ID sequence
            # ---------------------------------------------

            if db_analyte_id != expected_analyte_id:

                raise RuntimeError(
                    f"PS1 analyte ID mismatch at row {i}: "
                    f"expected {expected_analyte_id}, "
                    f"found {db_analyte_id}."
                )


            raw_phosphopeptide = str(
                quant_meta.iloc[i]["Phosphopeptide"]
            ).strip()


            raw_uniprot = str(
                quant_meta.iloc[i]["Uniprot"]
            ).strip()


            raw_site = str(
                quant_meta.iloc[i]["Site"]
            ).strip()


            raw_gene_value = (
                quant_meta.iloc[i]["Gene"]
            )


            if pd.isna(raw_gene_value):

                raw_gene = None

            else:

                raw_gene = str(
                    raw_gene_value
                ).strip()

                if raw_gene == "":
                    raw_gene = None


            # ---------------------------------------------
            # Validate UniProt mapping
            # ---------------------------------------------

            if raw_uniprot != db_accession:

                raise RuntimeError(
                    f"UniProt mismatch for analyte "
                    f"{db_analyte_id}: "
                    f"raw={raw_uniprot}, "
                    f"database={db_accession}."
                )


            # ---------------------------------------------
            # Validate phosphosite mapping
            # ---------------------------------------------

            site_match = re.fullmatch(
                r"([STY])(\d+)",
                raw_site
            )


            if site_match is None:

                raise ValueError(
                    f"Cannot parse Site '{raw_site}' "
                    f"for {raw_phosphopeptide}."
                )


            raw_amino_acid = (
                site_match.group(1)
            )

            raw_residue = int(
                site_match.group(2)
            )


            if (
                raw_amino_acid
                != db_amino_acid
                or
                raw_residue
                != int(db_residue)
            ):

                raise RuntimeError(
                    "Phosphosite mismatch for "
                    f"analyte {db_analyte_id}: "
                    f"raw={raw_site}, "
                    f"database="
                    f"{db_amino_acid}{db_residue}."
                )


            # ---------------------------------------------
            # Cross-omics TP1 protein link
            # ---------------------------------------------

            linked_protein_id = (
                tp1_map.get(
                    raw_uniprot
                )
            )


            if linked_protein_id is None:

                unlinked_count += 1

            else:

                linked_count += 1


            insert_rows.append(
                (
                    int(db_analyte_id),

                    raw_phosphopeptide,

                    raw_gene,

                    raw_uniprot,

                    raw_site,

                    regulation_status[i],

                    int(
                        defective_count.iloc[i]
                    ),

                    int(
                        emergent_count.iloc[i]
                    ),

                    (
                        int(linked_protein_id)
                        if linked_protein_id
                        is not None
                        else None
                    )
                )
            )


        print()
        print(
            "Prepared rows:",
            len(insert_rows)
        )

        print(
            "Linked to TP1 protein:",
            linked_count
        )

        print(
            "No TP1 protein match:",
            unlinked_count
        )


        if len(insert_rows) != EXPECTED_PS1_ROWS:

            raise RuntimeError(
                "Prepared row count mismatch."
            )


        # =================================================
        # Confirmation
        # =================================================

        print()
        print("=" * 65)
        print("PRE-IMPORT CHECK PASSED")
        print("=" * 65)

        answer = input(
            "\nType IMPORT to insert "
            "PhosphopeptideRegulation: "
        )


        if answer != "IMPORT":

            print("Import cancelled.")

            conn.rollback()

            raise SystemExit


        # =================================================
        # COPY auxiliary table
        # =================================================

        print()
        print(
            "COPYing PhosphopeptideRegulation "
            f"({len(insert_rows)} rows)..."
        )


        with cur.copy(
            '''
            COPY "PhosphopeptideRegulation" (
                analyte,
                phosphopeptide_id,
                gene_symbol,
                uniprot_id,
                site,
                insulin_regulation_status,
                defective_model_count,
                emergent_model_count,
                linked_protein_analyte_id
            )
            FROM STDIN
            '''
        ) as copy:

            for row in insert_rows:

                copy.write_row(row)


        # =================================================
        # Final audit BEFORE commit
        # =================================================

        cur.execute(
            '''
            SELECT
                COUNT(*) AS total,

                COUNT(*) FILTER (
                    WHERE
                    insulin_regulation_status
                    = 'defective'
                ) AS defective,

                COUNT(*) FILTER (
                    WHERE
                    insulin_regulation_status
                    = 'emergent'
                ) AS emergent,

                COUNT(*) FILTER (
                    WHERE
                    linked_protein_analyte_id
                    IS NOT NULL
                ) AS linked_to_tp1

            FROM "PhosphopeptideRegulation";
            '''
        )

        (
            total,
            defective,
            emergent,
            linked_to_tp1
        ) = cur.fetchone()


        print()
        print("=" * 65)
        print("FINAL DATABASE CHECK")
        print("=" * 65)

        print(
            "Total:",
            total
        )

        print(
            "Defective:",
            defective
        )

        print(
            "Emergent:",
            emergent
        )

        print(
            "Linked to TP1 protein:",
            linked_to_tp1
        )


        if total != EXPECTED_PS1_ROWS:

            raise RuntimeError(
                "Final table row count mismatch."
            )


        # ---------------------------------------------
        # Broken FK / dataset check
        # ---------------------------------------------

        cur.execute(
            '''
            SELECT COUNT(*)

            FROM "PhosphopeptideRegulation" pr

            LEFT JOIN "Analyte" ps
                ON ps.id = pr.analyte

            LEFT JOIN "Analyte" tp
                ON tp.id =
                   pr.linked_protein_analyte_id

            WHERE
                ps.id IS NULL

                OR ps.dataset <> 2

                OR (
                    pr.linked_protein_analyte_id
                    IS NOT NULL
                    AND (
                        tp.id IS NULL
                        OR tp.dataset <> 1
                    )
                );
            '''
        )

        broken_links = cur.fetchone()[0]


        print(
            "Broken regulation links:",
            broken_links
        )


        if broken_links != 0:

            raise RuntimeError(
                "Broken auxiliary-table links found."
            )


    # =====================================================
    # Commit
    # =====================================================

    conn.commit()

    print()
    print("=" * 65)
    print(
        "PS1 regulation import "
        "completed successfully."
    )
    print("=" * 65)


except BaseException:

    conn.rollback()

    print()
    print("=" * 65)
    print(
        "IMPORT STOPPED — "
        "transaction rolled back."
    )
    print(
        "No partial regulation data "
        "was committed."
    )
    print("=" * 65)

    raise


finally:

    conn.close()