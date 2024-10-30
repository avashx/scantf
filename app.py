from flask import Flask, request, jsonify, send_file
from PIL import Image
import pytesseract
import fontforge
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = f'uploads/{file.filename}'
    file.save(file_path)
    
    if file.filename.endswith('.pdf'):
        # Convert PDF to images
        images = pdf_to_images(file_path)
    else:
        images = [Image.open(file_path)]

    # Extract glyphs and generate font
    glyphs = extract_glyphs(images)
    font_path = generate_font(glyphs)
    
    return jsonify({
        'success': True,
        'message': 'Font extracted successfully!',
        'font_url': font_path
    })

def pdf_to_images(pdf_path):
    # Convert PDF pages to images
    from pdf2image import convert_from_path
    return convert_from_path(pdf_path)

def extract_glyphs(images):
    glyphs = []
    for image in images:
        text = pytesseract.image_to_string(image)
        # Process text to extract unique glyphs/characters
        glyphs.extend(process_text_to_glyphs(text))
    return glyphs

def process_text_to_glyphs(text):
    # Identify unique characters in the extracted text
    unique_characters = set(text)
    # Further processing to vectorize and prepare glyphs
    return unique_characters

def generate_font(glyphs):
    font = fontforge.font()
    for glyph in glyphs:
        # Add each glyph to font
        font.createChar(ord(glyph), glyph)
    font_path = 'static/fonts/extracted_font.ttf'
    font.generate(font_path)
    return font_path

if __name__ == '__main__':
    app.run(debug=True)
