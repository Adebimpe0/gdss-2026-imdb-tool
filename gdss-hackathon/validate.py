# Validation and Normalization Script - GDSS 2026 Hackathon
import pandas as pd
import re

df = pd.read_csv('output_extracted_filled.csv')
df.columns = df.columns.str.upper().str.strip()

print(f"Loaded {len(df)} rows\n")
total_rows = len(df)

# ── 1. NORMALIZE ALL TEXT TO UPPERCASE ──────────────────────────────────────
text_fields = [
    'ITEM_NAME', 'MANUFACTURER', 'BRAND', 'PACKAGING_TYPE',
    'COUNTRY', 'VARIANT', 'TYPE', 'FRAGRANCE_FLAVOR',
    'PROMOTION', 'ADDONS', 'TAGLINE'
]
for col in text_fields:
    if col in df.columns:
        df[col] = df[col].fillna('').astype(str).str.upper().str.strip()

print("✅ Text normalized to uppercase")

# ── 2. VALIDATE AND CLEAN BARCODES ──────────────────────────────────────────
def clean_barcode(val):
    val = str(val).strip().replace(' ', '').replace('-', '')
    # Keep only digits
    digits = re.sub(r'\D', '', val)
    # Valid barcode is 8-13 digits
    if 8 <= len(digits) <= 13:
        return digits
    return ''

df['BARCODE'] = df['BARCODE'].apply(clean_barcode)
valid_barcodes = (df['BARCODE'] != '').sum()
print(f"✅ Barcodes validated: {valid_barcodes}/{total_rows} valid")

# ── 3. NORMALIZE WEIGHT ──────────────────────────────────────────────────────
def normalize_weight(val):
    val = str(val).strip().upper()
    # Standardize units
    val = val.replace(' G', 'G').replace(' KG', 'KG')
    val = val.replace(' ML', 'ML').replace(' L', 'L')
    val = val.replace(' MG', 'MG').replace(' OZ', 'OZ')
    val = val.replace('GMS', 'G').replace('GRAMS', 'G')
    val = val.replace('GRAM', 'G').replace('LITRE', 'L')
    val = val.replace('LITER', 'L').replace('MILLILITER', 'ML')
    val = val.replace('MILLILITRE', 'ML')
    if val in ['', 'NAN', 'NONE']:
        return ''
    return val.strip()

df['WEIGHT'] = df['WEIGHT'].apply(normalize_weight)
print(f"✅ Weights normalized")

# ── 4. NORMALIZE PACKAGING TYPE ─────────────────────────────────────────────
valid_packaging = [
    'BOTTLE', 'SACHET', 'TIN', 'BOX', 'CAN', 'POUCH',
    'TUB', 'WRAPPER', 'JAR', 'TUBE', 'CARTON', 'BAG'
]

def normalize_packaging(val):
    val = str(val).strip().upper()
    for pkg in valid_packaging:
        if pkg in val:
            return pkg
    if val in ['', 'NAN', 'NONE']:
        return ''
    return val

df['PACKAGING_TYPE'] = df['PACKAGING_TYPE'].apply(normalize_packaging)
print(f"✅ Packaging types normalized")

# ── 5. NORMALIZE COUNTRY NAMES ───────────────────────────────────────────────
country_map = {
    'GH': 'GHANA', 'NG': 'NIGERIA', 'CN': 'CHINA',
    'UAE': 'UAE', 'UNITED ARAB EMIRATES': 'UAE',
    'UK': 'UNITED KINGDOM', 'GREAT BRITAIN': 'UNITED KINGDOM',
    'US': 'USA', 'UNITED STATES': 'USA', 'UNITED STATES OF AMERICA': 'USA',
    'VIET NAM': 'VIETNAM', 'COTE D\'IVOIRE': 'IVORY COAST'
}

def normalize_country(val):
    val = str(val).strip().upper()
    if val in ['', 'NAN', 'NONE']:
        return ''
    return country_map.get(val, val)

df['COUNTRY'] = df['COUNTRY'].apply(normalize_country)
print(f"✅ Country names normalized")

# ── 6. ADD CONFIDENCE FLAG ───────────────────────────────────────────────────
critical_fields = ['ITEM_NAME', 'BRAND', 'WEIGHT', 'PACKAGING_TYPE']

def flag_confidence(row):
    empty_count = sum(1 for f in critical_fields if str(row.get(f, '')).strip() == '')
    if empty_count == 0:
        return 'HIGH'
    elif empty_count == 1:
        return 'MEDIUM'
    else:
        return 'LOW'

df['CONFIDENCE'] = df.apply(flag_confidence, axis=1)
high = (df['CONFIDENCE'] == 'HIGH').sum()
medium = (df['CONFIDENCE'] == 'MEDIUM').sum()
low = (df['CONFIDENCE'] == 'LOW').sum()
print(f"✅ Confidence flags added: HIGH={high}, MEDIUM={medium}, LOW={low}")

# ── 7. SAVE FINAL VALIDATED CSV ──────────────────────────────────────────────
df.to_csv('output_final.csv', index=False)
print(f"\n✅ Final validated file saved: output_final.csv")
print(f"Total rows: {len(df)}")