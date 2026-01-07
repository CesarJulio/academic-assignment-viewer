import pandas as pd
import json

# Input and Output paths
input_file = 'Asignacion LUIS CARLOS.xlsx'
output_file = 'data.json'

try:
    # Read Excel file
    df = pd.read_excel(input_file)

    # Select relevant columns
    # 'Semestre Asignatura' might be numeric or text, convert to standard format if needed
    columns_to_keep = [
        'Facultad Code', 'Facultad',
        'Programa Code', 'Programa',
        'Semestre Asignatura',
        'Asignatura Code', 'Asignatura',
        'Grupo',
        'Docente Documento', 'Docente Apellidos', 'Docente Nombres'
    ]
    
    # Filter columns ensuring they exist
    df_filtered = df[[c for c in columns_to_keep if c in df.columns]].copy()
    
    # Clean data
    # Fill NaN with empty string or appropriate placeholders
    df_filtered = df_filtered.fillna('')

    # Helper function to format strings
    def clean_str(val):
        return str(val).strip()

    # Create composite fields or clean existing javaScript consumption
    # We will pass raw data and let JS handle the display formatting "Code - Name"
    # But let's ensure codes are strings to avoid weird float issues (e.g. 2.0 instead of 2)
    for col in ['Facultad Code', 'Programa Code', 'Asignatura Code', 'Semestre Asignatura', 'Grupo', 'Docente Documento']:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].apply(clean_str)

    # REMOVE DUPLICATES
    # The user wants unique records per Group (and other defining fields).
    # Since we dropped schedule info, rows that differed only by time are now identical.
    df_filtered = df_filtered.drop_duplicates()

    # Convert to list of dictionaries
    data = df_filtered.to_dict(orient='records')

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully extracted {len(data)} records to {output_file}")

except Exception as e:
    print(f"Error extracting data: {e}")
