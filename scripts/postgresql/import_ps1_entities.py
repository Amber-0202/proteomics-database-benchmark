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

DATASET_ID = 2
ORGANISM_ID = 10090

# TP1 uses AnalyteDescriptor id = 1
PS_DESCRIPTOR_ID = 2

# TP1 analytes occupy 1–7170
ANALYTE_START_ID = 7171

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PS1_FILE = str(Path(os.environ.get("PS1_FILE", PROJECT_ROOT / "data" / "raw" / "260316 Raw data - PS1.xlsx")).expanduser())


# =========================
# Read raw PS1
# =========================

print("Reading PS1...")

df = pd.read_excel(
    PS1_FILE,
    sheet_name="quantification",
    usecols=[
        "Phosphopeptide",
        "Gene",
        "Uniprot",
        "Site",
        "Multiplicity",
        "PTM Localization"
    ]
)

print("Rows:", len(df))
print("Unique phosphopeptides:", df["Phosphopeptide"].nunique())
print("Unique UniProt IDs:", df["Uniprot"].nunique())


# =========================
# Safety checks
# =========================

if len(df) != 39814:
    raise ValueError(
        f"Expected 39814 PS1 rows, but found {len(df)}"
    )

if df["Phosphopeptide"].nunique() != 39814:
    raise ValueError(
        "Phosphopeptide IDs are not unique."
    )

required = ["Gene", "Uniprot", "Site"]

for col in required:
    if df[col].isna().any():
        raise ValueError(
            f"Missing values found in required column: {col}"
        )

if df["Uniprot"].astype(str).str.len().max() > 11:
    raise ValueError(
        "Found UniProt accession longer than VARCHAR(11)."
    )


# =========================
# Parse phosphosite
# =========================

site_parts = (
    df["Site"]
    .astype(str)
    .str.strip()
    .str.extract(r"^([STY])(\d+)$")
)

if site_parts.isna().any(axis=1).any():
    bad_rows = df.loc[
        site_parts.isna().any(axis=1),
        ["Phosphopeptide", "Site"]
    ]

    print(bad_rows.head(20))

    raise ValueError(
        "Some PS1 Site values could not be parsed."
    )

df["amino_acid"] = site_parts[0]
df["residue"] = site_parts[1].astype(int)

df["Uniprot"] = (
    df["Uniprot"]
    .astype(str)
    .str.strip()
)

df["Gene"] = (
    df["Gene"]
    .astype(str)
    .str.strip()
)


# =========================
# Check site consistency
# =========================

site_check = (
    df[["Uniprot", "residue", "amino_acid"]]
    .drop_duplicates()
)

conflicting_sites = (
    site_check
    .groupby(["Uniprot", "residue"])
    ["amino_acid"]
    .nunique()
)

if (conflicting_sites > 1).any():
    raise ValueError(
        "Same accession/residue has conflicting amino acids."
    )


# =========================
# Build Analyte rows
# =========================

analyte_rows = []

for i in range(len(df)):

    analyte_id = ANALYTE_START_ID + i

    analyte_rows.append(
        (
            analyte_id,
            DATASET_ID
        )
    )


# =========================
# Build unique Phosphosite rows
# =========================

unique_sites = (
    df[
        [
            "Uniprot",
            "residue",
            "amino_acid"
        ]
    ]
    .drop_duplicates(
        subset=["Uniprot", "residue"]
    )
    .reset_index(drop=True)
)

unique_sites["phosphosite_id"] = (
    unique_sites.index + 1
)

site_id_map = {
    (
        row.Uniprot,
        int(row.residue)
    ): int(row.phosphosite_id)

    for row in unique_sites.itertuples(index=False)
}


phosphosite_rows = []

for row in unique_sites.itertuples(index=False):

    phosphosite_rows.append(
        (
            int(row.phosphosite_id),
            row.Uniprot,       # accession_id
            row.Uniprot,       # uniprot_entry
            1,                 # variant = isoform 1
            int(row.residue),
            row.amino_acid,
            None,              # phosphosite_group unknown
            None,              # human_analogue unknown
            None               # mod_rsd_type not supplied
        )
    )


# =========================
# DescriptorEntryPhosphosite
# =========================

descriptor_entry_rows = []

for i, row in df.iterrows():

    analyte_id = ANALYTE_START_ID + i
    entry_id = i + 1

    accession = row["Uniprot"]
    residue = int(row["residue"])
    amino_acid = row["amino_acid"]

    descriptor_entry_rows.append(
        (
            entry_id,
            PS_DESCRIPTOR_ID,
            analyte_id,
            accession,
            1,              # variant = isoform
            residue,
            1,              # entry_position
            amino_acid
        )
    )


# =========================
# UniProt reference records
# =========================

unique_uniprot = (
    df[
        ["Uniprot", "Gene"]
    ]
    .drop_duplicates()
)

uniprot_entry_rows = [
    (
        row.Uniprot,
        None,            # protein name unavailable in raw file
        ORGANISM_ID,
        None             # human_entry unavailable
    )
    for row in unique_uniprot.itertuples(index=False)
]


raw_gene_pairs = {
    (
        row.Uniprot,
        row.Gene
    )
    for row in unique_uniprot.itertuples(index=False)
}


