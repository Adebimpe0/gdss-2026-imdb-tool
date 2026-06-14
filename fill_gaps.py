import pandas as pd

df = pd.read_csv('output_extracted.csv')
df.columns = df.columns.str.upper().str.strip()
total_rows = len(df)

# Extract product ID from filename
df['PRODUCT_ID'] = df['IMAGE_FILE'].str.split('_').str[0]

fields_to_fill = ['BARCODE', 'MANUFACTURER', 'COUNTRY']

for field in fields_to_fill:
    df[field] = df[field].fillna('').astype(str).str.strip()
    
    # For each product group fill empty values from non-empty ones
    for product_id in df['PRODUCT_ID'].unique():
        mask = df['PRODUCT_ID'] == product_id
        group = df.loc[mask, field]
        filled = group[group != ''].values
        if len(filled) > 0:
            df.loc[mask, field] = filled[0]

df = df.drop(columns=['PRODUCT_ID'])
df.to_csv('output_extracted_filled.csv', index=False)
print("Done! Saved to output_extracted_filled.csv")

print(f"\nAfter filling:")
for field in fields_to_fill:
    filled = (df[field] != '').sum()
    fill_pct = (filled / total_rows * 100) if total_rows else 0
    print(f"{field}: {filled}/{total_rows} ({fill_pct:.1f}%)")