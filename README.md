# AI-Driven Image-to-Item Master Data Tool
### GDSS-Maverick Hackathon 2026

## Overview
This tool automates retail Item Master Database (IMDB) entry by extracting 13 key product attributes directly from product images using AI vision models — eliminating slow, error-prone manual data entry.

## Team
- **Adebimpe Sadiq Maryam** — AI/ML Pipeline, Data Processing, Backend
- **Abdulquyum Ajumobi** — Frontend, Flask Routes, UI/UX

## Features
- Upload a product image (front, back, or side)
- AI extracts 13 IMDB fields automatically:
  - Item Name, Barcode, Manufacturer, Brand, Weight, Packaging Type, Country, Variant, Type, Fragrance/Flavor, Promotion, Addons, Tagline
- Editable preview before export
- Export to CSV or Excel for database import
- Confidence flagging (HIGH/MEDIUM/LOW) for human review

## Tech Stack
- **AI Model**: Google Gemini 2.5 Flash (Vision)
- **Backend**: Python, Flask
- **Frontend**: HTML, Jinja2, Bootstrap
- **Data Processing**: Pandas
- **Export**: CSV / Excel (openpyxl)

## Results — Accuracy on 169 Test Images
| Field | Initial Fill Rate | After Optimization |
|---|---|---|
| Item Name | 99.4% | 99.4% |
| Brand | 98.8% | 98.8% |
| Packaging Type | 100% | 100% |
| Barcode | 43.2% | **97.6%** |
| Manufacturer | 65.7% | **98.8%** |
| Country | 58.0% | **100%** |

**86.4% of products achieved HIGH confidence** across all critical fields.

## How It Works
1. **Upload** — User uploads a product image
2. **Extract** — Gemini Vision analyzes the image and returns structured JSON with 13 fields
3. **Validate** — Barcodes, weights, packaging types, and country names are normalized
4. **Gap-Fill** — Missing fields are cross-referenced across multiple images of the same product
5. **Preview** — User reviews and edits extracted data
6. **Export** — Clean CSV/Excel file ready for database import

## How to Run Locally
```bash
git clone https://github.com/Adebimpe0/gdss-2026-imdb-tool.git
cd gdss-2026-imdb-tool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

GEMINI_API_KEY=your_api_key_here
Run the app:
```bash
python app.py
```

Visit `http://127.0.0.1:5000`

## Future Improvements
- Duplicate product detection (compare by barcode/brand/weight)
- Batch upload support
- Mobile camera integration
