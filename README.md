# Calcutta High Court Case Scrapper

## Court Chosen
This project is built for the Calcutta High Court online case lookup system.

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/nitesh-chauhan-b/case_scrapper.git
cd case_scrapper
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR
Tesseract is an open-source Optical Character Recognition (OCR) engine. It is used in this project to automatically solve CAPTCHA images required by the court website. Tesseract is chosen for its high accuracy, ease of integration with Python (via pytesseract), and strong community support.

- Download and install Tesseract for Windows from the official release:
  [Tesseract Installer v5.5.0 (Windows)](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

- After installation, copy the installation path (usually `C:\Program Files\Tesseract-OCR\tesseract.exe`).
- Set this path in your `captcha_reader.py` file:

```python
# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Replace the path above with your actual installation path if different.

## CAPTCHA Strategy
- The project uses Tesseract OCR to automatically solve CAPTCHA images.
- Images are preprocessed (grayscale, thresholding, resizing) to improve recognition accuracy.
- The solved text is then used to submit the form on the court website.


## Sample Case Details
Sample case details are provided in the `sample_case_details.txt` file for testing and demonstration purposes.

## Sample Usage
- Run the FastAPI app:
```bash
python app.py
```
- Access the web interface at `http://localhost:8000`
- Enter case details and submit to view results and dashboard.

---

# Screenshots

Below are screenshots of the Calcutta High Court Case Information System web interface:

![Case Search Form](static\SS\1.png)

![Case Search Result](static\SS\2.png)

Watch a demo of the project in action: [Video](https://youtu.be/ELNV73IvnNk)



**Note:**
- Ensure Tesseract is installed and the path is correctly set in `captcha_reader.py`.
- For any issues, refer to the official documentation of [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [FastAPI](https://fastapi.tiangolo.com/).
