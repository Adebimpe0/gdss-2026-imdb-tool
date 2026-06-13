# Export Script - GDSS 2026 Hackathon
# Handles CSV and Excel export of extracted IMDB data

import pandas as pd
import io

def export_to_csv(data):
    """
    Takes a list of dictionaries or a single dictionary
    and returns a CSV file as a string buffer
    """
    if isinstance(data, dict):
        data = [data]
    
    df = pd.DataFrame(data)
    
    # Reorder columns to match IMDB standard
    columns = [
        'item_name', 'barcode', 'manufacturer', 'brand',
        'weight', 'packaging_type', 'country', 'variant',
        'type', 'fragrance_flavor', 'promotion', 'addons', 'tagline'
    ]
    
    # Only keep columns that exist
    columns = [c for c in columns if c in df.columns]
    df = df[columns]
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def export_to_excel(data):
    """
    Takes a list of dictionaries or a single dictionary
    and returns an Excel file as a bytes buffer
    """
    if isinstance(data, dict):
        data = [data]
    
    df = pd.DataFrame(data)
    
    # Reorder columns to match IMDB standard
    columns = [
        'item_name', 'barcode', 'manufacturer', 'brand',
        'weight', 'packaging_type', 'country', 'variant',
        'type', 'fragrance_flavor', 'promotion', 'addons', 'tagline'
    ]
    
    # Only keep columns that exist
    columns = [c for c in columns if c in df.columns]
    df = df[columns]
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='IMDB Data')
    output.seek(0)
    return output

# TEST
if __name__ == "__main__":
    # Test with sample data
    sample = {
        "item_name": "MOK FINE SOAP ROSE 100G",
        "barcode": "6030057221077",
        "manufacturer": "MEIJI GHANA LIMITED",
        "brand": "MOK",
        "weight": "100G",
        "packaging_type": "BOX",
        "country": "GHANA",
        "variant": "",
        "type": "SOAP",
        "fragrance_flavor": "ROSE",
        "promotion": "",
        "addons": "",
        "tagline": "NATURAL AND FRESH"
    }
    
    # Test CSV export
    csv_output = export_to_csv(sample)
    print("CSV Export Test:")
    print(csv_output.read())
    
    # Test Excel export
    excel_output = export_to_excel(sample)
    with open("test_export.xlsx", "wb") as f:
        f.write(excel_output.read())
    print("✅ Excel export saved as test_export.xlsx")