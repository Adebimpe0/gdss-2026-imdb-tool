# Main Flask App - GDSS 2026 Hackathon
# AI-Driven Image-to-Item Master Data Tool

from flask import Flask, request, render_template, send_file, jsonify
from extract import extract_from_image
from export import export_to_csv, export_to_excel
import os
import io
from uuid import uuid4
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Home page"""
    return render_template('home.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'GET':
        """Upload page"""
        return render_template('upload.html')
        
    """Receive image, run AI pipeline, return extracted data"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save uploaded image temporarily
    safe_filename = secure_filename(file.filename)
    _, extension = os.path.splitext(safe_filename)
    extension = extension.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Unsupported file type. Please upload a JPG or PNG image.'}), 400
    try:
        Image.open(file.stream).verify()
        file.stream.seek(0)
    except (UnidentifiedImageError, OSError):
        return jsonify({'error': 'Invalid image content. Please upload a valid JPG or PNG image.'}), 400
    image_path = os.path.join(UPLOAD_FOLDER, f"{uuid4().hex}{extension}")
    file.save(image_path)
    
    try:
        # Run AI extraction pipeline
        data = extract_from_image(image_path)
        # Pass extracted data to preview page
        return render_template('preview.html', data=data)
    except Exception:
        app.logger.exception("Extraction failed")
        return jsonify({'error': 'Image extraction failed. Please ensure the image is valid and readable.'}), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(image_path):
            os.remove(image_path)

@app.route('/export', methods=['POST'])
def export():
    """Receive edited data from preview form and export as CSV or Excel"""
    # Get all form fields
    data = {
        'item_name': request.form.get('item_name', ''),
        'barcode': request.form.get('barcode', ''),
        'manufacturer': request.form.get('manufacturer', ''),
        'brand': request.form.get('brand', ''),
        'weight': request.form.get('weight', ''),
        'packaging_type': request.form.get('packaging_type', ''),
        'country': request.form.get('country', ''),
        'variant': request.form.get('variant', ''),
        'type': request.form.get('type', ''),
        'fragrance_flavor': request.form.get('fragrance_flavor', ''),
        'promotion': request.form.get('promotion', ''),
        'addons': request.form.get('addons', ''),
        'tagline': request.form.get('tagline', '')
    }
    
    export_format = request.form.get('format', 'csv')
    
    if export_format == 'excel':
        output = export_to_excel(data)
        return send_file(
            io.BytesIO(output.read()),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='imdb_data.xlsx'
        )
    else:
        output = export_to_csv(data)
        return send_file(
            io.BytesIO(output.read().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='imdb_data.csv'
        )

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0', debug=True)