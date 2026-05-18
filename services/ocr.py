import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

# Set Tesseract path for Windows (common installation locations)
if os.name == 'nt':
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        os.path.expanduser(r'~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text(file_path: str) -> dict:
    """
    Extracts text from an image or PDF file.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    full_text = ""
    success = False

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
        
        # Check if we actually extracted any meaningful text
        full_text = full_text.strip()
        if len(full_text) > 20:  # Arbitrary threshold to consider text meaningful
            success = True
    except Exception as e:
        print(f"OCR Error: {e}")
        full_text = f"Error: OCR engine (Tesseract or Poppler) not found or failed. Details: {str(e)}"

    return {
        "full_text": full_text,
        "snippet": full_text[:200],
        "success": success
    }
