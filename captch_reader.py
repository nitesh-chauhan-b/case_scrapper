import pytesseract
from PIL import Image
import asyncio


async def solve_captcha(image_path):
    # Preprocess the image for better OCR results
    
    # Convert to grayscale and apply thresholding
    img = Image.open(image_path).convert("L")
    
    # Apply a binary threshold to the image
    img = img.point(lambda x: 0 if x < 140 else 255, '1')

    # Resize the image to improve OCR accuracy
    img = img.resize((img.width * 2, img.height * 2))

    # Set the path to the tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    config = '--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
    text = pytesseract.image_to_string(img, config=config)
    # print("Tesseract OCR:", text.strip())
    result = text.strip()

    if result:
        return result
    else:
        raise Exception("No text found in the captcha image")
    

if __name__ == "__main__":
    image_path = "static\image.png"  # Path to the captcha image
    solved_text = asyncio.run(solve_captcha(image_path))
    print(f"Solved Captcha: {solved_text}")

