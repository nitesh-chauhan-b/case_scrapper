import easyocr
import asyncio
async def solve_captcha(image_path):
    # Specifiying the language for OCR
    reader = easyocr.Reader(['en'])

    # It internally performs the preprocessing and recognition
    # of the captcha image
    results = reader.readtext(image_path, detail=0)
    
    if results:
        return results[0]  # Return the first result as the solved captcha text
    else:
        raise Exception("No text found in the captcha image")
    

if __name__ == "__main__":
    image_path = "static\image.png"  # Path to the captcha image
    solved_text = asyncio.run(solve_captcha(image_path))
    print(f"Solved Captcha: {solved_text}")