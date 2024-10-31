from flask import Flask, render_template, request, jsonify
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Route for rendering the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload and OCR processing
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Convert PDF to images if necessary
    if file.filename.endswith('.pdf'):
        images = convert_from_path(file_path)
    else:
        images = [Image.open(file_path)]

    # Extract text from each image
    extracted_text = ""
    for image in images:
        extracted_text += pytesseract.image_to_string(image)

    # Determine visible alphabets in extracted text
    visible_alphabets = sorted(set([char.lower() for char in extracted_text if char.isalpha()]))

    # Cleanup: remove the uploaded file
    os.remove(file_path)

    # Return the processed text and visible alphabets
    return jsonify({
        'text': extracted_text,
        'visible_alphabets': visible_alphabets
    })

if __name__ == '__main__':
    app.run(debug=True)
