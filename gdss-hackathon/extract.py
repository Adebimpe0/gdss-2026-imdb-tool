from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_from_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    You are a product data extraction expert working with retail product images.
    Carefully examine EVERY part of this product image including front, back, sides, 
    top and bottom labels, and extract the following 13 fields.
    
    Return ONLY a valid JSON object with exactly these 13 keys, nothing else:

    {
        "item_name": "Full descriptive product name in UPPERCASE. Include brand, variant, weight and packaging type",
        "barcode": "Look carefully for any barcode number on the image. Check all sides. Return ONLY the numeric digits, no spaces or dashes. If truly not visible return empty string",
        "manufacturer": "Look for text like 'Manufactured by', 'Produced by', 'Made by', or company address details. Return company name in UPPERCASE. Check small print carefully",
        "brand": "Brand name as prominently shown on package in UPPERCASE",
        "weight": "Net weight or volume with unit. Look for 'Net Weight', 'Net Content', 'Poids Net'. e.g. 250G, 500ML, 2.2KG",
        "packaging_type": "Physical container type in UPPERCASE. Choose from: BOTTLE, SACHET, TIN, BOX, CAN, POUCH, TUB, WRAPPER, JAR, TUBE, CARTON, BAG",
        "country": "Look for text like 'Made in', 'Product of', 'Fabriqué en', 'Manufactured in'. Return country name in UPPERCASE. Check all sides of package",
        "variant": "Product variant or subtype e.g. ORIGINAL, LOW FAT, STRAWBERRY FLAVOUR, 3-IN-1. Empty string if none",
        "type": "Short product category in UPPERCASE e.g. DETERGENT, JUICE, MARGARINE, SOAP, TEA, SEASONING POWDER. Empty string if unclear",
        "fragrance_flavor": "Flavor or fragrance specifically mentioned e.g. STRAWBERRY, ROSE, GINGER, LEMON. Empty string if none",
        "promotion": "Any on-pack promotional text e.g. WIN A CAR, 25+7 FREE, BUY 2 GET 1. Empty string if none",
        "addons": "Extra items included or bonus content e.g. FREE SPOON, EXTRA 20%, BONUS PACK. Empty string if none",
        "tagline": "Short marketing tagline or slogan on pack e.g. DELICIOUS TASTE IN EVERY MEAL. Empty string if none"
    }

    IMPORTANT RULES:
    - Use UPPERCASE for ALL text values
    - Look at EVERY part of the image very carefully before deciding a field is empty
    - For barcode: scan the entire image for any numeric barcode
    - For manufacturer: check small print at bottom or back of pack
    - For country: look for 'Made in' or equivalent in any language
    - If a field is truly not visible return empty string ""
    - Return ONLY the JSON object, no explanation, no markdown, no backticks
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        ]
    )

    try:
        result = json.loads(response.text.strip())
    except json.JSONDecodeError:
        text = response.text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        result = json.loads(text[start:end])

    return result