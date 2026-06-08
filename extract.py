# AI Extraction Logic - GDSS 2026 Hackathon
# This module handles image analysis and extracts the 13 IMDB fields

def extract_from_image(image_path):
    # TODO: Connect Gemini Vision API here
    # Returns 13 IMDB fields extracted from product image
    
    # Dummy response for frontend development
    # Frontend dev should use these exact field names in templates
    return {
        "item_name": "GET 3X1 TOP CLEAN ECONOMIQUE DETERGENT EN POUDRE 180G",
        "barcode": "786368779467",
        "manufacturer": "S.D.T.M",
        "brand": "GET",
        "weight": "180G",
        "packaging_type": "SACHET",
        "country": "",
        "variant": "3X1 TOP CLEAN",
        "type": "DETERGENT",
        "fragrance_flavor": "",
        "promotion": "ECONOMIQUE",
        "addons": "",
        "tagline": ""
    }
