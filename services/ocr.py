import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

def extract_text(file_path: str) -> dict:
    """
    Extracts text from an image or PDF file.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    full_text = ""

    try:
        if file_extension == ".pdf":
            # Convert PDF to images
            pages = convert_from_path(file_path)
            for page in pages:
                text = pytesseract.image_to_string(page)
                full_text += text + "\n"
        elif file_extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            # Extract text from image
            full_text = pytesseract.image_to_string(Image.open(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        print(f"OCR Error: {e}")
        full_text = "Error: OCR engine (Tesseract or Poppler) not found or failed. Please ensure they are installed on your system."

    return {
        "full_text": full_text.strip(),
        "snippet": full_text.strip()[:200]
    }
