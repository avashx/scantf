from flask import Flask, render_template, request, jsonify, send_from_directory
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CROPPED_FOLDER = 'static/cropped_letters'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CROPPED_FOLDER'] = CROPPED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(CROPPED_FOLDER):
    os.makedirs(CROPPED_FOLDER)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload and OCR processing
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Convert PDF to images if it's a PDF file
    if file.filename.endswith('.pdf'):
        images = convert_from_path(file_path)
    else:
        images = [Image.open(file_path)]

    # Initialize counters and data holders
    extracted_text = ""
    alphabet_count = {}
    alphabet_images = {}

    for image in images:
        # Extract text and count alphabetic characters
        text = pytesseract.image_to_string(image)
        extracted_text += text

        for char in text:
            if char.isalpha():
                alphabet_count[char.lower()] = alphabet_count.get(char.lower(), 0) + 1

        # Detect bounding boxes for each character
        data = pytesseract.image_to_boxes(image)
        for d in data.splitlines():
            parts = d.split()
            char = parts[0].lower()
            if 'a' <= char <= 'z':  # Ensure it's a lowercase alphabet
                x, y, w, h = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
                cropped = image.crop((x, image.height - h, w, image.height - y))
                char_path = os.path.join(app.config['CROPPED_FOLDER'], f"{char}.png")
                cropped.save(char_path)
                alphabet_images[char] = f"/static/cropped_letters/{char}.png"

    os.remove(file_path)  # Clean up uploaded file

    # Return processed text, alphabet counts, and cropped images
    return jsonify({
        'text': extracted_text,
        'alphabet_count': alphabet_count,
        'alphabet_images': alphabet_images
    })

# Serve cropped letter images
@app.route('/static/cropped_letters/<filename>')
def cropped_letter(filename):
    return send_from_directory(app.config['CROPPED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
