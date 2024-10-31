import cv2
import pytesseract
import os

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    letters = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        letter_img = image[y:y+h, x:x+w]
        letters.append(letter_img)

    output = {}
    for letter in letters:
        # Recognize the letter (optional)
        letter_text = pytesseract.image_to_string(letter, config='--psm 10')
        letter_text = letter_text.strip().lower()
        if letter_text.isalpha():
            output[letter_text] = letter

    return output