print()
print("Prepared from Raw PS1:")
print("Analyte:", len(analyte_rows))
print("AnalyteDescriptor: 1")
print(
    "DescriptorEntryPhosphosite:",
    len(descriptor_entry_rows)
)
print(
    "Unique Phosphosite:",
    len(phosphosite_rows)
)
print(
    "Unique UniProt IDs:",
    len(uniprot_entry_rows)
)


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

        # =========================
        # Safety checks
        # =========================

        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "Analyte"
            WHERE dataset = %s;
            ''',
            (DATASET_ID,)
        )

        existing_ps1_analytes = cur.fetchone()[0]


        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "AnalyteDescriptor"
            WHERE dataset = %s;
            ''',
            (DATASET_ID,)
        )

        existing_ps1_descriptors = cur.fetchone()[0]


        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "DescriptorEntryPhosphosite";
            '''
        )

        existing_ps_entries = cur.fetchone()[0]


        cur.execute(
            '''
            SELECT COUNT(*)
            FROM "Phosphosite";
            '''
        )

        existing_phosphosites = cur.fetchone()[0]


        cur.execute(
            '''
            SELECT MAX(id)
            FROM "Analyte";
            '''
        )

        current_max_analyte = cur.fetchone()[0]


        print()
        print(
            "Existing PS1 analytes:",
            existing_ps1_analytes
        )
        print(
            "Existing PS1 descriptors:",
            existing_ps1_descriptors
        )
        print(
            "Existing phosphosite descriptor entries:",
            existing_ps_entries
        )
        print(
            "Existing phosphosites:",
            existing_phosphosites
        )
        print(
            "Current max Analyte ID:",
            current_max_analyte
        )


        if existing_ps1_analytes != 0:
            raise RuntimeError(
                "PS1 analytes already exist."
            )

        if existing_ps1_descriptors != 0:
            raise RuntimeError(
                "PS1 descriptor already exists."
            )

        if existing_ps_entries != 0:
            raise RuntimeError(
                "DescriptorEntryPhosphosite is not empty."
            )

        if existing_phosphosites != 0:
            raise RuntimeError(
                "Phosphosite table is not empty."
            )

        if current_max_analyte != 7170:
            raise RuntimeError(
                "Expected max Analyte ID to be 7170 "
                f"after TP1, but found {current_max_analyte}."
            )


        # =========================
        # Existing UniProt genes
        # =========================

        cur.execute(
            '''
            SELECT
                uniprot_entry,
                gene_name
            FROM "UniProtGene";
            '''
        )

        existing_gene_pairs = {
            (accession, gene)
            for accession, gene in cur.fetchall()
        }

        new_gene_pairs = sorted(
            raw_gene_pairs - existing_gene_pairs
        )

        print(
            "New UniProtGene mappings to insert:",
            len(new_gene_pairs)
        )


        # =========================
        # Confirmation
        # =========================

        answer = input(
            "\nType IMPORT to insert PS1 biological entities: "
        )

        if answer != "IMPORT":
            print("Import cancelled.")
            conn.rollback()
            raise SystemExit


        # =========================
        # 1. Analyte
        # =========================

        print("\nInserting PS1 Analyte...")

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


        # =========================
        # 2. AnalyteDescriptor
        # =========================

        print("Inserting PS1 AnalyteDescriptor...")

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
                PS_DESCRIPTOR_ID,
                DATASET_ID,
                "AND",
                "PS"
            )
        )


        # =========================
        # 3. UniProtEntry
        # =========================

        print("Updating UniProtEntry reference set...")

        cur.executemany(
            '''
            INSERT INTO "UniProtEntry" (
                accession_id,
                name,
                organism,
                human_entry
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (accession_id)
            DO NOTHING;
            ''',
            uniprot_entry_rows
        )


        # =========================
        # 4. UniProtGene
        # =========================

        print("Inserting new UniProtGene mappings...")

        cur.executemany(
            '''
            INSERT INTO "UniProtGene" (
                uniprot_entry,
                gene_name,
                type
            )
            VALUES (%s, %s, %s);
            ''',
            [
                (
                    accession,
                    gene,
                    None
                )
                for accession, gene in new_gene_pairs
            ]
        )


        # =========================
        # 5. Phosphosite
        # =========================

        print("Inserting unique Phosphosite records...")

        cur.executemany(
            '''
            INSERT INTO "Phosphosite" (
                id,
                accession_id,
                uniprot_entry,
                variant,
                residue,
                amino_acid,
                phosphosite_group,
                human_analogue,
                mod_rsd_type
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            );
            ''',
            phosphosite_rows
        )


        # =========================
        # 6. DescriptorEntryPhosphosite
        # =========================

        print(
            "Inserting DescriptorEntryPhosphosite..."
        )

        cur.executemany(
            '''
            INSERT INTO "DescriptorEntryPhosphosite" (
                id,
                descriptor,
                analyte,
                accession_id,
                variant,
                residue,
                entry_position,
                amino_acid
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            );
            ''',
            descriptor_entry_rows
        )


    conn.commit()

    print()
    print(
        "PS1 biological entity import "
        "completed successfully."
    )

finally:
    conn.close()