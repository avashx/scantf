from flask import Flask, request, jsonify, send_file
from PIL import Image
import pytesseract
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text using Tesseract
    text = pytesseract.image_to_string(Image.open(file_path))

    # Generate TTF file (pseudo-code)
    ttf_file_path = generate_font(text)

    return send_file(ttf_file_path, as_attachment=True)

def generate_font(text):
    # Placeholder for font generation logic
    font_name = "HandwrittenFont"
    ttf_file_path = f"{font_name}.ttf"

    # Use FontForge script or command to create the font file
    # Here you would typically call FontForge to process the characters
    # This requires a FontForge script to handle the character extraction and TTF creation.

    # Example command (this is pseudo-code and needs actual implementation):
    # subprocess.run(["fontforge", "-script", "create_font.ff", ttf_file_path, text])
    
    return ttf_file_path

if __name__ == '__main__':
    app.run(debug=True)
