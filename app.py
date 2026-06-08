# Main Flask App - GDSS 2026 Hackathon
# AI-Driven Image-to-Item Master Data Tool

from flask import Flask, jsonify
from flask import request, render_template

import extract

app = Flask(__name__)

extracted_data = extract.extract_from_image(image_path="dummy_image.jpg")  # Dummy image path for initial testing

@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    return render_template("home.html")
    # return jsonify({"message": "Welcome to the AI-Driven Image-to-Item Master Data Tool!"})

@app.route("/extract", methods=["GET", "POST"], strict_slashes=False)
def extract_route():
    if request.method == "GET":
        return render_template("extract.html")

    elif request.method == "POST":
        # Get uploaded image
        image_file = request.files["image"]
        image_path = f"uploads/{image_file.filename}"
        image_file.save(image_path)

        # Extract data using AI logic
        # extracted_data = extract.extract_from_image(image_path)

        # return jsonify(extracted_data)  # Return extracted data as JSON for frontend processing

        return render_template("results.html", data=extracted_data)

@app.route("/extracted", methods=["GET", "PATCH"], strict_slashes=False)
def extracted_route():
    if request.method == "GET":
        return render_template("results.html", data=extracted_data)  # Pass extracted data to template

    elif request.method == "PATCH":
        # Handle updates to extracted data (e.g., user corrections)
        updated_data = request.get_json()  # Get updated data from frontend

        # Process the updated data (e.g., save to database)
        #export as csv and excel file and save to local storage
        # Example: export_data_to_files(updated_data)

        return render_template("extracted.html", data=updated_data)
        # return {"message": "Data updated successfully"}, 200


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)
