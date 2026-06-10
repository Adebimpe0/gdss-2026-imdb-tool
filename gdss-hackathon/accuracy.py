# Accuracy Measurement Script - GDSS 2026 Hackathon
import pandas as pd

# Load both files
extracted = pd.read_csv('output_extracted.csv')
ground_truth = pd.read_excel('output_results.xlsx')

# Standardize column names
extracted.columns = extracted.columns.str.upper().str.strip().str.replace(' ', '_')
ground_truth.columns = ground_truth.columns.str.upper().str.strip().str.replace(' ', '_')

# Fix double underscore in ground truth packaging column
ground_truth = ground_truth.rename(columns={'PACKAGING__TYPE': 'PACKAGING_TYPE'})

# The 13 fields
fields = [
    'ITEM_NAME', 'BARCODE', 'MANUFACTURER', 'BRAND',
    'WEIGHT', 'PACKAGING_TYPE', 'COUNTRY', 'VARIANT',
    'TYPE', 'FRAGRANCE_FLAVOR', 'PROMOTION', 'ADDONS', 'TAGLINE'
]

# Clean both dataframes
for col in fields:
    if col in extracted.columns:
        extracted[col] = extracted[col].fillna('').astype(str).str.upper().str.strip()
    if col in ground_truth.columns:
        ground_truth[col] = ground_truth[col].fillna('').astype(str).str.upper().str.strip()

print("=== ACCURACY REPORT ===\n")
print(f"Our extracted rows: {len(extracted)}")
print(f"Ground truth rows: {len(ground_truth)}")

print("\n=== FIELD BY FIELD FILL RATE ===\n")
for field in fields:
    if field in extracted.columns and field in ground_truth.columns:
        our_filled = (extracted[field] != '').sum()
        gt_filled = (ground_truth[field] != '').sum()
        fill_rate = (our_filled / len(extracted)) * 100
        print(f"{field}:")
        print(f"  We filled: {our_filled}/{len(extracted)} ({fill_rate:.1f}%)")
        print(f"  Ground truth filled: {gt_filled}/{len(ground_truth)}")
        print()

print("\n=== SAMPLE COMPARISON ===\n")
print("Our extraction (first 5 rows):")
print(extracted[['ITEM_NAME', 'BRAND', 'WEIGHT', 'PACKAGING_TYPE', 'COUNTRY']].head())
print("\nGround truth (first 5 rows):")
print(ground_truth[['ITEM_NAME', 'BRAND', 'WEIGHT', 'PACKAGING_TYPE', 'COUNTRY']].head())