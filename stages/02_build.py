import pandas as pd
import os

def build_brick():
    input_file = "download/230106_frozen_metadata.csv.gz"
    output_dir = "brick"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "data.parquet")

    print("Loading data...")
    # Load all string columns as string
    df = pd.read_csv(input_file, dtype=str)
    
    print(f"Loaded {len(df)} rows.")

    # Rename columns
    rename_map = {
        'structure_smiles': 'smiles',
        'structure_inchi': 'inchi',
        'structure_inchikey': 'inchikey',
        'structure_molecular_formula': 'molecular_formula',
        'structure_exact_mass': 'exact_mass',
        'structure_xlogp': 'xlogp',
        'structure_nameIupac': 'iupac_name',
        'structure_nameTraditional': 'traditional_name',
        'organism_name': 'organism_name',
        'organism_taxonomy_ncbiid': 'ncbi_taxonomy_id',
        'reference_doi': 'doi'
    }
    
    # Rename matching columns
    df = df.rename(columns=rename_map)
    
    # Standardize other columns to snake_case if needed
    df.columns = [c.lower() for c in df.columns]

    # Drop rows without SMILES
    initial_count = len(df)
    df = df.dropna(subset=['smiles'])
    print(f"Dropped {initial_count - len(df)} rows without SMILES. New count: {len(df)}")

    # Convert numeric columns where appropriate
    numeric_cols = ['exact_mass', 'xlogp', 'structure_stereocenters_total', 'structure_stereocenters_unspecified']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert to Parquet using pandas directly which is usually robust
    print("Writing to parquet...")
    df.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    build_brick()
