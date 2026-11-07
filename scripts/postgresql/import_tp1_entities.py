# Repository preparation: configurable input paths and connection settings.
# Data transformations and interactive write confirmations are retained.
import os

from pathlib import Path
from getpass import getpass

import pandas as pd
import psycopg


# =========================
# Configuration
# =========================

DATASET_ID = 1
ORGANISM_ID = 10090
UP_DESCRIPTOR_ID = 1

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TP1_FILE = str(Path(os.environ.get("TP1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - TP1.xlsx")).expanduser())


# =========================
# Read raw TP1
# =========================

print("Reading TP1...")

df = pd.read_excel(
    TP1_FILE,
    sheet_name="quantification",
    usecols=["Gene_Uniprot", "Gene", "Uniprot"]
)

print("Rows:", len(df))
print("Unique UniProt IDs:", df["Uniprot"].nunique())
print("Missing Gene values:", df["Gene"].isna().sum())


# Basic safety checks
if len(df) != 7170:
    raise ValueError(
        f"Expected 7170 TP1 rows, but found {len(df)}"
    )

if df["Uniprot"].isna().any():
    raise ValueError("TP1 contains missing UniProt IDs.")

if df["Uniprot"].astype(str).str.len().max() > 11:
    raise ValueError("Found UniProt accession longer than VARCHAR(11).")


# =========================
# Build records
# =========================

analyte_rows = []
descriptor_entry_rows = []
uniprot_entry_rows = []
uniprot_gene_rows = []

for i, row in df.iterrows():

    analyte_id = i + 1
    descriptor_entry_id = i + 1

    accession = str(row["Uniprot"]).strip()

    gene = None
    if pd.notna(row["Gene"]):
        gene = str(row["Gene"]).strip()
        if gene == "":
            gene = None

    # Analyte: one row per protein
    analyte_rows.append(
        (
            analyte_id,
            DATASET_ID
        )
    )

    # Uploaded UniProt value for this analyte
    descriptor_entry_rows.append(
        (
            descriptor_entry_id,
            UP_DESCRIPTOR_ID,
            analyte_id,
            accession,
            1,      # variant
            1       # entry_position
        )
    )

    # Minimal UniProt reference row
    uniprot_entry_rows.append(
        (
            accession,
            None,           # full protein name not present in raw TP1
            ORGANISM_ID,
            None            # human_entry unknown
        )
    )

    # Gene annotation if available
    if gene is not None:
        uniprot_gene_rows.append(
            (
                accession,
                gene,
                None        # gene-name type not defined in supplied raw data
            )
        )


print()
print("Prepared:")
print("Analyte:", len(analyte_rows))
print("AnalyteDescriptor: 1")
print("DescriptorEntryUniProt:", len(descriptor_entry_rows))
print("UniProtEntry:", len(uniprot_entry_rows))
print("UniProtGene:", len(uniprot_gene_rows))


# =========================
# Database connection
# =========================

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

        # ---------------------------------
        # Safety check: don't import twice
        # ---------------------------------

        cur.execute(
            'SELECT COUNT(*) FROM "Analyte" WHERE dataset = %s;',
            (DATASET_ID,)
        )

        existing_analytes = cur.fetchone()[0]

        cur.execute(
            'SELECT COUNT(*) FROM "AnalyteDescriptor" WHERE dataset = %s;',
            (DATASET_ID,)
        )

        existing_descriptors = cur.fetchone()[0]

        print()
        print("Existing TP1 analytes:", existing_analytes)
        print("Existing TP1 descriptors:", existing_descriptors)

        if existing_analytes != 0 or existing_descriptors != 0:
            raise RuntimeError(
                "TP1 biological entities already exist. "
                "Import stopped to prevent duplicates."
            )

        # ---------------------------------
        # Confirmation
        # ---------------------------------

        answer = input(
            "\nType IMPORT to insert TP1 biological entities: "
        )

        if answer != "IMPORT":
            print("Import cancelled.")
            conn.rollback()
            raise SystemExit

        # ---------------------------------
        # 1. Analyte
        # ---------------------------------

        print("\nInserting Analyte...")

        cur.executemany(
            '''
            INSERT INTO "Analyte" (
                id,
                dataset
            )
            VALUES (%s, %s);
            ''',
            analyte_rows
        )

        # ---------------------------------
        # 2. AnalyteDescriptor
        # ---------------------------------

        print("Inserting AnalyteDescriptor...")

        cur.execute(
            '''
            INSERT INTO "AnalyteDescriptor" (
                id,
                dataset,
                entry_relationship,
                type
            )
            VALUES (%s, %s, %s, %s);
            ''',
            (
                UP_DESCRIPTOR_ID,
                DATASET_ID,
                "AND",
                "UP"
            )
        )

        # ---------------------------------
        # 3. DescriptorEntryUniProt
        # ---------------------------------

        print("Inserting DescriptorEntryUniProt...")

        cur.executemany(
            '''
            INSERT INTO "DescriptorEntryUniProt" (
                id,
                descriptor,
                analyte,
                accession_id,
                variant,
                entry_position
            )
            VALUES (%s, %s, %s, %s, %s, %s);
            ''',
            descriptor_entry_rows
        )

        # ---------------------------------
        # 4. UniProtEntry
        # ---------------------------------

        print("Inserting UniProtEntry...")

        cur.executemany(
            '''
            INSERT INTO "UniProtEntry" (
                accession_id,
                name,
                organism,
                human_entry
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (accession_id) DO NOTHING;
            ''',
            uniprot_entry_rows
        )

        # ---------------------------------
        # 5. UniProtGene
        # ---------------------------------

        print("Inserting UniProtGene...")

        cur.executemany(
            '''
            INSERT INTO "UniProtGene" (
                uniprot_entry,
                gene_name,
                type
            )
            VALUES (%s, %s, %s);
            ''',
            uniprot_gene_rows
        )

    # All inserts succeed together
    conn.commit()

    print("\nTP1 biological entity import completed successfully.")

finally:
    conn.close()