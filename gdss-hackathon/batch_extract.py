from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
import pandas as pd
import time

load_dotenv()
REQUEST_DELAY_SECONDS = 25

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_from_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    You are a product data extraction expert.
    Look at this product image carefully and extract the following fields.
    Return ONLY a valid JSON object with exactly these 13 keys, nothing else:

    {
        "item_name": "Full descriptive product name in UPPERCASE",
        "barcode": "Numeric barcode digits only, no spaces or dashes",
        "manufacturer": "Company that manufactures the product in UPPERCASE",
        "brand": "Brand name as shown on package in UPPERCASE",
        "weight": "Net weight or volume with unit e.g. 250G, 500ML, 2.2KG",
        "packaging_type": "e.g. BOTTLE, SACHET, TIN, BOX, CAN, POUCH, TUB",
        "country": "Country of manufacture in UPPERCASE",
        "variant": "Product variant e.g. ORIGINAL, LOW FAT. Empty string if none",
        "type": "Short product category e.g. MARGARINE, POWDER, JUICE. Empty string if none",
        "fragrance_flavor": "Flavor or fragrance e.g. STRAWBERRY, ROSE. Empty string if none",
        "promotion": "Any on-pack promotion text. Empty string if none",
        "addons": "Extra features or pack contents. Empty string if none",
        "tagline": "Short promotional tagline. Empty string if none"
    }

    Rules:
    - Use UPPERCASE for all text values
    - If a field is not visible or not applicable, use empty string ""
    - Return ONLY the JSON, no explanation, no markdown, no backticks
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


def batch_extract(images_folder, output_csv):
    images = [f for f in os.listdir(images_folder) if f.endswith('.jpg')]
    
    # Skip already processed images
    already_done = []
    if os.path.exists(output_csv):
        existing = pd.read_csv(output_csv)
        already_done = existing['image_file'].tolist()

    remaining = [f for f in images if f not in already_done]
    total = len(remaining)

    print(f"Total images: {len(images)}")
    print(f"Already processed: {len(already_done)}")
    print(f"Remaining: {total}\n")

    results = []
    failed = []

    for i, image_file in enumerate(remaining):
        image_path = os.path.join(images_folder, image_file)
        print(f"[{i+1}/{total}] Processing: {image_file}")

        try:
            data = extract_from_image(image_path)
            data['image_file'] = image_file
            results.append(data)
            print(f"  ✅ {data.get('item_name', 'N/A')}")

            # Save progress after every 10 images
            if len(results) % 10 == 0:
                df_new = pd.DataFrame(results)
                if os.path.exists(output_csv):
                    df_existing = pd.read_csv(output_csv)
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                else:
                    df_combined = df_new
                df_combined.to_csv(output_csv, index=False)
                results = []
                print(f"  💾 Progress saved!")

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed.append(image_file)

        time.sleep(REQUEST_DELAY_SECONDS)

    # Save any remaining results
    if results:
        df_new = pd.DataFrame(results)
        if os.path.exists(output_csv):
            df_existing = pd.read_csv(output_csv)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        df_combined.to_csv(output_csv, index=False)

    print(f"\n✅ Done! Failed: {len(failed)}")
    if failed:
        print(f"❌ Failed images: {failed}")


if __name__ == "__main__":
    batch_extract("images", "output_extracted.csv")