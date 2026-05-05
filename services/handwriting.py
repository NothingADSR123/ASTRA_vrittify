import cv2
import numpy as np
import os
from pdf2image import convert_from_path

def compute_handwriting_similarity(current_file_path: str, sample_path: str) -> float:
    """
    Computes a simple handwriting similarity score using Canny edge detection.
    """
    if not sample_path or not os.path.exists(sample_path):
        return 0.5

    try:
        # Load images
        img1 = _load_image(current_file_path)
        img2 = _load_image(sample_path)

        if img1 is None or img2 is None:
            return 0.5

        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Resize to same dimensions
        height, width = 500, 500
        gray1 = cv2.resize(gray1, (width, height))
        gray2 = cv2.resize(gray2, (width, height))

        # Apply Canny edge detection
        edges1 = cv2.Canny(gray1, 100, 200)
        edges2 = cv2.Canny(gray2, 100, 200)

        # Compute difference
        diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float)))
        similarity = 1 - (diff / 255.0)

        return float(similarity)
    except Exception as e:
        print(f"Error in handwriting similarity: {e}")
        return 0.5

def _load_image(file_path: str):
    """
    Loads an image from a path, supporting PDF by taking the first page.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        pages = convert_from_path(file_path, first_page=1, last_page=1)
        if pages:
            # Convert PIL image to OpenCV format
            return cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
        return None
    else:
        return cv2.imread(file_path)
