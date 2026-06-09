# Validation and Normalization Logic - GDSS 2026 Hackathon
# This module validates and cleans extracted IMDB fields

import re

def validate_barcode(barcode):
    # Barcodes are typically 8-13 digits
    pattern = r'^\d{8,13}$'
    return re.match(pattern, str(barcode)) is not None

def validate_weight(weight):
    # Weight should have a number followed by a unit (g, kg, ml, L)
    pattern = r'^\d+(\.\d+)?\s*(g|kg|ml|L|oz|lb)$'
    return re.match(pattern, str(weight), re.IGNORECASE) is not None

def normalize_fields(data):
    # Capitalize first letter of key fields
    fields_to_capitalize = [
        "category_type", "segment_type", "manufacturer",
        "brand", "product_name", "packaging_type", "country_of_origin"
    ]
    for field in fields_to_capitalize:
        if field in data and data[field]:
            data[field] = str(data[field]).strip().title()
    return data
